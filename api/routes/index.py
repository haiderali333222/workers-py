from .files import files_router
from .urls import urls_router
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(files_router, prefix="", tags=["Files"])
api_router.include_router(urls_router, prefix="", tags=["Scrape URLs"])
