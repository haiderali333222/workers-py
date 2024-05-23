
from celery import Celery
from .config import settings

# Create Celery application
celery_app = Celery(__name__)

# Configure Celery
celery_app.conf.broker_url = settings.celery_broker_url
celery_app.conf.result_backend = settings.celery_result_backend

# Define periodic tasks
@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10, periodic_task.s(), name='Periodic task example')

@celery_app.task(name="Periodic Task (every 10 seconds)")
def periodic_task():
    print("Example of periodic task executed!")