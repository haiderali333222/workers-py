import requests
from config.index import SLACK_HEADER, ENVIRONMENT, IS_DEVELOPMENT
import traceback
import requests
import json

def slack(slackMessageBody):
    if IS_DEVELOPMENT:
        print(json.dumps(slackMessageBody))
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
