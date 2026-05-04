import pandas as pd
from typing import List
from logger import logger


pd.set_option('display.max_columns', None)


def create_df_from_csv(file_path, dtype_dict, converter_dict):
    try:
        df = pd.read_csv(
            filepath_or_buffer=file_path,
            dtype=dtype_dict,
            converters=converter_dict
        )
        logger.info(f'Dataframe created from {file_path}')
        return df

    except KeyError as e:
        logger.error(f"Mapping Error: Column(s) {', '.join(dtype_dict.keys())}' may not exist in data file --> {e}")
        raise

    except Exception as e:
        logger.error(f'{type(e).__name__}: An error occurred when creating new dataframe --> {e}')
        raise


def rename_df_columns(dataframe, column_name_mapping):
    try:
        dataframe.rename(columns=column_name_mapping, inplace=True)
        logger.info(f'Renamed dataframe columns')
        return dataframe

    except KeyError as e:
        logger.error(f"Mapping Error: Column(s) {', '.join(column_name_mapping.keys())}' may not exist in data file --> {e}")
        raise

    except Exception as e:
        logger.error(f'{type(e).__name__}: An error occurred when renaming dataframe columns --> {e}')
        raise


def split_df_to_new_df(base_df, new_df_columns: List[str], unique=False):
    try:
        if unique:
            new_df = base_df[new_df_columns].drop_duplicates()
            logger.info(f'Dataframe with unique rows created with columns {', '.join(new_df_columns)}')
        else:
            new_df = base_df[new_df_columns]
            logger.info(f'Dataframe created with columns {', '.join(new_df_columns)}')
        return new_df

    except KeyError as e:
        logger.error(f"Mapping Error: Column(s) {', '.join(new_df_columns)}' may not exist in base_df --> {e}")
        raise

    except Exception as e:
        logger.error(f'{type(e).__name__}: An error occurred when creating new dataframe --> {e}')
        raise


def write_df_to_csv(dataframe, csv_location):
    try:
        dataframe.to_csv(csv_location, index=False)
        logger.info(f'CSV created from dataframe: {csv_location}')
    except Exception as e:
        logger.error(f'{type(e).__name__}: An error occurred when creating CSV --> {e}')
        raise
