from fastapi import UploadFile
from typing import List
from utils.file_upload_utils import upload_files
from utils.slack import slack_notify_error


async def upload_file_queue(files_list: List[UploadFile]) -> dict:
    try:
        print("here")
        files_number = upload_files(files_list)
        print(files_number)
        return {"Number of files will be processed": files_number}
    except Exception as e:
        slack_notify_error(e,"Internal Server Error", subtitle="An error occurred in upload_file_queue")