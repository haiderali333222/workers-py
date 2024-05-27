import traceback
import json
from threading import Thread
from fastapi.responses import JSONResponse

from .getting_urls import get_urls
from utils.slack import send_slack_message
from pydantic import BaseModel
from typing import List, Optional

class FetchUrlsRequest(BaseModel):
    competitors: Optional[List[str]] = None

async def execute_url_retrieval(data: dict):
    try:
        thread = Thread(target=get_urls, args=[data])
        thread.start()
        thread.join()
    except Exception as e:
        message = f"Error: {str(e)}" + "\n" + traceback.format_exc()
        send_slack_message(message)

async def enqueue_url_fetch_request(request: FetchUrlsRequest):
    data_json = request.model_dump_json()
    
    data = json.loads(data_json)
    await execute_url_retrieval(data)
    return JSONResponse(content={"message": "Getting Urls..."}, status_code=200)
