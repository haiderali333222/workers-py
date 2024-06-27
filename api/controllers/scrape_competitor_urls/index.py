import json
from typing import List, Optional

from celery.result import AsyncResult
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from utils.scrape_urls.mapping.mapping_for_urls import COMPETITOR_MAPPING
from utils.slack import send_slack_message
from workers.scrape_competitor_urls import scrape_competitor_urls_task


class FetchUrlsRequest(BaseModel):
    competitors: Optional[List[str]] = None


async def enqueue_competitors_url_fetch_request(request: FetchUrlsRequest):
    try:
        data_json = request.model_dump_json()
        data = json.loads(data_json)

        competitors = data.get("competitors", [])

        if not competitors:
            return JSONResponse(status_code=400, content={"message": "No competitors provided"})

        non_existent_competitors = [competitor for competitor in competitors if competitor not in COMPETITOR_MAPPING]

        competitors = [competitor for competitor in competitors if competitor not in non_existent_competitors]

        task_ids = {}
        for competitor in competitors:
            competitor_task = scrape_competitor_urls_task.delay(competitor)
            task_ids[competitor] = competitor_task.id

        message = ""

        if task_ids and not non_existent_competitors:
            message = f"URL Fetch tasks for {competitors} have been enqueued"

        if not task_ids and non_existent_competitors:
            message = "No valid competitors were provided"

        if task_ids and non_existent_competitors:
            message = f"URL Fetch tasks for {competitors} have been enqueued, but the following competitors are invalid: {non_existent_competitors}"

        send_slack_message(message)

        return {
            "task_ids": task_ids,
            "message": message,
            "non_existent_competitors": non_existent_competitors,
        }
    except Exception as err:
        send_slack_message(err,'error')

async def get_task_status(task_id: str):
    task_result = AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": task_result.status,
        "result": task_result.result,
    }
