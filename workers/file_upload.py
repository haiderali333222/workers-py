from services.celery.celery_app import celery_app
import os
import pandas as pd

@celery_app.task(name="file_handler_task")
def file_handler_task(file: str):
    try:
        print("here again")
        df = pd.read_excel(file)
        print(f"{df.head()}")
        print(f"file processed {file}")
        os.remove(file)
    except Exception as e:
        print(e)