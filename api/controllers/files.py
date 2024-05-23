import secrets
import hashlib
from fastapi import File
from typing import List
from utils.file_upload_utils import upload_files

class FileUpload:
    @staticmethod
    def upload_files(files_list: List[File]) -> int:
        return upload_files(files_list)

