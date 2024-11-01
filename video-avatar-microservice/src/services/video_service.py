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
        self.__service_results_dir = os.path.join(self.__service_dir, 'results')
        # API static paths
        self.__video_save_dir = os.path.join(STATIC_DIR, 'saved_videos')
        os.makedirs(self.__video_save_dir, exist_ok=True)

    async def generate_video(self, text: str, image: UploadFile):
        # Save input image to storage
        image_id = str(uuid.uuid4())
        image_name = f'{image_id}.jpg'
        image_path = os.path.join(self.__service_img_input_dir, image_name)
        async with aiofiles.open(image_path, 'wb') as out_file:
            content = await image.read()
            await out_file.write(content)

        # Generate avatar video
        video_id = str(uuid.uuid4())
        video_name = f'{video_id}.mp4'
        s = time.time()
        saved_video_path = self.inference.run(source_image=image_path,
                                              driven_audio=os.path.join(self.__service_audio_input_dir, 'bus_chinese.wav'),
                                              output_video_name=video_name)
        print(f'Video generation took: {time.time() - s:.2f} seconds')
        if not os.path.exists(saved_video_path):
            raise HTTPException(status_code=404, detail=f'Expected generated video {video_name} does not exist!')

        moved_video_path = os.path.join(self.__video_save_dir, video_name)
        shutil.move(saved_video_path, moved_video_path)
        return FileResponse(path=moved_video_path, filename=video_name, media_type="video/mp4")
