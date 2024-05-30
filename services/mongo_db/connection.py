import pymongo
from config.index import DB_URL
from utils.slack import send_slack_message

# client = pymongo.MongoClient(DB_URL, serverSelectionTimeoutMS=5000)

# send_slack_message(str(DB_URL))

mongo_client = None


def mongoConnection():
    global mongo_client  # Access the global client variable
    if mongo_client is not None:
        # send_slack_message("already have mongoConnection")
        return mongo_client

    try:
        # Create a new MongoClient if the global client is None
        mongo_client = pymongo.MongoClient(DB_URL, serverSelectionTimeoutMS=5000)
        # send_slack_message("new mongoConnection created")
        return mongo_client
    except Exception as e:
        # Handle any connection errors here
        send_slack_message(f"MongoDB connection error: {str(e)}")
        return None
