from postmarker.core import PostmarkClient
from config.index import MAIL_SENDER_SERVER_TOKEN, WEBDEVEMAIL, IS_LOCAL, IS_STAGING
from services.slack.slack_message import send_detailed_slack_message


def email(mesage, to_name, subject, cc_name=[]):
    if IS_LOCAL:
        return
    postmark = PostmarkClient(server_token=MAIL_SENDER_SERVER_TOKEN)
    postmark.emails.send(From=WEBDEVEMAIL, To=to_name, Cc=cc_name, Subject=subject, HtmlBody=mesage)


def email_with_attachments(message, to_name, subject, attachments=None, cc_name=[]):
    try:
        if IS_LOCAL:
            return
        email_subject = subject
        if IS_STAGING:
            email_subject = subject + "-staging"

        if attachments:
            attachment_links = "\n".join(f' \n <a href="{attachment}">{attachment}</a>' for attachment in attachments)
            message += f"<p>Attachments:</p>\n{attachment_links}"

        postmark = PostmarkClient(server_token=MAIL_SENDER_SERVER_TOKEN)
        postmark.emails.send(
            From=WEBDEVEMAIL,
            To=to_name,
            Cc=cc_name,
            Subject=email_subject,
            HtmlBody=message,
        )
    except Exception as e:
        send_detailed_slack_message("email-attachments-error", str(e))
