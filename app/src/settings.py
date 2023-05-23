import os
import sys
import datetime as dt
from ast import literal_eval
from pathlib import Path

from loguru import logger
from dotenv import load_dotenv


BASE_DIR: Path = Path(__file__).parent.parent.parent

if not (env_file_path := BASE_DIR / '.env').exists():
    raise FileNotFoundError('.env file not found in project directory.')

load_dotenv(BASE_DIR / '.env')

DEBUG = literal_eval(os.getenv('DEBUG', default=False))
DATA_AMOUNT_IN_DAYS: int = 30
TEST_DIR: Path = BASE_DIR / 'tests'
APP_DIR: Path = BASE_DIR / 'app'
TEMP_DIR: Path = APP_DIR / 'temp'
DATA_DIR: Path = APP_DIR / 'data'
LOGS_DIR: Path = APP_DIR / 'logs'

[dir_.mkdir() for dir_ in (LOGS_DIR, DATA_DIR, TEMP_DIR) if not dir_.exists()]

# Logging config
if DEBUG:
    base_logger, error_logger = logger, logger

else:
    logger.add(sink=LOGS_DIR / 'base.log',
               filter=lambda record: record['extra'].get('name') == 'base',
               rotation=dt.timedelta(days=7))
    logger.add(sink=LOGS_DIR / 'error.log',
               filter=lambda record: record['extra'].get('name') == 'error',
               rotation=dt.timedelta(days=7))
    base_logger = logger.bind(name='base')
    error_logger = logger.bind(name='error')

