import requests
from config.index import SLACK_HEADER
import json


def slack(slackMessageBody):
    # if IS_LOCAL:
    print("Slack Message: ", json.dumps(slackMessageBody))
    #     return

    headers = {
        "content-type": "application/json",
    }

    try:
        requests.post(
            SLACK_HEADER, headers=headers, data=json.dumps(slackMessageBody)
        )
    except Exception as error:
        print(error)
