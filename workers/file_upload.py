from services.celery.celery_app import celery_app
import os
import pandas as pd

@celery_app.task(name="File Processing Task")
def file_handler_task(file: str):
    df = pd.read_excel(file)
    print(f"{df.head()}")
    print(f"file processed {file}")
    os.remove(file)
