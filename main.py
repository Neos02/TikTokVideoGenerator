import praw
from random import randint
from HTMLFilter import html_to_text
from Censor import censor
from TTS import TTS
from VideoBuilder import VideoBuilder
from dotenv import dotenv_values


env = dotenv_values('.env')


posts_per_day = 1
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
reddit = praw.Reddit(
    client_id=env['REDDIT_CLIENT_ID'],
    client_secret=env['REDDIT_CLIENT_SECRET'],
    user_agent='praw'
)


if __name__ == '__main__':
    daily_subreddits = [subreddits[randint(0, len(subreddits) - 1)] for i in range(posts_per_day)]
    posted = []
    tts = TTS()

    for subreddit in daily_subreddits:
        # Get 50 posts then filter so they are not NSFW or pinned
        posts = list(filter(lambda x: not x.over_18 and not x.stickied, reddit.subreddit(subreddit).hot(limit=20)))

        for post in posts:
            if post not in posted:
                posted.append(post)

                title = censor(post.title)
                body = censor(html_to_text(post.selftext_html))

                title_data = tts.convert(title, name='title.mp3')
                print(title, post.url)
                audio_data = tts.convert(body, max_chars=25)
                audio_data.insert(0, title_data[0])

                video_builder = VideoBuilder(audio_data=audio_data, audio_directory='audio_out',
                                             background_path='background_videos/Minecraft_Parkour.mp4')

                video_builder.get_video()
                break
