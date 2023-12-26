import os
import shutil

from utils.text_cleaner import sanitize_text
from gtts import gTTS


class GTTS:

    def __init__(self, output_directory: str = './temp'):
        self.format = 'mp3'
        self.output_directory = output_directory

        self.create_output_directory()

    def create_output_directory(self):
        """
        Create the directory to output the audio files and
        delete any previously existing files at that location
        """

        if os.path.exists(self.output_directory):
            shutil.rmtree(self.output_directory)

        os.makedirs(self.output_directory)

    def run(self, text: str, name: str = None) -> str:
        """
        Converts text to audio using gTTS
        :param text: text to convert
        :param name: The name to give to the output file. If not specified,
                     the file will be named 'output.mp3'
        :return: The path to the file
        """
        print('Preparing text for TTS')

        sanitized = sanitize_text(text)

        print('Processing TTS')

        if not name:
            print('No filename specified. Defaulting to "output"')
            name = 'output'

        path = f'{self.output_directory}/{name}.{self.format}'
        gTTS(text=sanitized, lang='en', slow=False).save(path)

        return path
