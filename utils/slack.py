import traceback
from services.slack.slack_message import slack
from config.index import ENVIRONMENT


def slack_notify_info(title, subtitle, message):
    textMessage = f"{ENVIRONMENT} {subtitle or ''}{': ' if subtitle else ''}{message}"
    slackMessageBody = {
        "attachments": [{"title": title, "text": textMessage, "color": "#439FE0"}]
    }
    slack(slackMessageBody)


def slack_notify_error(title, subtitle, error):
    message = f"Error: {str(error)}" + "\n" + traceback.format_exc()
    textMessage = f"{subtitle or ''}{': ' if subtitle else ''}{message}"
    slackMessageBody = {
        "attachments": [
            {
                "title": title,
                "text": textMessage,
                "color": "danger",
                "mrkdwn_in": ["text"],
            }
        ]
    }
    slack(slackMessageBody)


def send_slack_message(message):
    message = f"{ENVIRONMENT} {str(message)}"
    payload = '{"text":"%s"}' % message
    return slack(payload)


def send_detailed_slack_message(title, message):
    full_message = f"*{title}*\n{message}"  # Bold title with newline
    payload = '{"text":"%s"}' % full_message

    return slack(payload)


def error_slack_message(e):
    message = f"Error: {str(e)}" + "\n" + traceback.format_exc()
    send_slack_message(message)
