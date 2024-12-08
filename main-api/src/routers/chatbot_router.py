import os
from typing import Optional

import httpx
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import Response
import aiofiles

from ..constants import SEND_MESSAGE_SERVICE_URL, SPEECH_TO_TEXT_SERVICE_URL, TEXT_TO_SPEECH_SERVICE_URL

# iterpti url visiems endpointams


chatbot_router = APIRouter(prefix="/chatbot", tags=["chatbot"])


@chatbot_router.get("/test")
async def test():
     return 'test'

@chatbot_router.get("/conversation")
async def conversation(audio: Optional[UploadFile] = File(None), message: Optional[str] = Form(None)):
    if not (audio or message):
        raise HTTPException(status_code=400, detail='Either audio file or message is required!')
    llm_input = message
    if audio:
        # If audio is provided, transcribe it to text
        llm_input = await speech_to_text(audio=audio)
    llm_response = await get_llm_response(msg=llm_input)
    # speech = text_to_speech(text=llm_response)
    # return
    return llm_response


async def text_to_speech(text: str) -> str:
    audio_path = './static/audio_for_voice/voice.mp3'
    if not os.path.exists(audio_path):
        raise HTTPException(status_code=400, detail=f'No audio file found for text-to-speech conversion! Excepted: {audio_path}')
    async with aiofiles.open(audio_path, 'rb') as audio_file:
        audio_content = await audio_file.read()
    audio = UploadFile(filename="voice.mp3", file=audio_content, content_type="audio/mpeg")
    form_data = {
        "audio": (audio.filename, audio_content, audio.content_type),
        "text": text
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(TEXT_TO_SPEECH_SERVICE_URL, form_data, timeout=httpx.Timeout(180))
            response.raise_for_status()
            return response.content

        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except httpx.TimeoutException as e:
            raise HTTPException(status_code=504,
                                detail=f'The request timed out while waiting for a response from text-to-speech service: {str(e)}')
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f'Failed to connect to text-to-speech service: {str(e)}')


async def get_llm_response(msg: str) -> str:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(SEND_MESSAGE_SERVICE_URL,
                                        params={'username': 'alex_morgan', 'msg': msg},
                                        timeout=httpx.Timeout(180))
            response.raise_for_status()
            return response.content

        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except httpx.TimeoutException as e:
            raise HTTPException(status_code=504,
                                detail=f'The request timed out while waiting for a response from chatbot service: {str(e)}')
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f'Failed to connect to the chatbot service: {str(e)}')


async def speech_to_text(audio: UploadFile) -> str:
    form_data = {"file": (audio.filename, await audio.read(), audio.content_type)}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(SPEECH_TO_TEXT_SERVICE_URL, files=form_data, timeout=httpx.Timeout(180))
            response.raise_for_status()
            return response.content['transcription']

        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except httpx.TimeoutException as e:
            raise HTTPException(status_code=504, detail=f'The request timed out while waiting for a response from speech-to-text service: {str(e)}')
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f'Failed to connect to the speech-to-text service: {str(e)}')
