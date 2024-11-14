import os

import uvicorn
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
# ====================================================
# pakeisti i nuoroda i mano servisa:
# from src.services.video_service import VideoService
# ====================================================

from src.constants import STATIC_DIR

app = FastAPI()
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
# cia irgi:
# video_service = VideoService()

# ======================================
# TODO:
# perrasyti visus servisus sukuriant klases 
# ir aprasyti endpointus
# ======================================
@app.get("/send-message")
def send_message():
    return 'send-message'


if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', port=8006, log_level="info", reload=False)