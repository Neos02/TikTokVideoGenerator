import cv2
import ffmpeg
from mutagen.mp4 import MP4
from moviepy.editor import *
from random import random


class VideoBuilder:

    def __init__(self, audio_data, audio_directory, background_path):
        self.width = 1080
        self.height = 1920
        self.audio_data = audio_data
        self.audio_directory = audio_directory
        self.background_path = self.crop_background(background_path)

    def get_video_duration(self):
        duration = 0

        for data in self.audio_data:
            duration += data['duration']

        return duration

    def get_video_dimensions(self, path):
        video = cv2.VideoCapture(path)

        return video.get(cv2.CAP_PROP_FRAME_WIDTH), video.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def crop_background(self, path):
        filename, filetype = path.split(".")
        output_path = f'{filename}_cropped.{filetype}'

        if os.path.exists(output_path):
            return output_path

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
        clip_start_time = random() * (MP4(self.background_path.replace('_cropped', '')).info.length - clip_duration)

        background_clip = VideoFileClip(self.background_path, target_resolution=(1920, 1080))\
            .subclip(clip_start_time, clip_start_time + clip_duration)
        text_clips = []
        audio_clips = []

        for i, data in enumerate(self.audio_data):
            text_clips.append(
                TextClip(
                    txt=data['text'],
                    fontsize=70,
                    font='Lilita-One',
                    color='white',
                    size=(int(self.width * .9), self.height),
                    method='caption',
                    transparent=True
                )
                .set_position('center')
                .set_duration(data['duration'])
            )
            print(data['duration'])
            audio_clips.append(ffmpeg.input(data['filename']))

        ffmpeg\
            .concat(*audio_clips, v=0, a=1)\
            .output('output/audio.m4a')\
            .overwrite_output()\
            .run()

        audio = AudioFileClip('output/audio.m4a')
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
