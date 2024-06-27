from celery import Celery

# from config import celery
from config.index import REDIS_HOST, REDIS_PASSWORD

# Create Celery application
celery_app = Celery(__name__)

# celery_app.config_from_object(celery)
celery_app.conf.broker_url = f"rediss://:{REDIS_PASSWORD}@{REDIS_HOST}:6380/0"
celery_app.conf.backend_url = f"rediss://:{REDIS_PASSWORD}@{REDIS_HOST}:6380/0"

celery_app.conf.broker_transport_options = {"visibility_timeout": 3600}  # 1 hour.
celery_app.conf.result_backend_transport_options = {"retry_policy": {"timeout": 5.0}}
celery_app.conf.broker_connection_retry_on_startup = True
celery_app.conf.imports = ["workers.scrape_competitor_urls", "workers.email_scrapper_status"]
celery_app.conf.task_routes = {
    "scrape_competitor_urls_task": {
        "queue": "celery_queue_for_scrape_competitor_urls",
    },
    "email_scrapper_status_task": {"queue": "celery_queue_for_send_scrapper_status"},
}
