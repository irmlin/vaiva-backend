from fastapi import FastAPI, APIRouter
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.constants import STATIC_DIR
from src.routers.video_router import video_router
from src.routers.chatbot_router import chatbot_router
from src.routers.files_router import files_router


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


root_router = APIRouter(prefix="/api")

root_router.include_router(video_router)
root_router.include_router(chatbot_router)
root_router.include_router(files_router)

app.include_router(root_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', port=8001, log_level="info", reload=False)
