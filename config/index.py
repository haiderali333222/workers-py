import os

from dotenv import load_dotenv

load_dotenv()

ENVIRONMENT = os.getenv("ENVIRONMENT")
IS_DEVELOPMENT = ENVIRONMENT == "local"
IS_LOCAL = ENVIRONMENT == "local"
IS_STAGING = ENVIRONMENT == "staging"

DB_URL = os.getenv("DB_URL")
DB_NAME = os.getenv("DB_NAME")

PROXY_CSV_URL = os.getenv("PROXY_CSV_URL")
SLACK_HEADER = os.getenv("SLACK_HEADER")
API_KEY_SCRAPY = os.getenv("API_KEY_SCRAPY")

ELASTIC_SEARCH_URL = os.getenv("ELASTIC_SEARCH_URL")
ELASTIC_SEARCH_USERNAME = os.getenv("ELASTIC_SEARCH_USERNAME")
ELASTIC_SEARCH_PASSWORD = os.getenv("ELASTIC_SEARCH_PASSWORD")

REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = 6380
REDIS_DB = 0
REDIS_URL = "redis://localhost:6379/0" if IS_LOCAL else f"rediss://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

GOOGLE_DRIVE_CREDENTIALS_FILE = "config/google_drive_credentials.json"

WEBDEVEMAIL = "webdev@electrical.com"
MAIL_SENDER_SERVER_TOKEN = "428bd180-5f7e-4cd9-94c0-ecde12b6863a"

MSDB_NAME = os.getenv("MSDB_NAME")
PASSWORD = os.getenv("PASSWORD")
SERVER_NAME = os.getenv("SERVER_NAME")
USER_NAME = os.getenv("USER_NAME")
