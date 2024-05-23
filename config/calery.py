import os
from dotenv import load_dotenv
load_dotenv()
# Broker URL
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
# Result backend
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")
# Accepted content types
# CELERY_ACCEPT_CONTENT = ['json']
# # Task serializer
# CELERY_TASK_SERIALIZER = 'json'
# # Result serializer
# CELERY_RESULT_SERIALIZER = 'json'
# # Timezone
# CELERY_TIMEZONE = 'UTC'