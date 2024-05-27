# Standard library import
import traceback
from datetime import datetime, date
# Third-party library import
from pymongo import UpdateOne
import requests
from dateutil.parser import parse
# local application import
from config.index import DB_NAME
from services.mongo_db.connection import mongoConnection
from utils.slack import send_slack_message
db = mongoConnection()[DB_NAME]
session = requests.Session()

SCRAPPING_URLS = False
URLS_STATUS = "initial"

# get dates and time
def get_date_time():
    today = date.today()
    now = datetime.now()
    d2 = today.strftime("%B %d, %Y")
    current_time = now.strftime("%H:%M:%S")
    date_time = f"{d2} {current_time}"
    date_time = parse(date_time)
    return date_time

def listToString(url):
    return "".join(url)

def url_insert_bulk(data):
    try:
        send_slack_message("inside url_insert_bulk mongo")
        if type(data) is not list or len(data) == 0:
            return
        rows = []
        for item in data:
            filter = {
                "competitor": item["competitor"],
                "url": item["url"],
                "scraper_type": item["scraper_type"]
            }
            rows.append(UpdateOne(filter, {"$setOnInsert": item}, True))
        db.competitor_url.bulk_write(rows)
    except Exception as e:
        message = f"Error: {str(e)}" + "\n" + traceback.format_exc()
        send_slack_message(message)