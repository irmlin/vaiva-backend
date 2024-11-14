import httpx
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import Response

from ..constants import SEND_MESSAGE_SERVICE_URL
# iterpti url visiems endpointams


chatbot_router = APIRouter(prefix="/chatbot", tags=["chatbot"])


@chatbot_router.get("/test")
async def test():
     return 'test'

@chatbot_router.get("/send-message")
async def conversation():
    async with httpx.AsyncClient() as client:
        try:
            # Request will time out if video is not generated in 180 seconds
            response = await client.get(SEND_MESSAGE_SERVICE_URL, timeout=httpx.Timeout(180))
            response.raise_for_status()

            # headers = {'Content-Disposition': 'attachment; filename="generated_video.mp4"'}
            # return Response(response.content, headers=headers, media_type='video/mp4')
            return response.content

        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except httpx.TimeoutException as e:
            raise HTTPException(status_code=504, detail=f'The request timed out while waiting for a response from avatar service: {str(e)}')
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f'Failed to connect to the chatbot service: {str(e)}')
