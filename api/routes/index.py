from fastapi import APIRouter

from .scrape_competitor_urls import scrape_competitor_urls_router

api_router = APIRouter()


@api_router.get("/")
async def root():
    return {"message": "Welcome to competitor URL scraping API!"}


api_router.include_router(scrape_competitor_urls_router, prefix="", tags=["Scrape Competitor URLs"])
