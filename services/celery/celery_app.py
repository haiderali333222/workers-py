
from celery import Celery
from config import calery

# Create Celery application
celery_app = Celery(__name__)

celery_app.config_from_object(calery)