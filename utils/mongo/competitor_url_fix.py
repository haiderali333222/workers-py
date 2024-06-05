import os
import sys

from config.index import DB_NAME
from services.mongo_db.connection import mongoConnection
from services.slack.slack_message import send_detailed_slack_message

# facing import issues, We need to get parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
# Import the necessary modules from the parent directory and its subdirectories
from utils.slack import send_slack_message
from services.mongo_db.connection import mongoConnection
from config.index import DB_NAME

db = mongoConnection()[DB_NAME]
CHUNK = 100000


def update_query_formation(url):
    return {"$set": {"url": url}}


def url_update(db_comp_product):
    try:
        for data in db_comp_product:
            _id = data["_id"]
            url = data["url"]

            if "?callback" in url:
                url = url.split("?callback")[0]

            db.competitorproducts.update_one({"_id": _id}, update_query_formation(url))
    except Exception as e:
        send_slack_message(f"competitor-url-fix: {e}", "error")


def competitor_url_fix():
    try:
        skip = 0
        product_count = db.competitorproducts.count_documents({"url": {"$regex": "\\?callback"}})
        send_slack_message(f"competitor-url-fix:{product_count} count")
        while True:
            urls = []
            cursor = db.competitorproducts.find({"url": {"$regex": "\\?callback"}}).limit(CHUNK)
            urls.extend((list(cursor)))
            if len(urls) == 0:
                break
            url_update(urls)
            send_slack_message(f"competitor-url-fix :{len(urls)} updated")
            skip += CHUNK
    except Exception as e:
        send_slack_message(f"competitor-url-fix: {e}", "error")


# now = datetime.now()
# start_time = now.strftime("%H:%M:%S")
# send_detailed_slack_message("competitor-url-fix","Info:  script started at "+start_time)

# competitor_url_fix()

# now = datetime.now()
# end_time = now.strftime("%H:%M:%S")
# send_detailed_slack_message("competitor-url-fix","Info:  script ended at "+end_time)
