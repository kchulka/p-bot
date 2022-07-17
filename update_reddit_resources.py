
import sys
import re

import asyncpraw
from ruamel.yaml import YAML
import ruamel.yaml as kkt

yaml = YAML()
yaml.enc = 'utf-8'

config = yaml.load(open('config/config.yml', 'r'))

reddit = asyncpraw.Reddit(
    client_id = config.get("reddit_login").get("client_id"),
    client_secret = config.get("reddit_login").get("client_secret"),
    user_agent = config.get("reddit_login").get("user_agent"),
    check_for_async=False
)

""" ----- reddit save stuff ----- """

async def save_images_from_reddit(subreddit, filename, max_posts):

    sub = await reddit.subreddit(subreddit)
    hot = sub.hot(limit=max_posts)

    quantity = 0
    new_file = yaml.load(f"""\
                        subreddit: {subreddit}
                        quantity: {quantity}
                        """)

    async for submission in hot:
        check = r"(?:http\:|https\:)?\/\/.*\.(?:png|jpg)"
        if re.search(check, submission.url, re.IGNORECASE) != None:
            quantity += 1
            new_file[quantity] = {}
            new_file[quantity]['id'] = f"{submission}"
            new_file[quantity]['url'] = f"{submission.url}"
            new_file[quantity]['title'] = f"{submission.title}"
            new_file[quantity]['author'] = f"{submission.author}"
            new_file[quantity]['score'] = f"{submission.score}"

    new_file["quantity"] = quantity

    with open(f"resources/{filename}.yml", 'w', encoding='utf-8') as file:
        yaml.dump(new_file, stream=file)