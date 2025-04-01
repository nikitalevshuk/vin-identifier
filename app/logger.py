import logging
import sys

LOG_FORMAT = "[%(asctime)s] [%(levelname)s] [%(module)s:%(lineno)d] %(message)s"

def get_logger(name: str) -> logging.getLogger:
    """"Создает логер"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(LOG_FORMAT, datefmt="%Y-%m-%d %H:%M:%S")

    if not logger.hasHandlers():
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)

        logger.addHandler(console_handler)

    return logger