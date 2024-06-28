import requests

from typing import List, Optional

from fastapi import APIRouter, FastAPI
from pydantic import BaseModel

from api.controllers.scrape_competitor_urls.index import (
    enqueue_competitors_url_fetch_request,
    get_task_status,
)

app = FastAPI()
scrape_competitor_urls_router = APIRouter()


class FetchUrlsRequest(BaseModel):
    competitors: Optional[List[str]] = None


@scrape_competitor_urls_router.post("/get-urls")
async def fetch_urls(request: FetchUrlsRequest):
    return await enqueue_competitors_url_fetch_request(request)


@scrape_competitor_urls_router.get("/task-status/{task_id}")
async def fetch_status(task_id: str):
    return await get_task_status(task_id)
