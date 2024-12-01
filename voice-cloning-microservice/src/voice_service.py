import uuid
import torch
import os
import aiofiles
from melo.api import TTS
from src.openvoice.api import ToneColorConverter
from src.openvoice import se_extractor
from fastapi import HTTPException, UploadFile
from fastapi.responses import FileResponse

class VoiceService:
    def __init__(self):
        print("Loading voice service models...")
        # Initialization
        ckpt_converter = 'src/checkpoints_v2/converter' 
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"

        self.input_dir = 'src/inputs'
        self.output_dir = 'src/outputs'
        self.processed_dir = 'src/processed'

        self.tone_color_converter = ToneColorConverter(f'{ckpt_converter}/config.json', device=self.device)
        self.tone_color_converter.load_ckpt(f'{ckpt_converter}/checkpoint.pth')
        # Should be loaded before if possible
        
    
    async def generate_audio_from_text(self, audio: UploadFile, text: str):
        audio_path = await self.__save_input_file_to_storage(file=audio, save_dir=self.input_dir)
        src_path  = f'{self.output_dir}/tmp.wav'

        target_se, _ = se_extractor.get_se(audio_path, self.tone_color_converter, target_dir=self.processed_dir, vad=False)
        texts = {
            'EN_NEWEST': text
        }

        speed = 1
        for language, text in texts.items():
            model = TTS(language=language, device=self.device)
            speaker_ids = model.hps.data.spk2id

            for speaker_key in speaker_ids.keys():
                speaker_id = speaker_ids[speaker_key]
                speaker_key = speaker_key.lower().replace('_', '-')
                
                source_se = torch.load(f'src/checkpoints_v2/base_speakers/ses/{speaker_key}.pth', map_location=self.device)
                model.tts_to_file(text, speaker_id, src_path, speed=speed)
                save_path = f'{self.output_dir}/output_v2_{speaker_key}.wav'

                # Run the tone color converter
                encode_message = "@MyShell"
                self.tone_color_converter.convert(
                    audio_src_path=src_path, 
                    src_se=source_se, 
                    tgt_se=target_se, 
                    output_path=save_path,
                    message=encode_message)
    @staticmethod
    async def __save_input_file_to_storage(file: UploadFile, save_dir: str) -> str:
        _, ext = os.path.splitext(file.filename)
        file_id = str(uuid.uuid4())
        file_name = f'{file_id}{ext}'
        file_path = os.path.join(save_dir, file_name)

        os.makedirs(save_dir, exist_ok=True)
        
        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
        return file_path
