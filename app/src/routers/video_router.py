import os

from fastapi.responses import FileResponse
from fastapi import APIRouter, HTTPException

from ..constants import STATIC_DIR


video_router = APIRouter(
    prefix="/video",
    tags=["video"]
)


@video_router.get("/generate")
async def generate_avatar_video():
    video = 'sample.mp4'
    file_path = os.path.join(STATIC_DIR, video)
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(path=file_path, filename=video, media_type="video/mp4")
