import os
import shutil
import ffmpeg

from mutagen.mp3 import MP3
from gtts import gTTS
from pydub import AudioSegment


class TTS:

    def __init__(self, output_directory='./audio_out'):
        self.output_directory = output_directory

        self.create_output_directory()

    def create_output_directory(self):
        if os.path.exists(self.output_directory):
            shutil.rmtree(self.output_directory)

        os.makedirs(self.output_directory)

    def convert(self, text, max_chars=None, name=None):
        length = len(text)

        if max_chars is None:
            max_chars = length

        index = 0
        segment_start = 0
        segment_end = max_chars
        output = []

        while segment_start == 0 or segment_end < length:
            prev_end = segment_end
            segment_end = length if segment_start + max_chars >= length else text.rindex(' ', segment_start, min(segment_start + max_chars, length))

            if segment_end == prev_end:
                segment_end = length

            segment_text = text[segment_start:segment_end].strip()

            filename = f'{self.output_directory}/{name if name is not None else index}.mp3'
            gTTS(text=segment_text).save(filename)
            AudioSegment.from_mp3(filename)\
                .speedup(playback_speed=1.2)\
                .export(filename, format='mp3')
            duration = MP3(filename).info.length

            output.append({'filename': filename, 'text': segment_text, 'duration': duration})
            segment_start = segment_end
            index += 1

        return output
