from utils.text_cleaner import censor, html_to_text
from TTS import TTS
from VideoBuilder import VideoBuilder
from dotenv import dotenv_values
from reddit.subreddit import get_subreddit_thread


env = dotenv_values('.env')

subreddits = [
    'AmItheAsshole',
    'confessions',
    'confession',
    'tifu',
    'JUSTNOMIL',
    'TalesFromTechSupport',
    'TalesFromRetail',
    'creepyencounters'
]


if __name__ == '__main__':
    thread = get_subreddit_thread('tifu')

    title = censor(thread.title)
    body = censor(html_to_text(thread.selftext_html))

    tts = TTS()

    title_data = tts.convert(title, name='title.mp3')
    audio_data = tts.convert(body, max_chars=25)
    audio_data.insert(0, title_data[0])

    video_builder = VideoBuilder(audio_data=audio_data, audio_directory='audio_out',
                                 background_path='background_videos/Minecraft_Parkour.mp4')

    video_builder.get_video()
