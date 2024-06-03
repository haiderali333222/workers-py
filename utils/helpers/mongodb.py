# Third-party library import
from pymongo import UpdateOne

# local application import
from services.mongo_db.connection import mongoConnection
from utils.slack import send_slack_message, error_slack_message
from config.index import DB_NAME
from utils.helpers.date_time import get_date_time


db = mongoConnection()[DB_NAME]


def url_insert_bulk(data, from_manufacturer=False):
    try:
        if type(data) is not list or len(data) == 0:
            return
        send_slack_message(
            f'Inserting into Mongo DB: {data[0]["competitor"]}', "success"
        )
        rows = []
        for item in data:
            filter = {
                "competitor": item["competitor"],
                "url": item["url"],
                "scraper_type": item["scraper_type"],
            }
            if from_manufacturer:
                item["from_manufacturer"] = True
            item["captured_at"] = get_date_time()

            rows.append(UpdateOne(filter, {"$set": item}, True))
        db.competitor_url.bulk_write(rows)
    except Exception as e:
        error_slack_message(e)


def remove_outdated_urls(competitor):
    try:
        db.competitor_url.delete_many({"competitor": competitor})

        send_slack_message(
            f"Records successfully deleted and Updating outdated records status for {competitor}",
            "success",
        )
        db.competitorproducts.update_many(
            {"competitor": competitor}, {"$set": {"isOutdated": True}}
        )
    except Exception as e:
        error_slack_message(e)
        return


def url_insert(item):
    try:
        if type(item) is not dict:
            return

        send_slack_message(
            f'Inserting 1 item into Mongo DB: {item["competitor"]}', "success"
        )
        filter = {
            "competitor": item["competitor"],
            "url": item["url"],
            "scraper_type": item["scraper_type"],
        }
        item["captured_at"] = get_date_time()
        db.competitor_url.update_one(filter, {"$setOnInsert": item}, True)
    except Exception as e:
        error_slack_message(e)
