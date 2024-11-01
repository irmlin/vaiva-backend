import os
import shutil

import torch

from src.external.sadtalker.src.facerender.animate import AnimateFromCoeff
from src.external.sadtalker.src.generate_batch import get_data
from src.external.sadtalker.src.generate_facerender_batch import get_facerender_data
from src.external.sadtalker.src.test_audio2coeff import Audio2Coeff
from src.external.sadtalker.src.utils.init_path import init_path
from src.external.sadtalker.src.utils.preprocess import CropAndExtract


class Inference:
    def __init__(self):
        # Default args
        self.result_dir = os.path.join('src', 'external', 'sadtalker', 'results')
        self.pose_style = 0
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.batch_size = 2
        self.input_yaw_list = None
        self.input_pitch_list = None
        self.input_roll_list = None
        self.ref_eyeblink = None
        self.ref_pose = None
        self.checkpoint_dir = os.path.join('src', 'external', 'sadtalker', 'checkpoints')
        self.config_dir = os.path.join('src', 'external', 'sadtalker', 'src', 'config')
        self.size = 256
        self.old_version = False
        self.preprocess = 'crop'
        self.still = False
        self.expression_scale = 1.0
        self.enhancer = 'gfpgan'
        self.background_enhancer = None
        self.verbose = False

        # Load models
        sadtalker_paths = init_path(self.checkpoint_dir, self.config_dir, self.size, self.old_version, self.preprocess)
        self.preprocess_model = CropAndExtract(sadtalker_paths, self.device)
        self.audio_to_coeff = Audio2Coeff(sadtalker_paths, self.device)
        self.animate_from_coeff = AnimateFromCoeff(sadtalker_paths, self.device)

    def run(self,
            source_image: str,
            driven_audio: str,
            output_video_name: str) -> str:
        pic_path = source_image
        audio_path = driven_audio
        save_dir = os.path.join(self.result_dir, os.path.splitext(output_video_name)[0])
        os.makedirs(save_dir, exist_ok=True)

        # crop image and extract 3dmm from image
        first_frame_dir = os.path.join(save_dir, 'first_frame_dir')
        os.makedirs(first_frame_dir, exist_ok=True)
        print('3DMM Extraction for source image')
        first_coeff_path, crop_pic_path, crop_info = self.preprocess_model.generate(pic_path, first_frame_dir,
                                                                                    self.preprocess,
                                                                                    source_image_flag=True,
                                                                                    pic_size=self.size)
        if first_coeff_path is None:
            print("Can't get the coeffs of the input")
            return

        if self.ref_eyeblink is not None:
            ref_eyeblink_videoname = os.path.splitext(os.path.split(self.ref_eyeblink)[-1])[0]
            ref_eyeblink_frame_dir = os.path.join(save_dir, ref_eyeblink_videoname)
            os.makedirs(ref_eyeblink_frame_dir, exist_ok=True)
            print('3DMM Extraction for the reference video providing eye blinking')
            ref_eyeblink_coeff_path, _, _ = self.preprocess_model.generate(self.ref_eyeblink, ref_eyeblink_frame_dir,
                                                                           self.preprocess, source_image_flag=False)
        else:
            ref_eyeblink_coeff_path = None

        if self.ref_pose is not None:
            if self.ref_pose == self.ref_eyeblink:
                ref_pose_coeff_path = ref_eyeblink_coeff_path
            else:
                ref_pose_videoname = os.path.splitext(os.path.split(self.ref_pose)[-1])[0]
                ref_pose_frame_dir = os.path.join(save_dir, ref_pose_videoname)
                os.makedirs(ref_pose_frame_dir, exist_ok=True)
                print('3DMM Extraction for the reference video providing pose')
                ref_pose_coeff_path, _, _ = self.preprocess_model.generate(self.ref_pose, ref_pose_frame_dir,
                                                                           self.preprocess,
                                                                           source_image_flag=False)
        else:
            ref_pose_coeff_path = None

        # audio2ceoff
        batch = get_data(first_coeff_path, audio_path, self.device, ref_eyeblink_coeff_path, still=self.still)
        coeff_path = self.audio_to_coeff.generate(batch, save_dir, self.pose_style, ref_pose_coeff_path)


        # coeff2video
        data = get_facerender_data(coeff_path, crop_pic_path, first_coeff_path, audio_path,
                                   self.batch_size, self.input_yaw_list, self.input_pitch_list, self.input_roll_list,
                                   expression_scale=self.expression_scale, still_mode=self.still,
                                   preprocess=self.preprocess, size=self.size)

        result = self.animate_from_coeff.generate(data, save_dir, pic_path, crop_info,
                                                  enhancer=self.enhancer, background_enhancer=self.background_enhancer,
                                                  preprocess=self.preprocess, img_size=self.size)

        out_path = os.path.join(os.path.dirname(save_dir), f'{output_video_name}')
        shutil.move(result, out_path)
        print('The generated video:', out_path)

        if not self.verbose:
            shutil.rmtree(save_dir)

        return out_path