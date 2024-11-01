import httpx
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import Response

from ..constants import AVATAR_SERVICE_URL


video_router = APIRouter(prefix="/video", tags=["video"])


@video_router.post("/generate-video")
async def generate_video(text: str = Form(), image: UploadFile = File(...)):
    async with httpx.AsyncClient() as client:
        form_data = {
            "text": (None, text),
            "image": (image.filename, await image.read(), image.content_type),
        }
        try:
            response = await client.post(AVATAR_SERVICE_URL, files=form_data, timeout=httpx.Timeout(80))
            response.raise_for_status()

            headers = {'Content-Disposition': 'attachment; filename="generated_video.mp4"'}
            return Response(response.content, headers=headers, media_type='video/mp4')

        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f'Failed to connect to the avatar service: {str(e)}')
        except httpx.TimeoutException as e:
            raise HTTPException(status_code=504, detail=f'The request timed out while waiting for a response from avatar service: {str(e)}')