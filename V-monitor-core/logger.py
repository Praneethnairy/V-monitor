import logging
import os
from logging.handlers import RotatingFileHandler

def get_logger(name=__name__):
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
        log_path = os.path.join(os.getcwd(), 'vmonitor.log')
        file_handler = RotatingFileHandler(log_path, maxBytes=1_000_000, backupCount=0)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger