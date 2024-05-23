
from fastapi import File
from typing import List
from workers.file_upload import file_handler_task
from .generate_random_hash import generate_random_hash


def upload_files(files_list: List[File]) -> int:
    try:
        for f in files_list:
            with open(f'data/temp_{generate_random_hash()}', 'wb') as file_object:
                file_object.write(f.file.read())
                file_handler_task.delay(file_object.name)
        return len(files_list)
    except Exception as e:
        print(e)
            


