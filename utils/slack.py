import traceback
from services.slack.slack_message import slack
from config.index import ENVIRONMENT
from .index import get_parent_name


def send_slack_message(
    message, type: str = "info" or "error" or "warning" or "success"
):
    color = "#439FE0"

    switcher = {
        "error": "danger",
        "warning": "warning",
        "success": "good",
    }

    title = f"{ENVIRONMENT.upper()}"

    slackMessageBody = {
        "attachments": [
            {"title": title, "text": message, "color": switcher.get(type, color)}
        ]
    }

    return slack(slackMessageBody)


def error_slack_message(e):
    function_name = get_parent_name()
    message = f"Error {function_name}: {str(e)} \n {traceback.format_exc()}"
    send_slack_message(message, "error")


def detailed_error_slack_message(e, competitor_name=None, message=None):
    error_message = str(e)

    if message:
        error_message = f"{message}\n{error_message}"

    traceback_message = traceback.format_exc()
    function_name = get_parent_name()
    if competitor_name:
        function_name = f"{competitor_name}/{function_name}"

    title = f"{ENVIRONMENT.upper()}: - {function_name}"
    text_message = f"```Error: {error_message}\n{traceback_message}```"
    slackMessageBody = {
        "attachments": [
            {
                "title": title,
                "text": text_message,
                "color": "danger",
                "mrkdwn_in": ["text"],
            }
        ]
    }
    slack(slackMessageBody)
