from fastapi import APIRouter

from .urls import urls_router

api_router = APIRouter()
api_router.include_router(urls_router, prefix="", tags=["Scrape URLs"])
