import logging
import os

# Create the logs directory if it doesn't exist
os.makedirs('src/logs', exist_ok=True)

# Function to create a logger


def setup_logger(name, log_file, level):
    handler = logging.FileHandler(log_file)
    handler.setLevel(level)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s - [%(pathname)s:%(lineno)d]')
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


# Create separate loggers
info_logger = setup_logger('info_logger', 'src/logs/info.log', logging.INFO)
debug_logger = setup_logger(
    'debug_logger', 'src/logs/debug.log', logging.DEBUG)
error_logger = setup_logger(
    'error_logger', 'src/logs/errors.log', logging.ERROR)
warning_logger = setup_logger(
    'warning_logger', 'src/logs/warnings.log', logging.WARNING)
