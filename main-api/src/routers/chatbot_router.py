import os
from typing import Optional

import aiofiles
import httpx
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Response

from ..constants import SEND_MESSAGE_SERVICE_URL, SPEECH_TO_TEXT_SERVICE_URL, TEXT_TO_SPEECH_SERVICE_URL
from ..util.external_services import text_to_speech, get_llm_response, speech_to_text, extract_features_for_persona

chatbot_router = APIRouter(prefix="/chatbot", tags=["chatbot"])


@chatbot_router.get("/test")
async def test():
     return 'test'

@chatbot_router.post("/conversation")
async def conversation(audio: Optional[UploadFile] = File(None), message: Optional[str] = Form(None), username: str = Form(...)):
    if not (audio or message):
        raise HTTPException(status_code=400, detail='Either audio file or message is required!')
    llm_input = message
    if audio:
        # If audio is provided, transcribe it to text
        print('Transcribing audio...')
        llm_input = await speech_to_text(audio=audio)
    print(f'Calling LLM with: {llm_input}')
    llm_response = await get_llm_response(msg=llm_input, username=username)
    print(f'LLM response: {llm_response}')
    speech_response = await text_to_speech(text=llm_response)
    print(f'Converted LLM response to speech!')
    headers = {'Content-Disposition': 'attachment; filename="speech.wav"'}
    return Response(speech_response, headers=headers, media_type='audio/mpeg')


@chatbot_router.post("/extract-features-for-persona-from-audio")
async def extract_features(audio: UploadFile = File(...), username: str = Form(...)):
    text = await speech_to_text(audio=audio)
    response = await extract_features_for_persona(text=text, username=username)
    return {'llm_response': response}


@chatbot_router.post("/extract-features-for-persona-from-text")
async def extract_features(text: str, username: str = Form(...)):
    response = await extract_features_for_persona(text=text, username=username)
    return {'llm_response': response}
