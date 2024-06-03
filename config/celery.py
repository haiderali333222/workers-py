from dotenv import load_dotenv
from .index import REDIS_URL

load_dotenv()
# Broker URL
CELERY_BROKER_URL = REDIS_URL
# Configure Celery
broker_url = CELERY_BROKER_URL
broker_transport_options = {"visibility_timeout": 3600}  # 1 hour.
result_backend_transport_options = {"retry_policy": {"timeout": 5.0}}
broker_connection_retry_on_startup = True

imports = ["workers.scrape_competitor_urls"]
task_routes = {
    "scrape_competitor_urls_task": {
        "queue": "celery_queue_for_scrape_competitor_urls"
    },
}
