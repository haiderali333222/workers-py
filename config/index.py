import os
from dotenv import load_dotenv

load_dotenv()
ES_URL = os.getenv("ELASTIC_SEARCH_URL")
ES_NAME = os.getenv("ELASTIC_SEARCH_USERNAME")
ES_PASSWORD = os.getenv("ELASTIC_SEARCH_PASSWORD")
API_URL = os.getenv("AMPLIFY_API_URL")
# API_URL = "https://amp.electrical.com/api/"
MAIL_SENDER_SERVER_TOKEN = "428bd180-5f7e-4cd9-94c0-ecde12b6863a"
SLACK_HEADER = (
    "https://hooks.slack.com/services/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"
)
DRIVE_ID = "191YWO0qnCNFA-Ap3catRCdWoAJ38GmW3"
WEBDEVEMAIL = "webdev@electrical.com"
SERVER_NAME = os.getenv("SERVER_NAME")
MSDB_NAME = os.getenv("MSDB_NAME")
USER_NAME = os.getenv("USER_NAME")
PASSWORD = os.getenv("PASSWORD")
REDIS_HOST=os.getenv('REDIS_HOST')
REDIS_PASSWORD=os.getenv('REDIS_PASSWORD')
REDIS_SERVER_NAME=os.getenv('REDIS_SERVER_NAME')