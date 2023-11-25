import praw
import random
from dotenv import dotenv_values

secrets = dotenv_values(".env")


def get_titles():
    """
    Appends 33 reddit titles from 3 different subreddits into a list.
    Returns a scrambled version of the list.
    """
    reddit = praw.Reddit(client_id = secrets["CLIENT_ID"],
                        client_secret = secrets["CLIENT_SECRET"],
                        uesrname = secrets["USERNAME"],
                        password = secrets["PASSWORD"],
                        user_agent = secrets["USER_AGENT"])

    neutral = reddit.subreddit('IsraelPalestine')
    palestine = reddit.subreddit('Israel')
    israel = reddit.subreddit('Palestine')

    neutral_posts = neutral.new(limit = 33)
    palestine_posts = palestine.new(limit = 33)
    israel_posts = israel.new(limit = 33)

    neutral_titles = [post.title for post in neutral_posts]
    palestine_titles = [post.title for post in palestine_posts]
    israel_titles = [post.title for post in israel_posts]

    all_titles = neutral_titles + palestine_titles + israel_titles

    random.shuffle(all_titles)

    return all_titles
