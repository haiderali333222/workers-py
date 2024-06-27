import ssl
from celery import Celery

# from config import celery
from config.index import REDIS_HOST, REDIS_PASSWORD
from utils.slack import  send_slack_message


celery_app = Celery(__name__)

# Set the broker URL
# Set the broker URL with SSL parameters
celery_app.conf.broker_url = f"rediss://:{REDIS_PASSWORD}@{REDIS_HOST}:6380/0?ssl_cert_reqs=CERT_NONE"
# Set the result backend URL with SSL parameters
celery_app.conf.result_backend = f"rediss://:{REDIS_PASSWORD}@{REDIS_HOST}:6380/0?ssl_cert_reqs=CERT_NONE"

# Set broker transport options with TLS settings
celery_app.conf.broker_transport_options = {
    "visibility_timeout": 3600,
    'ssl': {
        'ssl_cert_reqs': ssl.CERT_NONE,
        'connect_timeout': 10,
        'ssl_check_hostname': False,
    }
}

# Custom retry strategy
def custom_retry_strategy(options):
    return {"interval_start": 0, "interval_step": 0.2, "interval_max": 0.2, "max_retries": 3}

celery_app.conf.broker_transport_options['retry_policy'] = custom_retry_strategy({
    'prev_attempt': 0
})

celery_app.conf.result_backend_transport_options = {
    "retry_policy": {
        "timeout": 5.0
    }
}

# Enable retry on startup
celery_app.conf.broker_connection_retry_on_startup = True

# Import task modules
celery_app.conf.imports = ["workers.scrape_competitor_urls", "workers.email_scrapper_status"]

# Set task routes
celery_app.conf.task_routes = {
    "scrape_competitor_urls_task": {
        "queue": "celery_queue_for_scrape_competitor_urls",
    },
    "email_scrapper_status_task": {
        "queue": "celery_queue_for_send_scrapper_status"
    },
}

# Set task retry policy
celery_app.conf.task_default_retry_delay = 5 * 60  # Retry in 5 minutes
celery_app.conf.task_acks_late = True
celery_app.conf.worker_prefetch_multiplier = 1

send_slack_message(celery_app.conf.broker_url)

