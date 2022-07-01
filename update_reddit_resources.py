
""" ----- this file saves posts from reddit to .yml files, so the main.py can use them ------ """

import praw

import re

import yaml
from yaml import Loader

import time

from datetime import datetime

""" ----- settings stuff ----- """

class settings:
    def __init__(self):
        self.file = open('resources/settings.yml', 'r')
        self.data = yaml.load(self.file, Loader=Loader)
settings = settings()

debug = settings.data.get("debug-mode")
if debug >= 1:
    print("debug mode activated \n")

""" ----- reddet ----- """

reddit = praw.Reddit(
    client_id = settings.data.get("reddit_login").get("client_id"),
    client_secret = settings.data.get("reddit_login").get("client_secret"),
    user_agent = settings.data.get("reddit_login").get("user_agent")
)

""" ----- reddit save stuff ----- """

class saved_reddit:
    def __init__(self, saved_reddit):
        self.file = open(f'resources/reddit_saved_{saved_reddit}.yml', 'r')
        self.data = yaml.load(self.file, Loader=Loader)


def save_from_reddit():
    for max_subreddits in range (1, 1+settings.data.get('subreddits').get("max")):
        if debug >= 1:
            print(f" creating file for subreddit num: {max_subreddits} ")

        subreddit = settings.data.get('subreddits').get(max_subreddits).get('name')

        sub = reddit.subreddit(subreddit)
        hot = sub.hot(limit=settings.data.get('subreddits').get("max_posts"))

        quantity = 0
        dict_ = {}

        for submission in hot:

            check = r"(?:http\:|https\:)?\/\/.*\.(?:png|jpg)"
            matches = re.search(check, submission.url, re.IGNORECASE)

            if debug >= 2:
                print(f" random subreddit match: {matches} ")
            if matches != None:
                quantity += 1
                dict1 = {quantity: {'id': f'{submission}', 'url': f'{submission.url}', 'title': f'{submission.title}', 'author': f'{submission.author}', 'score': submission.score}}
                if debug >= 2:
                    print(f" submission: {submission} ")
                dict_.update(dict1)
            else:
                if debug >= 2:
                    print(f" random subreddit match: {matches} ")

        current_time = {"time": datetime.now()}
        dict_.update(current_time)

        dict2 = {"quantity": quantity}
        dict_.update(dict2)
        if debug >= 1:
            print(f"  submissions from sub {max_subreddits} that went thru: {quantity}")
        with open(f'resources/reddit_saved_{max_subreddits}.yml', 'w') as yaml_file:
            yaml.dump(dict_, yaml_file, default_flow_style=False)
        print(f"  subreddit num: {max_subreddits} with name: {subreddit} hase been downloaded")


save_from_reddit()

time.sleep(3)
exit("\nFinished saving reddit posts")