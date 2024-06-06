import os
import sys

from config.index import DB_NAME
from services.mongo_db.connection import mongoConnection
from utils.slack import send_slack_message

# facing import issues, We need to get parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

db = mongoConnection()[DB_NAME]


def remove_duplicate(competitor):
    try:
        pipeline = [
            {"$match": {"competitor": competitor}},
            {"$group": {"_id": {"url": "$url"}, "uniqueIds": {"$addToSet": "$_id"}, "capture": {"$addToSet": "$captured_at"}, "count": {"$sum": 1}}},
            {"$match": {"count": {"$gt": 1}}},
        ]
        duplicates = []
        for data in db.competitorproducts.aggregate(pipeline, allowDiskUse=True):
            if len(data["uniqueIds"]) > 1:
                uniqueIds = data["uniqueIds"]
                captured_at = data["capture"]
                max_index = captured_at.index(max(captured_at))
                for i in range(len(uniqueIds)):
                    if i != max_index:
                        duplicates.append(uniqueIds[i])

            if len(duplicates) >= 50000:
                send_slack_message("duplicate-remove: removeing 50000 duplicates")
                db.competitorproducts.delete_many({"_id": {"$in": duplicates}})
                duplicates = []
        if len(duplicates):
            db.competitorproducts.delete_many({"_id": {"$in": duplicates}})
    except Exception as e:
        send_slack_message(f"remove_duplicate_for_all_competitor: {e}", "error")


def remove_duplicate_for_all_competitor():
    try:
        distinct_competitors = db.competitorproducts.distinct("competitor")
        for competitor in distinct_competitors:
            remove_duplicate(competitor)
    except Exception as e:
        send_slack_message(f"remove_duplicate_for_all_competitor: {e}", "error")
