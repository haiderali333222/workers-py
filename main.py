# -*- coding: utf-8 -*-
import subprocess

import uvicorn
from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import JSONResponse

from api.routes.index import api_router
from utils.slack import detailed_error_slack_message, send_slack_message

app = FastAPI()
main_router = APIRouter()

main_router.include_router(api_router, prefix="")
app.include_router(main_router)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    detailed_error_slack_message(exc, message="Internal Server Error")
    return JSONResponse(status_code=500, content={"message": "Internal Server Error"})


if __name__ == "__main__":
    celery_beat_cmd = ["celery", "--app", "services.celery.celery_app", "beat"]
    celery_beat_process = subprocess.Popen(celery_beat_cmd)

    celery_worker_cmd_fetch = [
        "celery",
        "--app",
        "services.celery.celery_app",
        "worker",
        "--concurrency=3",
        "-Q",
        "celery_queue_for_scrape_competitor_urls,celery_queue_for_send_scrapper_status",
        "--pool=solo",
    ]

    celery_worker_process_fetch = subprocess.Popen(celery_worker_cmd_fetch)

    send_slack_message("Server Started", "success")
    uvicorn.run(app, host="0.0.0.0", port=8888)

    celery_beat_process.terminate()
    celery_worker_process_fetch.terminate()
