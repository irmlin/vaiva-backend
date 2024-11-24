import os
from typing import List

import httpx
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import Response, FileResponse

from ..constants import DOCUMENTS_DIR, VIDEO_DIR, IMAGES_DIR, ALLOWED_DOCUMENTS_EXTENSIONS, \
    ALLOWED_AUDIO_EXTENSIONS, AUDIO_FOR_AVATAR_DIR, AUDIO_FOR_VOICE_DIR, ALLOWED_IMAGE_EXTENSIONS
from ..util.util import save_input_file_to_storage, is_directory_empty, delete_files_with_extensions, delete_file

files_router = APIRouter(prefix="/files", tags=["files"])


# DOCUMENTS, USED FOR LLM CONTEXT
# -------------------------------

@files_router.get("/get-all-documents")
async def get_all_documents() -> List[str]:
    # Get all non-hidden files
    documents = [
        file for file in os.listdir(DOCUMENTS_DIR)
        if not file.startswith('.') and os.path.isfile(os.path.join(DOCUMENTS_DIR, file))
    ]
    return documents

@files_router.get("/download-document")
async def download_document(file_name: str):
    file_path = os.path.join(DOCUMENTS_DIR, file_name)
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail=f"File {file_name} not found.")

    return FileResponse(
        path=file_path,
        media_type="application/octet-stream",
        filename=file_name
    )

@files_router.post("/upload-document")
async def upload_document(document: UploadFile = File(...)):
    name, ext = os.path.splitext(document.filename)
    if ext not in ALLOWED_DOCUMENTS_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"File type not supported. Must be one of {ALLOWED_DOCUMENTS_EXTENSIONS}")
    await save_input_file_to_storage(file=document, save_dir=DOCUMENTS_DIR)
    return {'detail': 'File uploaded successfully!', 'file_name': document.filename}


@files_router.delete("/delete-document")
async def delete_document(file_name: str):
    file_path = os.path.join(DOCUMENTS_DIR, file_name)
    return await delete_file(file_path)


# AUDIO USED FOR AVATAR VIDEO GENERATION. SHOULD ALLOW TO UPLOAD ONLY 1 AUDIO FILE.
# -------------------------------

@files_router.get("/get-all-audio-for-avatar")
async def get_all_audio_for_avatar() -> List[str]:
    audio_files = [
        file for file in os.listdir(AUDIO_FOR_AVATAR_DIR)
        if not file.startswith('.') and os.path.isfile(os.path.join(AUDIO_FOR_AVATAR_DIR, file))
    ]
    return audio_files

@files_router.get("/download-audio-for-avatar")
async def download_audio_for_avatar(file_name: str):
    file_path = os.path.join(AUDIO_FOR_AVATAR_DIR, file_name)
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail=f"File {file_name} not found.")

    return FileResponse(
        path=file_path,
        media_type="application/octet-stream",
        filename=file_name
    )

@files_router.post("/upload-audio-for-avatar")
async def upload_audio_for_avatar(audio_file: UploadFile = File(...)):
    name, ext = os.path.splitext(audio_file.filename)
    if ext not in ALLOWED_AUDIO_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"File type not supported. Must be one of {ALLOWED_AUDIO_EXTENSIONS}")
    # Only 1 audio file allowed, so remove previously uploaded file
    delete_files_with_extensions(dir_path=AUDIO_FOR_AVATAR_DIR, extensions=ALLOWED_AUDIO_EXTENSIONS)
    await save_input_file_to_storage(file=audio_file, save_dir=AUDIO_FOR_AVATAR_DIR)
    return {'detail': 'File uploaded successfully!', 'file_name': audio_file.filename}

@files_router.delete("/delete-audio-for-avatar")
async def delete_audio_for_avatar(file_name: str):
    file_path = os.path.join(AUDIO_FOR_AVATAR_DIR, file_name)
    return await delete_file(file_path)


# IMAGES USED FOR AVATAR VIDEO GENERATION. SHOULD ALLOW TO UPLOAD ONLY AND 1 IMAGE.
# -------------------------------

@files_router.get("/get-all-images")
async def get_all_images() -> List[str]:
    images = [
        file for file in os.listdir(IMAGES_DIR)
        if not file.startswith('.') and os.path.isfile(os.path.join(IMAGES_DIR, file))
    ]
    return images

@files_router.get("/download-image")
async def download_image(file_name: str):
    file_path = os.path.join(IMAGES_DIR, file_name)
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail=f"File {file_name} not found.")

    return FileResponse(
        path=file_path,
        media_type="application/octet-stream",
        filename=file_name
    )

@files_router.post("/upload-image")
async def upload_image(image_file: UploadFile = File(...)):
    name, ext = os.path.splitext(image_file.filename)
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"File type not supported. Must be one of {ALLOWED_IMAGE_EXTENSIONS}")
    # Only 1 image file allowed, so remove previously uploaded file
    delete_files_with_extensions(dir_path=IMAGES_DIR, extensions=ALLOWED_IMAGE_EXTENSIONS)
    await save_input_file_to_storage(file=image_file, save_dir=IMAGES_DIR)
    return {'detail': 'File uploaded successfully!', 'file_name': image_file.filename}

@files_router.delete("/delete-image")
async def delete_image(file_name: str):
    file_path = os.path.join(IMAGES_DIR, file_name)
    return await delete_file(file_path)

# VIDEO - THE GENERATED AVATAR VIDEO. SHOULD ALLOW TO KEEP ONLY 1 VIDEO FOR SIMPLICITY
# -------------------------------

@files_router.get("/get-all-videos")
async def get_all_videos() -> List[str]:
    videos = [
        file for file in os.listdir(VIDEO_DIR)
        if not file.startswith('.') and os.path.isfile(os.path.join(VIDEO_DIR, file))
    ]
    return videos

@files_router.get("/download-video")
async def download_video(file_name: str):
    file_path = os.path.join(VIDEO_DIR, file_name)
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail=f"File {file_name} not found.")

    return FileResponse(
        path=file_path,
        media_type="application/octet-stream",
        filename=file_name
    )

@files_router.delete("/delete-video")
async def delete_video(file_name: str):
    file_path = os.path.join(VIDEO_DIR, file_name)
    return await delete_file(file_path)

# AUDIO USED FOR VOICE CLONING. SHOULD ALLOW TO UPLOAD ONLY 1 AUDIO FILE
# -------------------------------

@files_router.get("/get-all-audio-for-voice")
async def get_all_audio_for_voice() -> List[str]:
    audio_files = [
        file for file in os.listdir(AUDIO_FOR_VOICE_DIR)
        if not file.startswith('.') and os.path.isfile(os.path.join(AUDIO_FOR_VOICE_DIR, file))
    ]
    return audio_files

@files_router.get("/download-audio-for-voice")
async def download_audio_for_voice(file_name: str):
    file_path = os.path.join(AUDIO_FOR_VOICE_DIR, file_name)
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail=f"File {file_name} not found.")

    return FileResponse(
        path=file_path,
        media_type="application/octet-stream",
        filename=file_name
    )

@files_router.post("/upload-audio-for-voice")
async def upload_audio_for_voice(audio_file: UploadFile = File(...)):
    name, ext = os.path.splitext(audio_file.filename)
    if ext not in ALLOWED_AUDIO_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"File type not supported. Must be one of {ALLOWED_AUDIO_EXTENSIONS}")
    # Only 1 audio file allowed, so remove previously uploaded file
    delete_files_with_extensions(dir_path=AUDIO_FOR_VOICE_DIR, extensions=ALLOWED_IMAGE_EXTENSIONS)
    await save_input_file_to_storage(file=audio_file, save_dir=AUDIO_FOR_VOICE_DIR)
    return {'detail': 'File uploaded successfully!', 'file_name': audio_file.filename}

@files_router.delete("/delete-audio-for-voice")
async def delete_audio_for_voice(file_name: str):
    file_path = os.path.join(AUDIO_FOR_VOICE_DIR, file_name)
    return await delete_file(file_path)