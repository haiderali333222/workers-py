import traceback
from fastapi import HTTPException
from services.celery.celery_app import celery_app

from jobs.mapping.mapping_for_urls import COMPETITOR_MAPPING
from utils.slack import send_slack_message


@celery_app.task(name="scrape_competitor_urls_task")
def scrape_competitor_urls_task(competitor: str):
    try:
        send_slack_message(f"Starting URL Fetch task for {competitor}...")
        COMPETITOR_MAPPING[competitor]()
        send_slack_message(f"URL Fetch task for {competitor} has been completed")
    except Exception as e:
        message = f"Error: {str(e)}" + "\n" + traceback.format_exc()
        send_slack_message(message)
        raise HTTPException(status_code=500, detail=str(e)) from e
