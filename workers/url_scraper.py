import traceback
from fastapi import HTTPException
from api.controllers.urls.scrapping_urls import multithreaded_url_scraper
from utils.slack import send_slack_message
from services.celery.celery_app import celery_app

@celery_app.task(name="fetch_urls_task")
def fetch_urls_task(data: dict):
    try:
        if 'competitors' not in data:
            raise HTTPException(status_code=400, detail="Incorrect parameters!")

        competitors = data.get('competitors')
        multithreaded_url_scraper(competitors)

        print('urls fetched')
        send_slack_message("{'message': 'Getting Urls...'}")
    except Exception as e:
        message = f"Error: {str(e)}" + "\n" + traceback.format_exc()
        send_slack_message(message)
        raise HTTPException(status_code=500, detail=str(e)) from e
