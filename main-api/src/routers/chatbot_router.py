import os
import uuid
from typing import Optional

from fastapi import APIRouter, HTTPException, UploadFile, File, Form

from ..constants import AUDIO_RESPONSES_DIR
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
    speech_response = await text_to_speech(text=llm_response, username=username)
    print(f'Converted LLM response to speech!')

    # Save in audio_responses folder for later download access
    audio_response_title = f'{username}_{uuid.uuid4()}.wav'
    audio_path = os.path.join(AUDIO_RESPONSES_DIR, audio_response_title)
    with open(audio_path, 'wb') as audio_file:
        audio_file.write(speech_response)
    return {'llm_response': llm_response, 'audio_response_file': audio_response_title}


@chatbot_router.post("/extract-features-for-persona-from-audio")
async def extract_features_from_audio(audio: UploadFile = File(...), username: str = Form(...)):
    text = await speech_to_text(audio=audio)
    response = await extract_features_for_persona(text=text, username=username)
    return {'llm_response': response}


@chatbot_router.post("/extract-features-for-persona-from-text")
async def extract_features_from_text(text: str, username: str):
    response = await extract_features_for_persona(text=text, username=username)
    return {'llm_response': response}
