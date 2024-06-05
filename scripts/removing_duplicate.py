import os
import sys
from datetime import datetime

from config.index import DB_NAME
from services.mongo_db.connection import mongoConnection

# Import the necessary modules from the parent directory and its subdirectories
from utils.slack import send_slack_message

# facing import issues, We need to get parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

db = mongoConnection()[DB_NAME]


def remove_dublicate():
    send_slack_message("removing dublicate")
    print("conection")
    dupplicate_data_output = db.competitorproducts.aggregate(
        [
            {"$group": {"_id": {"url": "$url"}, "uniqueIds": {"$addToSet": "$_id"}, "capture": {"$addToSet": "$captured_at"}, "count": {"$sum": 1}}},
            {"$match": {"count": {"$gt": 1}}},
        ],
        allowDiskUse=True,
    )
    print("after query")
    send_slack_message("after auery")
    duplicates = []
    for data in dupplicate_data_output:
        if len(data["uniqueIds"]) > 1:
            uniqueIds = data["uniqueIds"]
            captured_at = data["capture"]
            max_index = captured_at.index(max(captured_at))
            for i in range(len(uniqueIds)):
                if i != max_index:
                    duplicates.append(uniqueIds[i])
        if len(duplicates) >= 50000:
            send_slack_message("removing duplicates in 50000")
            db.competitorproducts.delete_many({"_id": {"$in": duplicates}})
            duplicates = []
    if len(duplicates):
        db.competitorproducts.delete_many({"_id": {"$in": duplicates}})


now = datetime.now()
start_time = now.strftime("%H:%M:%S")
send_slack_message(start_time)

remove_dublicate()

now = datetime.now()
end_time = now.strftime("%H:%M:%S")
send_slack_message(end_time)
