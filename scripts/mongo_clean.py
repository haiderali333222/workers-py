import os
import sys
from datetime import datetime

# Import the necessary modules from the parent directory and its subdirectories
from dateutil.parser import parse

from config.index import DB_NAME
from services.mongo_db.connection import mongoConnection
from utils.slack import send_slack_message

# facing import issues, We need to get parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

db = mongoConnection()[DB_NAME]
CHUNK = 50000


def update_query_formation(date, url):
    return {"$set": {"captured_at": date, "url": url}}


def date_update(db_comp_product):
    try:
        for data in db_comp_product:
            _id = data["_id"]
            captured_at = data["captured_at"]
            competitor = data["competitor"]
            url = data["url"]
            if competitor == "radwell":
                if "?redirect" in url:
                    url = url.split("?redirect")[0]
                    if "/en-US" in url:
                        url = url.split("/en-US")
                        url = "".join(url)

            if not isinstance(captured_at, datetime):
                new_date = captured_at.split(",")[1]
                old_date = captured_at.split(",")[0]
                if len(new_date) == 13 and "2022 " not in new_date:
                    new_date = new_date.replace("2022", "2022 ")[1:-1]
                    date = old_date + ", " + new_date
                    dt = parse(date)
                    db.competitorproducts.update_one({"_id": _id}, update_query_formation(dt, url))
                else:
                    dt = parse(captured_at)
                    db.competitorproducts.update_one({"_id": _id}, update_query_formation(dt, url))
    except Exception as e:
        send_slack_message(e)


def cleanMongoData():
    try:
        skip = 0
        urls = []
        product_count = db.competitorproducts.count_documents({})
        while skip < product_count:
            cursor = db.competitorproducts.find().skip(skip).limit(CHUNK)
            urls.extend((list(cursor)))
            skip += CHUNK
            print(skip)
            date_update(urls)
            urls = []
    except Exception as e:
        send_slack_message(e)


now = datetime.now()
start_time = now.strftime("%H:%M:%S")
send_slack_message(start_time)

cleanMongoData()

now = datetime.now()
end_time = now.strftime("%H:%M:%S")
send_slack_message(end_time)
