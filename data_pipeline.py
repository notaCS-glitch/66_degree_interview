import os
from decimal import Decimal
from kaggle_process import get_kaggle_data
from pandas_process import create_df_from_csv, split_df_to_new_df, rename_df_columns, write_df_to_csv, reformat_df_date_col
from sqlite_process import create_tables, upsert_data, run_report_queries

########################################################################################################################
'''
This section will download the dataset and place it in the data directory local to this project
'''

# r"""
handle = 'lovishbansal123/sales-of-a-supermarket'
output_dir = os.path.join(os.getcwd(), 'data')
data_path = get_kaggle_data(data_handle=handle, output_dir=output_dir)
# """

########################################################################################################################
'''
This will read the dataset csv, covert data to specific data types, rename columns, and transform columns
'''

# r"""
file_path = "data/supermarket_sales.csv"
dtype_dict = {
    "Invoice ID": "string",
    "Branch": "string",
    "City": "string",
    "Customer type": "string",
    "Gender": "string",
    "Product line": "string",
    "Quantity": "int32",
    "Tax 5%": "float64",
    "Total": "float64",
    "Date": "string",
    "Time": "string",
    "Payment": "string",
    "gross margin percentage": "float64"
}
converter_dict = {
    "Unit price": Decimal,
    "cogs": Decimal,
    "Rating": Decimal,
    "gross income": Decimal
}
df_supermarket = create_df_from_csv(file_path=file_path, dtype_dict=dtype_dict, converter_dict=converter_dict)

col_name_mapping = {
    "Branch": "branch", # product_location
    "City": "city", # product_location
    "Product line": "product_line", # product_location
    "Tax 5%": "markup_rate", # product_location
    "Gender": "gender", # customer
    "Customer type": "customer_type", # customer
    "Invoice ID": "invoice_id", # sales
    "Quantity": "quantity", # sales
    "Unit price": "unit_price", # sales
    "gross income": "markup_amount", # sales
    "Total": "total", # sales
    "Date": "date", # sales
    "Time": "time", # sales
    "Payment": "payment", # sales
    "Rating": "rating", # sales
    "cogs": "cogs", # None
    "gross margin percentage": "gross_margin_percentage" # None
}
df_supermarket = rename_df_columns(dataframe=df_supermarket, column_name_mapping=col_name_mapping)
df_supermarket['markup_rate'] = df_supermarket['markup_amount'] / df_supermarket['cogs']
df_supermarket = reformat_df_date_col(dataframe=df_supermarket, col_name='date')

# """

########################################################################################################################

# r"""
customer_cols = [
    "gender",
    "customer_type"
]
df_customer = split_df_to_new_df(base_df=df_supermarket, new_df_columns=customer_cols, unique=True)
df_customer.insert(loc=0, column='customer_id', value=range(1, len(df_customer) + 1))
write_df_to_csv(dataframe=df_customer, csv_location='data/customer.csv')
# """

########################################################################################################################

# r"""
product_location_cols = [
    "branch",
    "city",
    "product_line",
    "markup_rate"
]
df_product_location = split_df_to_new_df(base_df=df_supermarket, new_df_columns=product_location_cols, unique=True)
df_product_location.insert(loc=0, column='product_location_id', value=range(1, len(df_product_location) + 1))
write_df_to_csv(dataframe=df_product_location, csv_location='data/product_location.csv')
# """

########################################################################################################################

# r"""
df_supermarket = df_supermarket.merge(
    df_customer[['gender', 'customer_type', 'customer_id']],
    on=['gender', 'customer_type'],
    how='left'
)

df_supermarket = df_supermarket.merge(
    df_product_location[['branch', 'city', 'product_line', 'product_location_id']],
    on=['branch', 'city', 'product_line'],
    how='left'
)

sales_cols = [
    "invoice_id",
    "customer_id",
    "product_location_id",
    "quantity",
    "unit_price",
    "markup_amount",
    "total",
    "date",
    "time",
    "payment",
    "rating"
]
df_sales = split_df_to_new_df(base_df=df_supermarket, new_df_columns=sales_cols, unique=False)
write_df_to_csv(dataframe=df_sales, csv_location='data/sales.csv')
# """

########################################################################################################################
'''
This will create the tables in sqlite and upsert the data to their respective tables
'''

# r"""
db = "supermarket.db"
table_name = create_tables(database=db, table_sql="sql/create_tables/customer.sql")
upsert_data(database=db, dataframe=df_customer, table_name=table_name)

table_name = create_tables(database=db, table_sql="sql/create_tables/product_location.sql")
upsert_data(database=db, dataframe=df_product_location, table_name=table_name)

table_name = create_tables(database=db, table_sql="sql/create_tables/sales.sql")
upsert_data(database=db, dataframe=df_sales, table_name=table_name)
# """

########################################################################################################################
'''
This is where we will build our reports
'''

db = "supermarket.db"


out = run_report_queries(database=db, sql_file='sql/reports/top_porduct_by_female.sql')
print(out)

out = run_report_queries(database=db, sql_file='sql/reports/top_porduct_by_male.sql')
print(out)

out = run_report_queries(database=db, sql_file='sql/reports/top_product_rank.sql')
print(out)

out = run_report_queries(database=db, sql_file='sql/reports/revenue_by_month.sql')
print(out)

out = run_report_queries(database=db, sql_file='sql/reports/top_product_lines_by_city.sql')
print(out)

out = run_report_queries(database=db, sql_file='sql/reports/top_product_lines.sql')
print(out)

out = run_report_queries(database=db, sql_file='sql/reports/customer_demo.sql')
print(out)

out = run_report_queries(database=db, sql_file='sql/reports/markup_report.sql')
print(out)
