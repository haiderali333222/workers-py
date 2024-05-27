import os
from dotenv import load_dotenv
load_dotenv()
# Broker URL
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
# Configure Celery
broker_url = CELERY_BROKER_URL
broker_transport_options = {"visibility_timeout": 3600}  # 1 hour.
result_backend_transport_options = {"retry_policy": {"timeout": 5.0}}
broker_connection_retry_on_startup = True

imports = ['workers.url_scraper']
task_routes = {
    'urls_scraper_task': {'queue': 'celery_queue_for_url_fetch'},
}