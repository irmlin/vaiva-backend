import os

import uvicorn
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from src.services.video_service import VideoService

from src.constants import STATIC_DIR

app = FastAPI()
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
video_service = VideoService()


@app.post("/generate-video")
async def generate_video(audio: UploadFile = File(...), image: UploadFile = File(...)):
    return await video_service.generate_video(audio, image)


if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', port=8002, log_level="info", reload=False)