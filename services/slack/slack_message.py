import json

import requests

from config.index import IS_LOCAL, SLACK_HEADER


def slack(slackMessageBody):
    if IS_LOCAL:
        print("Slack Message: ", json.dumps(slackMessageBody))
        return

    headers = {
        "content-type": "application/json",
    }

    try:
        requests.post(SLACK_HEADER, headers=headers, data=json.dumps(slackMessageBody))
    except Exception as error:
        print(error)


def send_detailed_slack_message(title, message):
    if IS_LOCAL:
        print(f"{title}: {message}")
        return
    full_message = f"*{title}*\n{message}"  # Bold title with newline
    payload = '{"text":"%s"}' % full_message
    response = requests.post(SLACK_HEADER, data=payload)
    return response
