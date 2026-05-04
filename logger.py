import logging
from datetime import datetime


logger = logging.getLogger("supermarket_sales")
logger.setLevel(logging.DEBUG)

log_format = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')

console_handler = logging.StreamHandler()
console_handler.setFormatter(log_format)
logger.addHandler(console_handler)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
file_handler = logging.FileHandler(f"logs/pipeline_{timestamp}.log")
file_handler.setFormatter(log_format)
logger.addHandler(file_handler)
