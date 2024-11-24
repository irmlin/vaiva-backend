import os
from typing import List

import httpx
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import Response, FileResponse

from ..constants import DOCUMENTS_DIR, VIDEO_DIR, IMAGES_DIR, AUDIO_DIR


files_router = APIRouter(prefix="/files", tags=["files"])


# DOCUMENTS, USED FOR LLM CONTEXT
# -------------------------------

@files_router.get("/get_all_documents")
async def get_all_documents() -> List[str]:
    # Get all non-hidden files
    documents = [
        file for file in os.listdir(DOCUMENTS_DIR)
        if not file.startswith('.') and os.path.isfile(os.path.join(DOCUMENTS_DIR, file))
    ]
    return documents

@files_router.get("/download_document")
async def download_document(file_name: str):
    file_path = os.path.join(DOCUMENTS_DIR, file_name)
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail=f"File {file_name} not found.")

    return FileResponse(
        path=file_path,
        media_type="application/octet-stream",
        filename=file_name
    )



# AUDIO AND IMAGES ARE USED FOR AVATAR VIDEO GENERATION. SHOULD ALLOW TO UPLOAD ONLY 1 AUDIO FILE AND 1 IMAGE.
# -------------------------------

@files_router.get("/get_all_audio")
async def get_all_audio() -> List[str]:
    audio_files = [
        file for file in os.listdir(AUDIO_DIR)
        if not file.startswith('.') and os.path.isfile(os.path.join(AUDIO_DIR, file))
    ]
    return audio_files

@files_router.get("/download_audio")
async def download_audio(file_name: str):
    file_path = os.path.join(AUDIO_DIR, file_name)
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail=f"File {file_name} not found.")

    return FileResponse(
        path=file_path,
        media_type="application/octet-stream",
        filename=file_name
    )


@files_router.get("/get_all_images")
async def get_all_images() -> List[str]:
    images = [
        file for file in os.listdir(IMAGES_DIR)
        if not file.startswith('.') and os.path.isfile(os.path.join(IMAGES_DIR, file))
    ]
    return images

@files_router.get("/download_image")
async def download_audio(file_name: str):
    file_path = os.path.join(IMAGES_DIR, file_name)
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail=f"File {file_name} not found.")

    return FileResponse(
        path=file_path,
        media_type="application/octet-stream",
        filename=file_name
    )


# VIDEO - THE GENERATED AVATAR VIDEO. SHOULD ALLOW TO KEEP ONLY 1 VIDEO FOR SIMPLICITY
# -------------------------------

@files_router.get("/get_all_videos")
async def get_all_videos() -> List[str]:
    videos = [
        file for file in os.listdir(VIDEO_DIR)
        if not file.startswith('.') and os.path.isfile(os.path.join(VIDEO_DIR, file))
    ]
    return videos

@files_router.get("/download_video")
async def download_video(file_name: str):
    file_path = os.path.join(VIDEO_DIR, file_name)
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail=f"File {file_name} not found.")

    return FileResponse(
        path=file_path,
        media_type="application/octet-stream",
        filename=file_name
    )