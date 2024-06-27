# -*- coding: utf-8 -*-
import os
import requests
import subprocess

import uvicorn
from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import JSONResponse

from api.routes.index import api_router
from utils.slack import detailed_error_slack_message, send_slack_message

def log_public_ip():
    try:
        # Make a GET request to api.ipify.org to fetch your public IP
        response = requests.get('https://api.ipify.org/')
        if response.status_code == 200:
            public_ip = response.text.strip()
            print(f"My public IP address is: {public_ip}")
            # Optionally, you can log the IP address to a file or database here
        else:
            print(f"Failed to fetch public IP. Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error fetching public IP: {e}")

# Call the function to log your public IP
log_public_ip()

def print_env():
    env_vars = "\n".join([f"{key}: {value}" for key, value in os.environ.items()])
    send_slack_message(env_vars)


app = FastAPI()
main_router = APIRouter()

main_router.include_router(api_router, prefix="")
app.include_router(main_router)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    detailed_error_slack_message(exc, message="Internal Server Error")
    return JSONResponse(status_code=500, content={"message": "Internal Server Error"})


if __name__ == "__main__":
    print_env()
    celery_beat_cmd = ["celery", "--app", "services.celery.celery_app", "beat"]
    celery_beat_process = subprocess.Popen(celery_beat_cmd)

    celery_worker_cmd_fetch = [
        "celery",
        "--app",
        "services.celery.celery_app",
        "worker",
        "--concurrency=2",
        "-Q",
        "celery_queue_for_scrape_competitor_urls,celery_queue_for_send_scrapper_status",
        "--pool=solo",
    ]

    celery_worker_process_fetch = subprocess.Popen(celery_worker_cmd_fetch)

    send_slack_message("Server Started", "success")
    uvicorn.run(app, host="0.0.0.0", port=8888)

    celery_beat_process.terminate()
    celery_worker_process_fetch.terminate()
