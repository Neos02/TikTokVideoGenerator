from utils.text_cleaner import censor, html_to_text, remove_tldr
from tts.GTTS import GTTS
from VideoBuilder import VideoBuilder
from dotenv import dotenv_values
from reddit.subreddit import get_subreddit_thread
from utils.timestamps import get_timestamps


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
    story = censor(remove_tldr(html_to_text(thread.selftext_html)))

    tts = GTTS()

    title_audio = tts.run(title, name='title')
    story_audio = tts.run(story, name='story')

    title_caption = get_timestamps(title_audio)
    captions = get_timestamps(story_audio)
    captions.insert(0, {'text': title, 'start_time': title_caption[0]['start_time'], 'end_time': title_caption[-1]['end_time']})

    video_builder = VideoBuilder(
        title=title,
        story=story,
        title_audio=title_audio,
        story_audio=story_audio,
        captions=captions,
        background_path='background_videos/Minecraft_Parkour.mp4'
    )

    video_builder.get_video()
