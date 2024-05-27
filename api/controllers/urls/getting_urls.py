from fastapi import HTTPException
from fastapi.responses import JSONResponse
import traceback

from .scrapping_urls import multithreaded_url_scraper
from utils.slack import send_slack_message


def get_urls(data: dict):
    try:
        if 'competitors' not in data:
            raise HTTPException(status_code=400, detail="Incorrect parameters!")

        competitors = data.get('competitors')
        multithreaded_url_scraper(competitors)

        send_slack_message("{'message': 'Getting Urls...'}")
        return JSONResponse(content={'message': 'Getting Urls...'}, status_code=200)

    except Exception as e:
        message = f"Error: {str(e)}" + "\n" + traceback.format_exc()
        send_slack_message(message)
        raise HTTPException(status_code=500, detail=str(e)) from e
