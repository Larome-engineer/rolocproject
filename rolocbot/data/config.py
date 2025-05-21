import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

YML_CONF = os.getenv('YML_CONF')
TML_CONF = os.getenv('TML_CONF')
LOG_FILE = os.getenv('LOG_FILE')
ADV_FILE = os.getenv('ADV_FILE')
