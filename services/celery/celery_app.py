
from celery import Celery
from config.calery import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

# Create Celery application
celery_app = Celery(__name__)

# Configure Celery
celery_app.conf.broker_url = CELERY_BROKER_URL
celery_app.conf.result_backend = CELERY_RESULT_BACKEND

# Define periodic tasks
@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10, periodic_task.s(), name='Periodic task example')

@celery_app.task(name="Periodic Task (every 10 seconds)")
def periodic_task():
    print("Example of periodic task executed!")