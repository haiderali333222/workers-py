# -*- coding: utf-8 -*-
import os
import subprocess
import redis
import ssl

import uvicorn
from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import JSONResponse

from api.routes.index import api_router
from utils.slack import detailed_error_slack_message, send_slack_message


def check_redis_connection():
    host = os.getenv('REDIS_HOST')
    port = 6380
    password = os.getenv('REDIS_PASSWORD')
    servername = os.getenv('REDIS_SERVER_NAME')
    connect_timeout = 10  # Timeout in seconds

    # Setting up SSL context for TLS connection
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    # Create Redis connection parameters
    connection_params = {
        'host': host,
        'port': port,
        'password': password,
        'ssl': True,
        'ssl_cert_reqs': ssl.CERT_NONE,
        'socket_connect_timeout': connect_timeout,
        'ssl_ca_certs': None,
        'ssl_check_hostname': False,
    }

    # Retry strategy
    # Custom retry mechanism
    max_attempts = 5
    attempt = 0
    while attempt < max_attempts:
        try:
            # Create a Redis client
            client = redis.StrictRedis(**connection_params)
            # Ping the server to check the connection
            client.ping()
            send_slack_message("Connected to Redis successfully!")
            return
        except redis.ConnectionError as e:
            attempt += 1
            wait_time = max(attempt * 100, 3000) / 1000  # Convert milliseconds to seconds
            send_slack_message(f"Failed to connect to Redis (attempt {attempt}/{max_attempts}): {e}",'error')
    
    print("Exceeded maximum retry attempts. Could not connect to Redis.",'error')

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
    check_redis_connection()
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
