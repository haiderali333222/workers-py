import traceback
import json
from threading import Thread
from fastapi.responses import JSONResponse

from utils.slack import send_slack_message
from pydantic import BaseModel
from typing import List, Optional
from celery.result import AsyncResult
from workers.url_scraper import fetch_urls_task

class FetchUrlsRequest(BaseModel):
    competitors: Optional[List[str]] = None

async def enqueue_url_fetch_request(request: FetchUrlsRequest):
    data_json = request.model_dump_json()
    data = json.loads(data_json)

    task = fetch_urls_task.delay(data)

    return  {"task_id": task.id, "message": "Getting URLs started..."}

async def get_task_status(task_id: str):
    task_result = AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": task_result.status,
        "result": task_result.result,
    }