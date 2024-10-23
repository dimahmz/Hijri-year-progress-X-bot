import logging
import os

os.makedirs('src/logs/info', exist_ok=True)
os.makedirs('src/logs/debug', exist_ok=True)
os.makedirs('src/logs/errors', exist_ok=True)
os.makedirs('src/logs/warnings', exist_ok=True)
logging.basicConfig(filename='src/logs/info/index.log', level=logging.INFO)
logging.basicConfig(filename='src/logs/debug/index.log', level=logging.DEBUG)
logging.basicConfig(filename='src/logs/errors/index.log', level=logging.DEBUG)
logging.basicConfig(filename='src/logs/warnings/index.log', level=logging.WARNING)
logger = logging.getLogger(__name__)