import os
import kagglehub
from logger import logger


def get_kaggle_data(data_handle, output_dir):
    try:
        if os.path.isdir(os.path.join(output_dir, '.complete')):
            path = output_dir
            logger.info('Data has already been downloaded')
        else:
            path = kagglehub.dataset_download(handle=data_handle, output_dir=output_dir)
            logger.info(f'Data downloaded to {path}')
        return path

    except ConnectionError as conn_e:
        logger.error(f"Network issue: {conn_e}")
        raise

    except Exception as e:
        logger.error(f'{type(e).__name__}: Something went wrong when downloading the data --> {e}')
        raise



