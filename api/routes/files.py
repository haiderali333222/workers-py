from fastapi import APIRouter, File, UploadFile
from typing import List
from api.controllers.files.index import upload_file_queue

files_router = APIRouter()


@files_router.get("/")
async def root():
    return {"message": "File Upload Example. Please use `/docs` for enter to Swagger UI and test the API"}


@files_router.post("/upload_files/", response_model=dict)
async def upload_files(files: List[UploadFile] = File(...)):
    return await upload_file_queue(files)