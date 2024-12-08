import uvicorn
import nltk
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from src.constants import STATIC_DIR
from src.voice_service import VoiceService
import torch

print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"CUDA version: {torch.version.cuda}")
print(f"Device name: {torch.cuda.get_device_name(0)}")
print(f"Float16 supported: {torch.cuda.get_device_capability(0) >= (7, 0)}")

nltk.download('averaged_perceptron_tagger_eng')

app = FastAPI()

voice_service = VoiceService()


@app.post("/clone-voice")
async def generate_audio(audio: UploadFile = File(...), text: str = Form(...)):
    return await voice_service.generate_audio_from_text(audio, text)

if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', port=8002, log_level="info", reload=False)