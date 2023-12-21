import praw
from praw.exceptions import PRAWException
from dotenv import dotenv_values

env = dotenv_values('.env')


def get_subreddit_thread(subreddit: str):
    """
    Get a thread from the specified subreddit
    :param subreddit: name of the subreddit to pull from
    :return: one of the top threads in the subreddit
    """

    # Remove the r/ from a subreddit if it's there
    if subreddit.casefold().startswith('r/'):
        subreddit = subreddit[2:]

    print('Connecting to Reddit')

    try:
        reddit = praw.Reddit(
            client_id=env['REDDIT_CLIENT_ID'],
            client_secret=env['REDDIT_CLIENT_SECRET'],
            user_agent='Retreiving Reddit Data'
        )

        print('Retrieving post')

        # TODO: Store all posted threads and do not allow repeats
        thread = list(filter(lambda x: not x.over_18 and not x.stickied, reddit.subreddit(subreddit).hot(limit=50)))[0]

        print(f'Thread will be "{thread.title}" - {thread.url}')

        return thread
    except PRAWException:
        print('Something went wrong...')

    return None
