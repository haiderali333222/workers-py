import requests
from config.index import SLACK_HEADER, IS_LOCAL
import traceback
import requests
import json

def slack(slackMessageBody):
    if IS_LOCAL:
        print("Slack Message: ",json.dumps(slackMessageBody))
        return

    slackUrl = SLACK_HEADER
    headers = {
        'content-type': 'application/json',
    }
    body = slackMessageBody
    try:
        requests.post(slackUrl, headers=headers, data=json.dumps(body))
    except Exception as error:
        print(error)
