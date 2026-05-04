import sqlite3
from logger import logger
from decimal import Decimal
from tabulate import tabulate


# Convert any Decimal object into a String
sqlite3.register_adapter(Decimal, lambda d: str(d))


def create_tables(database, table_sql):
    conn = sqlite3.connect(database)
    try:
        with open(table_sql, 'r') as f:
            f_sql = f.read()

        table_name = f_sql.split('\n')[0].split(' ')[-2]

        cursor = conn.cursor()
        cursor.executescript(f_sql)

        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
        if cursor.fetchone():
            logger.info(f"Table '{table_name}' successfully created")
            conn.commit()
            return table_name
        else:
            raise Exception(f"Table '{table_name}' failed created")

    except Exception as e:
        conn.rollback()
        logger.error(f'{type(e).__name__}: An error occurred when creating sql table --> {e}')
        raise

    finally:
        conn.close()


def upsert_data(database, dataframe, table_name):
    conn = sqlite3.connect(database)
    try:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")

        data = dataframe.to_records(index=False).tolist()

        cols_list = dataframe.columns.tolist()
        values_list = ['?' for col in cols_list]

        set_clause = ',\n'.join([f"{col} = excluded.{col}" for col in cols_list[1:]])

        query_list = [
            f"INSERT INTO {table_name} ({', '.join(cols_list)})",
            f"VALUES ({', '.join(values_list)})",
            f"ON CONFLICT({cols_list[0]})",
            f"DO UPDATE SET",
            f"{set_clause};"
        ]
        query = '\n'.join(query_list)
        cursor.executemany(query, data)

        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        db_count = cursor.fetchone()[0]

        logger.info(f"Verification: DataFrame has {len(dataframe)} rows | SQLite has {db_count} rows.")

        if len(dataframe) == db_count:
            logger.info("Data load verified: Row counts match.")
            conn.commit()
        else:
            raise Exception("Data load mismatch: Row counts do not match!")

    except Exception as e:
        conn.rollback()
        logger.error(f'{type(e).__name__}: An error occurred when loading data into {table_name} --> {e}')
        raise

    finally:
        conn.close()


def run_report_queries(database, sql_file):
    conn = sqlite3.connect(database)

    try:
        with open(sql_file, 'r') as f:
            query = f.read()

        cursor = conn.cursor()
        cursor.execute(query)

        rows = cursor.fetchall()
        headers = [description[0] for description in cursor.description]

        return tabulate(rows, headers=headers, tablefmt="grid")

    except Exception as e:
        logger.error(f'{type(e).__name__}: An error occurred when running the joining query --> {e}')
        raise

    finally:
        conn.close()

