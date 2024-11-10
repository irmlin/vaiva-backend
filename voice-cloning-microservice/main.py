import uvicorn
import nltk
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from src.constants import STATIC_DIR
from src.voice_service import VoiceService

nltk.download('averaged_perceptron_tagger_eng')

app = FastAPI()
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

voice_service = VoiceService()

@app.post("/clone-voice")
async def generate_video(audio: UploadFile = File(...), text: str = Form(...)):
    return await voice_service.generate_audio_from_text(audio, text)

if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', port=8002, log_level="info", reload=False)