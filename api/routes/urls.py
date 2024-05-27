from api.controllers.urls.index import enqueue_url_fetch_request, get_task_status
from pydantic import BaseModel
from typing import List, Optional
from fastapi import FastAPI, APIRouter


app = FastAPI()
urls_router = APIRouter()


class FetchUrlsRequest(BaseModel):
    competitors: Optional[List[str]] = None

@urls_router.post("/get-urls")
async def fetch_urls(request: FetchUrlsRequest):
    return await enqueue_url_fetch_request(request)
    
    
@urls_router.get("/task-status/{task_id}")
async def fetch_status(task_id: str):
    return await get_task_status(task_id)