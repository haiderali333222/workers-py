from celery import Celery

from config import celery

# Create Celery application
celery_app = Celery(__name__)

celery_app.config_from_object(celery)
