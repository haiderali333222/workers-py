from utils.scrape_urls.mapping.mapping_for_urls import COMPETITOR_MAPPING
from utils.slack import error_slack_message, send_slack_message


from celery import Celery

# from config import celery
from config.index import REDIS_HOST, REDIS_PASSWORD
from utils.slack import  send_slack_message

# Create Celery application
celery = Celery(__name__)

# celery.config_from_object(celery)
celery.conf.broker_url = f"rediss://:{REDIS_PASSWORD}@{REDIS_HOST}:6380/0"
celery.conf.backend_url = f"rediss://:{REDIS_PASSWORD}@{REDIS_HOST}:6380/0"


celery.conf.broker_transport_options = {"visibility_timeout": 3600,   'ssl': {
            'servername': REDIS_HOST,
            'connectTimeout': 10000,
        }}  # 1 hour.

celery.conf.broker_retry_strategy=lambda options: max(options.get('prev_attempt', 0) * 100, 3000),
celery.conf.result_backend_transport_options = {"retry_policy": {"timeout": 5.0}}
celery.conf.broker_connection_retry_on_startup = True
celery.conf.imports = ["workers.scrape_competitor_urls", "workers.email_scrapper_status"]
celery.conf.task_routes = {
    "scrape_competitor_urls_task": {
        "queue": "celery_queue_for_scrape_competitor_urls",
    },
    "email_scrapper_status_task": {"queue": "celery_queue_for_send_scrapper_status"},
}

send_slack_message(celery.conf.broker_url)



@celery.task(name="scrape_competitor_urls_task")
def scrape_competitor_urls_task(competitor: str):
    try:
        message = f"Starting URL Fetch task for {competitor}"
        send_slack_message(message)
        COMPETITOR_MAPPING[competitor]()
        message = f"URL Fetch task for {competitor} completed"
        send_slack_message(message, "success")
    except Exception as e:
        error_slack_message(e)
