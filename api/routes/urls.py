from api.controllers.urls.index import enqueue_url_fetch_request
from pydantic import BaseModel
from typing import List, Optional
from fastapi import FastAPI, APIRouter


app = FastAPI()
urls_router = APIRouter()


class FetchUrlsRequest(BaseModel):
    competitors: Optional[List[str]] = None

@urls_router.post("/get-urls")
async def fetch_urls(request: FetchUrlsRequest):
    await enqueue_url_fetch_request(request)