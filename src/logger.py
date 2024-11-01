import logging
import os
from dotenv import load_dotenv

load_dotenv(".env")


environment = os.getenv("ENVIRONMENT")

logs_folder = "src/logs/prod"

if (environment == "development"):
    logs_folder = "src/logs/dev"
elif (environment == "test"):
    logs_folder = "src/logs/test"

# Create the logs directory if it doesn't exist
os.makedirs(logs_folder, exist_ok=True)

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

info_logger = setup_logger('info_logger', f'{logs_folder}/info.log', logging.INFO)
debug_logger = setup_logger(
    'debug_logger', f'{logs_folder}/debug.log', logging.DEBUG)
error_logger = setup_logger(
    'error_logger', f'{logs_folder}/errors.log', logging.ERROR)
warning_logger = setup_logger('warning_logger', f'{logs_folder}/warnings.log', logging.WARNING)