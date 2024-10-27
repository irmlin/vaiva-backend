import os

import uvicorn
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from src.constants import STATIC_DIR

app = FastAPI()
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.post("/infer")
async def infer(text: str = Form(), image: UploadFile = File(...)):
    video = 'sample.mp4'
    file_path = os.path.join(STATIC_DIR, video)
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(path=file_path, filename=video, media_type="video/mp4")


if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', port=8002, log_level="info", reload=False)
