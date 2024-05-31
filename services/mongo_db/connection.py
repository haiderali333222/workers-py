import pymongo
from config.index import DB_URL
from utils.slack import send_slack_message

mongo_client = None


def mongoConnection():
    global mongo_client  # Access the global client variable
    if mongo_client is not None:
        return mongo_client

    try:
        mongo_client = pymongo.MongoClient(DB_URL, serverSelectionTimeoutMS=5000)
        return mongo_client
    except Exception as e:
        send_slack_message(f"MongoDB connection error: {str(e)}", "error")
        return None
