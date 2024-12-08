import os

import uvicorn
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from src.services.features import FeaturesService
from src.services.conversation import ConversationService

from src.constants import STATIC_DIR

app = FastAPI()
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

features_service = FeaturesService()
conversation_service = ConversationService()

@app.get("/get-features")
async def get_features(username: str):
    return await features_service.get_features(username=username)

# @app.post("/write-features")
# async def write_features(username: str, data: str):
#     return await features_service.write_features(username=username, data=data)

@app.get("/extract-features")
async def extract_features(username: str, msg: str):
    return await features_service.extreact_features(username=username, msg=msg)

@app.get("/send-message")
async def send_message(username: str, msg: str):
    return await conversation_service.send_message(username=username, message=msg, messages=None)

if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', port=8006, log_level="info", reload=False)