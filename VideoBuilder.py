import cv2
import ffmpeg

from tqdm import tqdm
from moviepy.editor import *
from random import random


class VideoBuilder:

    def __init__(self, title: str, story: str, title_audio: str, story_audio: str, captions: list[dict], background_path: str):
        self.width = 1080
        self.height = 1920
        self.title = title
        self.story = story
        self.title_audio = title_audio
        self.story_audio = story_audio
        self.captions = captions
        self.background_path = self.crop_background(background_path)

    def get_video_duration(self):
        print('Calculating video duration')

        return float(ffmpeg.probe(self.title_audio)['format']['duration']) + float(ffmpeg.probe(self.story_audio)['format']['duration'])

    def get_video_dimensions(self, path):
        video = cv2.VideoCapture(path)

        return video.get(cv2.CAP_PROP_FRAME_WIDTH), video.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def crop_background(self, path):
        filename, filetype = path.split(".")
        output_path = f'{filename}_cropped.{filetype}'

        if os.path.exists(output_path):
            return output_path

        print('Cropping background video')

        aspect_ratio = self.width / self.height
        background_width, background_height = self.get_video_dimensions(path)
        new_width = int(background_height * aspect_ratio)

        ffmpeg \
            .input(path) \
            .filter('crop', new_width, background_height, (background_width - new_width) // 2, 0) \
            .output(output_path) \
            .overwrite_output() \
            .run()

        return output_path

    def get_video(self):
        clip_duration = self.get_video_duration()
        background_duration = float(ffmpeg.probe(self.background_path)['format']['duration'])
        clip_start_time = random() * (background_duration - clip_duration)

        background_clip = VideoFileClip(self.background_path, target_resolution=(1920, 1080))\
            .subclip(clip_start_time, clip_start_time + clip_duration)
        text_clips = []

        for caption in tqdm(self.captions, desc='Creating captions'):
            text_clips.append(
                TextClip(
                    txt=caption['text'],
                    fontsize=90,
                    font='Lilita-One',
                    color='white',
                    size=(int(self.width * .9), self.height),
                    stroke_width=5,
                    stroke_color='black',
                    method='caption',
                    transparent=True
                )
                .set_position('center')
                .set_duration(caption['end_time'] - caption['start_time'])
            )

        print('Finalizing audio')

        ffmpeg\
            .concat(ffmpeg.input(self.title_audio), ffmpeg.input(self.story_audio), v=0, a=1)\
            .output('output/audio.m4a')\
            .overwrite_output()\
            .run(quiet=True)

        audio = AudioFileClip('./temp/audio.m4a')
        text = concatenate_videoclips(text_clips)
        video = CompositeVideoClip(size=(self.width, self.height), use_bgclip=True, clips=[background_clip, text.set_position('center')]).set_audio(audio)

        video.write_videofile(
            'output/output.mp4',
            audio=True,
            # temp_audiofile='output/audio.m4a',
            # remove_temp=True,
            audio_codec='aac',
            ffmpeg_params=None,
            verbose=True,
            threads=None,
            preset='medium',
            fps=None,
            audio_nbytes=4,
            audio_bitrate=None,
            audio_bufsize=2000,
            codec='libx264'
        )
