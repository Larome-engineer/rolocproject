import toml
import yaml
from aiogram import Bot, Dispatcher
from data.config import YML_CONF, TML_CONF
from aiogram.client.bot import DefaultBotProperties

TOML = toml.load(TML_CONF)

with open(YML_CONF) as yam:
    YAML = yaml.safe_load(yam)

# [MESSAGES]
admin_messages = TOML['admin_msg']
user_messages = TOML['user_msg']

# [KEYBOARD-TEXT]
common_kb_text = TOML['common_kb']
admin_kb_text = TOML['admin_kb']
user_kb_text = TOML['user_kb']

# [TELEGRAM]
telegram = YAML['telegram']
webhook = telegram['webhook']
webapp = telegram['webapp']

ADMIN_IDS = telegram['admin_ids']
BOT_TOKEN = telegram['bot_token']

WEBHOOK_DOMAIN = webhook['domain']
WEBHOOK_PATH = webhook['path']
WEBHOOK_URL = f"{WEBHOOK_DOMAIN}{WEBHOOK_PATH}"

WEBAPP_HOST = webapp['host']
WEBAPP_PORT = webapp['port']


# [DATABASE]
database = YAML['database']
DBNAME = database['dbname']
HOST = database['host']
PORT = database['port']
USERNAME = database['username']
PASSWORD = database['password']

roloc_bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher()
