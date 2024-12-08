import os
from typing import List

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse

from ..constants import VIDEO_DIR, ALLOWED_AUDIO_EXTENSIONS, AUDIO_FOR_VOICE_DIR, ALLOWED_IMAGE_EXTENSIONS, \
    AUDIO_RESPONSES_DIR
from ..util.util import save_input_file_to_storage, delete_files_with_extensions, delete_file

files_router = APIRouter(prefix="/files", tags=["files"])


# VIDEO - THE GENERATED AVATAR VIDEO
# -------------------------------

@files_router.get("/get-all-videos")
async def get_all_videos() -> List[str]:
    videos = [
        file for file in os.listdir(VIDEO_DIR)
        if not file.startswith('.') and os.path.isfile(os.path.join(VIDEO_DIR, file))
    ]
    return videos

@files_router.get("/download-video/{file_name}")
async def download_video(file_name: str):
    file_path = os.path.join(VIDEO_DIR, file_name)
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail=f"File {file_name} not found.")

    return FileResponse(
        path=file_path,
        media_type="application/octet-stream",
        filename=file_name
    )

@files_router.delete("/delete-video/{file_name}")
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

@files_router.get("/download-audio-for-voice/{file_name}")
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
async def upload_audio_for_voice(audio_file: UploadFile = File(...), username: str = Form(...)):
    name, ext = os.path.splitext(audio_file.filename)
    if ext not in ALLOWED_AUDIO_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"File type not supported. Must be one of {ALLOWED_AUDIO_EXTENSIONS}")
    # Only 1 audio file allowed, so remove previously uploaded file
    delete_files_with_extensions(dir_path=AUDIO_FOR_VOICE_DIR, extensions=ALLOWED_IMAGE_EXTENSIONS)
    name = f'{username}{ext}'
    await save_input_file_to_storage(file=audio_file, save_dir=AUDIO_FOR_VOICE_DIR, name=name)
    return {'detail': 'File uploaded successfully!', 'file_name': name}

@files_router.delete("/delete-audio-for-voice/{file_name}")
async def delete_audio_for_voice(file_name: str):
    file_path = os.path.join(AUDIO_FOR_VOICE_DIR, file_name)
    return await delete_file(file_path)



# AUDIO RESPONSES FOR FRONTEND
# -------------------------------

@files_router.get("/download-audio-response/{audio_file_name}")
async def download_video(audio_file_name: str):
    file_path = os.path.join(AUDIO_RESPONSES_DIR, audio_file_name)
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail=f"File {audio_file_name} not found.")

    return FileResponse(
        path=file_path,
        media_type="application/octet-stream",
        filename=audio_file_name
    )