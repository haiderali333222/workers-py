import os
from dotenv import load_dotenv

load_dotenv()

ENVIRONMENT = os.getenv("ENVIRONMENT")
IS_DEVELOPMENT = ENVIRONMENT == "local"
API_URL = os.getenv("AMPLIFY_API_URL")
IS_LOCAL = ENVIRONMENT == "local"
IS_STAGING = ENVIRONMENT == "staging"
DB_URL = os.getenv("DB_URL")
DB_NAME = os.getenv("DB_NAME")
PROXY_CSV_URL = os.getenv("PROXY_CSV_URL")
SLACK_HEADER = os.getenv("SLACK_HEADER")
API_KEY_SCRAPY = os.getenv("API_KEY_SCRAPY")
REDIS_PORT = 6380
REDIS_DB = 0

REDIS_URL = os.getenv("REDIS_URL")
