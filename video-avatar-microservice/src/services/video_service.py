import os
import shutil
import subprocess
import time
import uuid
import aiofiles

from fastapi import HTTPException, UploadFile
from fastapi.responses import FileResponse
from src.external.sadtalker.inference import Inference
from ..constants import STATIC_DIR


class VideoService:
    def __init__(self):
        print("Loading video service models...")
        self.inference = Inference()
        # Video generating service paths
        self.__service_dir = os.path.join('src', 'external', 'sadtalker')
        self.__service_img_input_dir = os.path.join(self.__service_dir, 'examples', 'source_image')
        self.__service_audio_input_dir = os.path.join(self.__service_dir, 'examples', 'driven_audio')

    async def generate_video(self, audio: UploadFile, image: UploadFile):
        # Save input files to storage
        img_path = await self.__save_input_file_to_storage(file=image, save_dir=self.__service_img_input_dir)
        audio_path = await self.__save_input_file_to_storage(file=audio, save_dir=self.__service_audio_input_dir)

        # Generate avatar video
        video_id = str(uuid.uuid4())
        video_name = f'{video_id}.mp4'
        s = time.time()
        saved_video_path = self.inference.run(source_image=img_path,
                                              driven_audio=audio_path,
                                              output_video_name=video_name)
        print(f'Video generation took: {time.time() - s:.2f} seconds')
        if not os.path.exists(saved_video_path):
            raise HTTPException(status_code=404, detail=f'Expected generated video {video_name} does not exist!')
        return FileResponse(path=saved_video_path, filename=video_name, media_type="video/mp4")

    @staticmethod
    async def __save_input_file_to_storage(file: UploadFile, save_dir: str) -> str:
        _, ext = os.path.splitext(file.filename)
        file_id = str(uuid.uuid4())
        file_name = f'{file_id}{ext}'
        file_path = os.path.join(save_dir, file_name)
        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
        return file_path
