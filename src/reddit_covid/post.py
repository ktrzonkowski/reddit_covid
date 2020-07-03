import praw
from . import constants
from . import praw_config


def post(stateConfig):
    reddit = praw.Reddit(**praw_config.prawConf)

    for subreddit in stateConfig.subreddits:
        sr = reddit.subreddit(subreddit)
        sr.submit_image(
            title=f"Testing: {stateConfig['name']} COVID-19 Daily New Positive",
            image_path=f"./fig-{stateConfig['name'].replace(' ', '_')}"
        )
