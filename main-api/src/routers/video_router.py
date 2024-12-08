import os

import httpx
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import Response

from ..constants import AVATAR_SERVICE_URL, VIDEO_DIR

video_router = APIRouter(prefix="/video", tags=["video"])


@video_router.post("/generate-video")
async def generate_video(audio: UploadFile = File(...), image: UploadFile = File(...), username: str = Form(...)):
    async with httpx.AsyncClient() as client:
        form_data = {
            "audio": (audio.filename, await audio.read(), audio.content_type),
            "image": (image.filename, await image.read(), image.content_type),
        }
        try:
            # Request will time out if video is not generated in 180 seconds
            response = await client.post(AVATAR_SERVICE_URL, files=form_data, timeout=httpx.Timeout(180))
            response.raise_for_status()

            # Save in videos folder for later download access
            video_name = f'{username}.mp4'
            video_path = os.path.join(VIDEO_DIR, video_name)
            with open(video_path, 'wb') as video_file:
                video_file.write(response.content)

            return {'video_name': video_name}

        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except httpx.TimeoutException as e:
            raise HTTPException(status_code=504, detail=f'The request timed out while waiting for a response from avatar service: {str(e)}')
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f'Failed to connect to the avatar service: {str(e)}')
