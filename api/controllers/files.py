from fastapi import UploadFile
from typing import List
from utils.file_upload_utils import upload_files

async def upload_file_queue(files_list: List[UploadFile]) -> dict:
    try:
        print("here")
        files_number = upload_files(files_list)
        print(files_number)
        return {"Number of files will be processed": files_number}
    except Exception as e:
        print(e)