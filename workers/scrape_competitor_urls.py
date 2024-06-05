from services.celery.celery_app import celery_app
from utils.scrape_urls.mapping.mapping_for_urls import COMPETITOR_MAPPING
from utils.slack import error_slack_message, send_slack_message


@celery_app.task(name="scrape_competitor_urls_task")
def scrape_competitor_urls_task(competitor: str):
    try:
        message = f"Starting URL Fetch task for {competitor}"
        send_slack_message(message)
        COMPETITOR_MAPPING[competitor]()
        message = f"URL Fetch task for {competitor} completed"
        send_slack_message(message, "success")
    except Exception as e:
        error_slack_message(e)
