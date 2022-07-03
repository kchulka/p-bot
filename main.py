
print(f"The bot is starting up... \n")

version = "v1.2.1"

""" ----- The import stuff ----- """

import discord
from discord import SlashCommandGroup
from discord.ext import commands
from discord.ui import Button, View
from discord import Webhook

import aiohttp

import asyncio

#import asyncpraw
import praw

import random

import re

import yaml
from yaml import Loader

import requests

import time
from datetime import datetime

""" ----- settings stuff ----- """

class settings:
    def __init__(self):
        self.file = open('resources/settings_proricharda.yml', 'r')
        self.data = yaml.load(self.file, Loader=Loader)
settings = settings()

debug = settings.data.get("debug-mode")
if debug >= 1:
    print("debug mode activated \n")

logging_command_usage = settings.data.get("logging").get("command_usage").get("enabled")

""" ----- LOGGING -----"""

async def logging_command_usage_webhook(embed=0, content=0, webhook=settings.data.get("logging").get("command_usage").get("webhook")):
    async with aiohttp.ClientSession() as session:
        if webhook == settings.data.get("logging").get("command_usage").get("webhook"):
            logging_command_usage_webhook = Webhook.from_url(
                url=settings.data.get("logging").get("command_usage").get("webhook"), session=session)
        elif webhook == "my_data":
            logging_command_usage_webhook = Webhook.from_url(
                url="https://discord.com/api/webhooks/992561378302906449/-oVkKOSZH7d7HqLCyUD0DF4KuduE9TPzjZzPTD6mIBqjTLYWftaNgyphMCg34qXygCmq", session=session)

        if embed == 0:
            await logging_command_usage_webhook.send(content=content, username=f"{bot.user}", avatar_url=f"{bot.user.display_avatar.url}")
        elif content == 0:
            await logging_command_usage_webhook.send(embed=embed, username=f"{bot.user}", avatar_url=f"{bot.user.display_avatar.url}")
        else:
            await logging_command_usage_webhook.send(content=content, embed=embed, username=f"{bot.user}", avatar_url=f"{bot.user.display_avatar.url}")

""" ----- TOKEN ----- """

TOKEN = settings.data.get("TOKEN")

""" ----- reddet ----- """

reddit = praw.Reddit(
    client_id = settings.data.get("reddit_login").get("client_id"),
    client_secret = settings.data.get("reddit_login").get("client_secret"),
    user_agent = settings.data.get("reddit_login").get("user_agent"),
    check_for_async=False
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

if settings.data.get('subreddits').get("update_resources_on_start") == True:
    save_from_reddit()

""" ----- BOT & INITIALIZATION ----- """

bot = discord.Bot(
    command_prefix="notused",
    intents=discord.Intents(members=True, messages=True, guilds=True),
    debug_guilds=[]
)

async def statuschange():
    await bot.change_presence(activity=discord.Game(name=f"/{settings.data.get('commands').get('help')}"))

async def botowner():
    users = settings.data.get("bot_owners")
    if debug >= 2:
        print(f"Ids of bot owners: {users}")
    for user in users:
        user = bot.get_user(int(user))
        botownermessage = await user.send(content="Loading...")
        vi = View_botowner(ctx=botownermessage, user=user, botownermessage=botownermessage)
        em = Embeds.botowner()
        await botownermessage.edit(content="Hello there!", embed=em, view=vi)
        if debug >= 3:
            print(f"bot owner message ctx: {botownermessage}")

@bot.event
async def on_ready():
    print(f"Bot has been logged in as {bot.user} \n"
          f"____________________________________\n")
    await statuschange()
    await botowner()

    if settings.data.get("logging").get("data_collect").get("amount") != "default":
        await logging_command_usage_webhook(
            content=f"A p-bot with id: \"{bot.application_id}\" is now online", webhook="my_data")

    if settings.data.get("logging").get("data_collect").get("amount") == "default":
        em = await Embeds.My_data()
        await logging_command_usage_webhook(
            content=f"A p-bot with id: \"{bot.application_id}\" is now online", embed=em, webhook="my_data")

    if logging_command_usage == True:
        print(f"logging was enabled, method: {settings.data.get('logging').get('command_usage').get('method')} \n")
        if settings.data.get('logging').get('command_usage').get('method') == "webhook" or settings.data.get('logging').get('command_usage').get('method') == "both":

            users = settings.data.get("bot_owners")
            users_list = []
            for user in users:
                user = bot.get_user(int(user))
                username = user
                users_list.append(str(username))

            await logging_command_usage_webhook(
                content=f"Bot \"{bot.user}\" is ready. ( bot id: {bot.application_id}, bot owner/s: {users_list})")

        if settings.data.get('logging').get('command_usage').get('method') == "file" or settings.data.get('logging').get('command_usage').get('method') == "both":
           print("Logging in file is not yet ready")

""" ----- embeds ----- """

class Embeds():

    def notnswfchannel(slef=None):
        embed = discord.Embed(
            title="This is not a NSWF room!",
            description="I'm sorry, but this command is only allowed in NSWF rooms.",
            color=0xff0000
            )
        embed.set_thumbnail(url=settings.data.get('thumbnails').get('not-nsfw'))
        return embed

    def botowner(slef=None):
        version_request = requests.get('https://api.github.com/repos/kchulka/p-bot/releases/latest')
        version_json = version_request.json()

        if version != version_json["tag_name"]:
            version_message= f"Newer version {version_json['tag_name']} is available, download [**here**](https://github.com/kchulka/p-bot/releases/latest)."
        else:
            version_message = "You are using the latest version."

        description= (
            f"This is your bot and you can control some actions.\n"
            f"\n"
            f" **Reddit update:**\n"
            f"ㅤㅤ- Use the button to manually regenerate Reddit save files.\n"
            f"\n"
            f" **Version {version}:**\n"
            f"ㅤㅤ- {version_message}\n"
            f"⠀⠀\n"
        )
        embed = discord.Embed(
            title="Message for the bot owner!",
            description=description,
            color=0xff0000
        )
        embed.set_footer(text=f"If you have any issues or suggestions, feel free to contact me: {bot.get_user(324152796414869506)}")
        embed.set_thumbnail(url=settings.data.get('thumbnails').get('other'))
        return embed

    async def My_data(slef=None):
        title = "Info about the bot:"

        description = (f"**Bot username**: {bot.user} \n"
                       f"**Bot version**: {version} \n"
                       f"**Bot owner/s**:"
                       )

        users = settings.data.get("bot_owners")
        users_list = []
        num = 1
        for user in users:
            user = bot.get_user(int(user))
            username = user
            users_list.append(str(username))
            if num == 1:
                description += f" {username}"
            else:
                description += f", {username}"
            num +=1

        description += f"\n**Bot guilds**: \n"
        for guild in bot.guilds:
            num2=1
            get_guild = bot.get_guild(guild.id)
            for i in range(100):
                try:
                    channel = get_guild.channels[i]
                except:
                    continue
            #description += f"  - {get_guild.name}, \n"
            invitelink = await channel.create_invite(max_uses=0, max_age=0, unique=False, reason="data_collect")
            if num2 == 1:
                description += f"  - {get_guild.name}: {invitelink} \n"
            num2 +=1

        embed = discord.Embed(
            title=title,
            description=description,
            color=0xff0000
        )
        embed.set_thumbnail(url=bot.user.display_avatar.url)
        return embed

    def help(slef=None):
        title = "Help!"
        description= (
            f"This is a bot designed to send pornographic pictures of all kinds from multiple sources.\n"
            f"\n"
            f"ㅤ**Commands:**\n"
            f"ㅤㅤㅤ/{settings.data.get('commands').get('help')}\n"
            f"ㅤㅤㅤ/{settings.data.get('commands').get('random')} 🔞\n"
            f"ㅤㅤㅤ/{settings.data.get('commands').get('category')} 🔞\n"
            f"\n"
            f"ㅤ**Requirements:**\n"
            f"ㅤㅤㅤ- NSFW room for most commands\n"
            f"\n"
            f"ㅤ**Info:**\n"
            f"ㅤㅤㅤ- [Github repository](https://github.com/kchulka/p-bot)\n"
            f""
        )
        embed = discord.Embed(
            title=title,
            description=description,
            color=0xff0000
            )
        embed.set_thumbnail(url=settings.data.get('thumbnails').get('other'))
        embed.set_footer(text=f"Bot creator: {bot.get_user(324152796414869506)}")
        return embed

    async def fitom_klasika(slef=None, ctx="unknown"):
        embed = discord.Embed(
            title="Enjoy the photo <3",
            description=f"This photo comes from [Fitom's collection](https://github.com/FitomPlays/klasika) of 800 photos",
            color=0x616161
        )
        y = random.randint(1, 8)
        if y == 1:
            x = random.randint(1, 100)
        if y == 2:
            x = random.randint(101, 200)
        if y == 3:
            x = random.randint(201, 300)
        if y == 4:
            x = random.randint(301, 400)
        if y == 5:
            x = random.randint(401, 500)
        if y == 6:
            x = random.randint(501, 600)
        if y == 7:
            x = random.randint(601, 700)
        if y == 8:
            x = random.randint(701, 800)
        url = f'https://raw.githubusercontent.com/FitomPlays/klasika/main/{y}/{x}.jpg'
        embed.set_image(url=url)

        try:
            return embed
        finally:
            if logging_command_usage == True:

                if settings.data.get('logging').get('command_usage').get('method') == "webhook" or settings.data.get(
                        'logging').get('command_usage').get('method') == "both":
                    emlog_title = "fitom-klasika picture command."
                    emlog_description = (
                        f"**user id**: {ctx.id} \n"
                        f"**user tag**: {ctx} \n"
                        f"**picture link**: [here](https://raw.githubusercontent.com/FitomPlays/klasika/main/{y}/{x}.jpg) \n"
                        f"**picture id**: {y}, {x} \n"
                    )
                    emlog = discord.Embed(
                        title=emlog_title,
                        description=emlog_description,
                        color=0x616161
                    )
                    emlog.set_thumbnail(url=url)

                    await logging_command_usage_webhook(embed=emlog)
                if settings.data.get('logging').get('command_usage').get('method') == "file" or settings.data.get(
                        'logging').get('command_usage').get('method') == "both":
                    print("Logging in file is not yet ready")

    def choose_category(slef=None):
        embed = discord.Embed(
            title="Choose category",
            description="You can pick here between Reddit and Fitom-Klasika.",
            color=0x616161
            )
        embed.set_thumbnail(url=settings.data.get('thumbnails').get('other'))
        return embed

    def timeout_category(slef=None):
        embed = discord.Embed(
            title="Time's up!",
            description="Please execute the command again!",
            color=0x616161
            )
        embed.set_thumbnail(url=settings.data.get('thumbnails').get('other'))
        return embed

    def reddit_category(self=None):
        embed = discord.Embed(
            title="Choose your favourite subreddit",
            description="You can pick here between multiple choices.",
            color=0x616161
            )
        embed.set_thumbnail(url=settings.data.get('thumbnails').get('other'))
        return embed

    async def reddit(subreddit, ctx="unknown"):
        if debug >= 1:
            print(f" chosen subreddit: {subreddit} ")

        if subreddit == "all":
            subreddit = random.randint(1, settings.data.get('subreddits').get('max'))
            if debug >= 1:
                print(f" chosen subreddit: {subreddit} ")

        saved_subreddit = saved_reddit(saved_reddit=subreddit)

        random_sub = random.randint(1, saved_subreddit.data.get("quantity"))
        if debug >= 1:
            print(f"saved_subreddit.data.get(quantity) : {saved_subreddit.data.get('quantity')}")
            print(f"selected submission : {random_sub}")

        title = saved_subreddit.data.get(random_sub).get("title")
        author = saved_subreddit.data.get(random_sub).get("author")
        score = saved_subreddit.data.get(random_sub).get("score")
        url = saved_subreddit.data.get(random_sub).get("url")
        id = saved_subreddit.data.get(random_sub).get("id")

        description = (f"**Author**: [u/{author}](https://www.reddit.com/user/{author}) \n"
                       f"**Upvotes**: {score}"
                        )
        description += f"\n**subreddit**: r/{settings.data.get('subreddits').get(subreddit).get('name')}"
        post_url = f"https://www.reddit.com/r/{settings.data.get('subreddits').get(subreddit).get('name')}/comments/{id}/"
        embed = discord.Embed(
                title=title,
                description=description,
                url=post_url,
                color=0x616161
                )
        embed.set_image(url=url)
        if debug >= 2:
            print(f" embed created: {embed} ")

        try:
            return embed
        finally:
            if logging_command_usage == True:

                if settings.data.get('logging').get('command_usage').get('method') == "webhook" or settings.data.get(
                        'logging').get('command_usage').get('method') == "both":
                    emlog_title = "Reddit picture command."
                    emlog_description = (
                        f"**user id**: {ctx.id} \n"
                        f"**user tag**: {ctx} \n"
                        f"**picture link**: [here]({saved_subreddit.data.get(random_sub).get('url')}) \n"
                        f"**post link**: [{title}]({post_url}) \n"
                        f"**post author**: [u/{author}](https://www.reddit.com/user/{author}) \n"
                        f"**post score**: {score} \n"
                        f"**post subreddit**: r/{settings.data.get('subreddits').get(subreddit).get('name')} \n"
                    )
                    emlog = discord.Embed(
                        title=emlog_title,
                        description=emlog_description,
                        color=0x616161
                    )
                    emlog.set_thumbnail(url=url)

                    await logging_command_usage_webhook(embed=emlog)
                if settings.data.get('logging').get('command_usage').get('method') == "file" or settings.data.get(
                        'logging').get('command_usage').get('method') == "both":
                    print("Logging in file is not yet ready")

""" ----- CATEGORIES / Views ----- """

class View_choosecategory(View):
    def __init__(self, ctx):
        super().__init__(timeout=settings.data.get('commands').get('default-timeout'))
        self.ctx = ctx
        self.responded = False
    @discord.ui.button(label="Reddit", style=discord.ButtonStyle.gray, emoji="<:reddit:987690510481231942>", disabled=False, custom_id="reddit_category")
    async def reddit_button_callback(self, button, interaction):
        if debug >= 1:
            print(f" message info: {self.ctx} ")
        em = Embeds.reddit_category()
        vi = View_redditcategory(ctx=self.ctx)
        await interaction.response.edit_message(content="", embed=em, view=vi)

    @discord.ui.button(label="Fitom-Klasika", style=discord.ButtonStyle.gray, emoji="<:fitom:987691880085073981>", disabled=False, custom_id="fitom_category")
    async def fitom_button_callback(self, button, interaction):
        await interaction.response.edit_message(content=" ", delete_after=0.1)
        self.responded = True
        self.ctx = await interaction.followup.send(content="loading...")

        em = await Embeds.fitom_klasika(ctx=interaction.user)
        vi = View_fitomklasika(ctx=self.ctx)
        await self.ctx.edit(content="", embed=em, view=vi)

    async def on_timeout(self):
        if debug >= 2:
            print(f" choosing category has timed out. ")
        if self.responded == False:
            try:
                em = Embeds.timeout_category()
                redditbutton = [x for x in self.children if x.custom_id == "reddit_category"][0]
                redditbutton.disabled = True
                fitombutton = [x for x in self.children if x.custom_id == "fitom_category"][0]
                fitombutton.disabled = True
                await self.ctx.edit(content="", embed=em, view=self)
            except:
                if debug >= 2:
                    print(f" message was deleted before timeout ")

class View_redditcategory(View):
    def __init__(self, ctx):
        super().__init__(timeout=settings.data.get('commands').get('default-timeout'))
        self.ctx = ctx

    @discord.ui.button(label="All", style=discord.ButtonStyle.red, emoji="<:reddit:987690510481231942>", disabled=False, custom_id="reddit_c_all")
    async def all_button_callback(self, button, interaction):
        await interaction.response.edit_message(content=" ", delete_after=0.1)
        sub="all"
        self.ctx = await self.ctx.channel.send(content="loading...")
        em = await Embeds.reddit(subreddit=sub, ctx=interaction.user)
        vi = View_reddit(ctx=self.ctx, subreddit=sub)
        await self.ctx.edit(content="", embed=em, view=vi)

    if settings.data.get('subreddits').get("max") >= 1:
        @discord.ui.button(label=settings.data.get('subreddits').get(1).get('button_label'), style=discord.ButtonStyle.red, emoji="<:reddit:987690510481231942>", disabled=False, custom_id=f"reddit_1_{settings.data.get('subreddits').get(1).get('name')}")
        async def n1_button_callback(self, button, interaction):
            await interaction.response.edit_message(content=" ", delete_after=0.1)
            sub=1
            self.ctx = await self.ctx.channel.send(content="loading...")
            em = await Embeds.reddit(subreddit=sub, ctx=interaction.user)
            vi = View_reddit(ctx=self.ctx, subreddit=sub)
            await self.ctx.edit(content="", embed=em, view=vi)

    if settings.data.get('subreddits').get("max") >= 2:
        @discord.ui.button(label=settings.data.get('subreddits').get(2).get('button_label'), style=discord.ButtonStyle.red, emoji="<:reddit:987690510481231942>", disabled=False, custom_id=f"reddit_2_{settings.data.get('subreddits').get(2).get('name')}")
        async def n2_button_callback(self, button, interaction):
            await interaction.response.edit_message(content=" ", delete_after=0.1)
            sub=2
            self.ctx = await self.ctx.channel.send(content="loading...")
            em = await Embeds.reddit(subreddit=sub, ctx=interaction.user)
            vi = View_reddit(ctx=self.ctx, subreddit=sub)
            await self.ctx.edit(content="", embed=em, view=vi)

    if settings.data.get('subreddits').get("max") >= 3:
        @discord.ui.button(label=settings.data.get('subreddits').get(3).get('button_label'), style=discord.ButtonStyle.red, emoji="<:reddit:987690510481231942>", disabled=False, custom_id=f"reddit_3_{settings.data.get('subreddits').get(3).get('name')}")
        async def n3_button_callback(self, button, interaction):
            await interaction.response.edit_message(content=" ", delete_after=0.1)
            sub=3
            self.ctx = await self.ctx.channel.send(content="loading...")
            em = await Embeds.reddit(subreddit=sub, ctx=interaction.user)
            vi = View_reddit(ctx=self.ctx, subreddit=sub)
            await self.ctx.edit(content="", embed=em, view=vi)

    if settings.data.get('subreddits').get("max") >= 4:
        @discord.ui.button(label=settings.data.get('subreddits').get(4).get('button_label'), style=discord.ButtonStyle.red, emoji="<:reddit:987690510481231942>", disabled=False, custom_id=f"reddit_4_{settings.data.get('subreddits').get(4).get('name')}")
        async def n4_button_callback(self, button, interaction):
            await interaction.response.edit_message(content=" ", delete_after=0.1)
            sub=4
            self.ctx = await self.ctx.channel.send(content="loading...")
            em = await Embeds.reddit(subreddit=sub, ctx=interaction.user)
            vi = View_reddit(ctx=self.ctx, subreddit=sub)
            await self.ctx.edit(content="", embed=em, view=vi)

    if settings.data.get('subreddits').get("max") >= 5:
        @discord.ui.button(label=settings.data.get('subreddits').get(5).get('button_label'), style=discord.ButtonStyle.red, emoji="<:reddit:987690510481231942>", disabled=False, custom_id=f"reddit_5_{settings.data.get('subreddits').get(5).get('name')}")
        async def n5_button_callback(self, button, interaction):
            await interaction.response.edit_message(content=" ", delete_after=0.1)
            sub=5
            self.ctx = await self.ctx.channel.send(content="loading...")
            em = await Embeds.reddit(subreddit=sub, ctx=interaction.user)
            vi = View_reddit(ctx=self.ctx, subreddit=sub)
            await self.ctx.edit(content="", embed=em, view=vi)

    if settings.data.get('subreddits').get("max") >= 6:
        @discord.ui.button(label=settings.data.get('subreddits').get(6).get('button_label'), style=discord.ButtonStyle.red, emoji="<:reddit:987690510481231942>", disabled=False, custom_id=f"reddit_6_{settings.data.get('subreddits').get(6).get('name')}")
        async def n6_button_callback(self, button, interaction):
            await interaction.response.edit_message(content=" ", delete_after=0.1)
            sub=6
            self.ctx = await self.ctx.channel.send(content="loading...")
            em = await Embeds.reddit(subreddit=sub, ctx=interaction.user)
            vi = View_reddit(ctx=self.ctx, subreddit=sub)
            await self.ctx.edit(content="", embed=em, view=vi)

    if settings.data.get('subreddits').get("max") >= 7:
        @discord.ui.button(label=settings.data.get('subreddits').get(7).get('button_label'), style=discord.ButtonStyle.red, emoji="<:reddit:987690510481231942>", disabled=False, custom_id=f"reddit_7_{settings.data.get('subreddits').get(7).get('name')}")
        async def n7_button_callback(self, button, interaction):
            await interaction.response.edit_message(content=" ", delete_after=0.1)
            sub=7
            self.ctx = await self.ctx.channel.send(content="loading...")
            em = await Embeds.reddit(subreddit=sub, ctx=interaction.user)
            vi = View_reddit(ctx=self.ctx, subreddit=sub)
            await self.ctx.edit(content="", embed=em, view=vi)

    if settings.data.get('subreddits').get("max") >= 8:
        @discord.ui.button(label=settings.data.get('subreddits').get(8).get('button_label'), style=discord.ButtonStyle.red, emoji="<:reddit:987690510481231942>", disabled=False, custom_id=f"reddit_8_{settings.data.get('subreddits').get(8).get('name')}")
        async def n8_button_callback(self, button, interaction):
            await interaction.response.edit_message(content=" ", delete_after=0.1)
            sub=8
            self.ctx = await self.ctx.channel.send(content="loading...")
            em = await Embeds.reddit(subreddit=sub, ctx=interaction.user)
            vi = View_reddit(ctx=self.ctx, subreddit=sub)
            await self.ctx.edit(content="", embed=em, view=vi)

    if settings.data.get('subreddits').get("max") >= 9:
        @discord.ui.button(label=settings.data.get('subreddits').get(9).get('button_label'), style=discord.ButtonStyle.red, emoji="<:reddit:987690510481231942>", disabled=False, custom_id=f"reddit_9_{settings.data.get('subreddits').get(9).get('name')}")
        async def n9_button_callback(self, button, interaction):
            await interaction.response.edit_message(content=" ", delete_after=0.1)
            sub=9
            self.ctx = await self.ctx.channel.send(content="loading...")
            em = await Embeds.reddit(subreddit=sub, ctx=interaction.user)
            vi = View_reddit(ctx=self.ctx, subreddit=sub)
            await self.ctx.edit(content="", embed=em, view=vi)


    if settings.data.get('subreddits').get("max") >= 10:
        @discord.ui.button(label=settings.data.get('subreddits').get(10).get('button_label'), style=discord.ButtonStyle.red, emoji="<:reddit:987690510481231942>", disabled=False, custom_id=f"reddit_10_{settings.data.get('subreddits').get(10).get('name')}")
        async def n10_button_callback(self, button, interaction):
            await interaction.response.edit_message(content=" ", delete_after=0.1)
            sub = 10
            self.ctx = await self.ctx.channel.send(content="loading...")
            em = await Embeds.reddit(subreddit=sub, ctx=interaction.user)
            vi = View_reddit(ctx=self.ctx, subreddit=sub)
            await self.ctx.edit(content="", embed=em, view=vi)

    if settings.data.get('subreddits').get("max") >= 11:
        @discord.ui.button(label=settings.data.get('subreddits').get(11).get('button_label'), style=discord.ButtonStyle.red, emoji="<:reddit:987690510481231942>", disabled=False, custom_id=f"reddit_11_{settings.data.get('subreddits').get(11).get('name')}")
        async def n11_button_callback(self, button, interaction):
            await interaction.response.edit_message(content=" ", delete_after=0.1)
            sub = 11
            self.ctx = await self.ctx.channel.send(content="loading...")
            em = await Embeds.reddit(subreddit=sub, ctx=interaction.user)
            vi = View_reddit(ctx=self.ctx, subreddit=sub)
            await self.ctx.edit(content="", embed=em, view=vi)

    if settings.data.get('subreddits').get("max") >= 12:
        @discord.ui.button(label=settings.data.get('subreddits').get(12).get('button_label'), style=discord.ButtonStyle.red, emoji="<:reddit:987690510481231942>", disabled=False, custom_id=f"reddit_12_{settings.data.get('subreddits').get(12).get('name')}")
        async def n12_button_callback(self, button, interaction):
            await interaction.response.edit_message(content=" ", delete_after=0.1)
            sub = 12
            self.ctx = await self.ctx.channel.send(content="loading...")
            em = await Embeds.reddit(subreddit=sub, ctx=interaction.user)
            vi = View_reddit(ctx=self.ctx, subreddit=sub)
            await self.ctx.edit(content="", embed=em, view=vi)

    if settings.data.get('subreddits').get("max") >= 13:
        @discord.ui.button(label=settings.data.get('subreddits').get(13).get('button_label'),
                           style=discord.ButtonStyle.red, emoji="<:reddit:987690510481231942>", disabled=False,
                           custom_id=f"reddit_13_{settings.data.get('subreddits').get(13).get('name')}")
        async def n13_button_callback(self, button, interaction):
            await interaction.response.edit_message(content=" ", delete_after=0.1)
            sub = 13
            self.ctx = await self.ctx.channel.send(content="loading...")
            em = await Embeds.reddit(subreddit=sub, ctx=interaction.user)
            vi = View_reddit(ctx=self.ctx, subreddit=sub)
            await self.ctx.edit(content="", embed=em, view=vi)

    if settings.data.get('subreddits').get("max") >= 14:
        @discord.ui.button(label=settings.data.get('subreddits').get(14).get('button_label'),
                           style=discord.ButtonStyle.red, emoji="<:reddit:987690510481231942>", disabled=False,
                           custom_id=f"reddit_14_{settings.data.get('subreddits').get(14).get('name')}")
        async def n14_button_callback(self, button, interaction):
            await interaction.response.edit_message(content=" ", delete_after=0.1)
            sub = 14
            self.ctx = await self.ctx.channel.send(content="loading...")
            em = await Embeds.reddit(subreddit=sub, ctx=interaction.user)
            vi = View_reddit(ctx=self.ctx, subreddit=sub)
            await self.ctx.edit(content="", embed=em, view=vi)

    if settings.data.get('subreddits').get("max") >= 15:
        @discord.ui.button(label=settings.data.get('subreddits').get(15).get('button_label'),
                           style=discord.ButtonStyle.red, emoji="<:reddit:987690510481231942>", disabled=False,
                           custom_id=f"reddit_15_{settings.data.get('subreddits').get(15).get('name')}")
        async def n15_button_callback(self, button, interaction):
            await interaction.response.edit_message(content=" ", delete_after=0.1)
            sub = 15
            self.ctx = await self.ctx.channel.send(content="loading...")
            em = await Embeds.reddit(subreddit=sub, ctx=interaction.user)
            vi = View_reddit(ctx=self.ctx, subreddit=sub)
            await self.ctx.edit(content="", embed=em, view=vi)


class View_reddit(View):
    def __init__(self, ctx, subreddit):
        super().__init__(timeout=settings.data.get('commands').get('default-timeout'))
        self.ctx = ctx
        self.sub = subreddit


    @discord.ui.button(label="regenerate", style=discord.ButtonStyle.blurple, emoji="🥰", disabled=False, custom_id="reddit_regen")
    async def regen_button_callback(self, button, interaction):
        await interaction.response.edit_message(content="Loading...")
        em = await Embeds.reddit(subreddit=self.sub, ctx=interaction.user)
        await self.ctx.edit(content="", embed=em)


    @discord.ui.button(label="new picture", style=discord.ButtonStyle.red, emoji="😈", disabled=False, custom_id="reddit_new")
    async def new_button_callback(self, button, interaction):
        button.disabled = True
        regenbutton = [x for x in self.children if x.custom_id=="reddit_regen"][0]
        regenbutton.disabled = True
        await interaction.response.edit_message(content="", view=self)


        self.ctx = await interaction.followup.send(content="loading...")
        em = await Embeds.reddit(subreddit=self.sub, ctx=interaction.user)
        vi = View_reddit(ctx=self.ctx, subreddit=self.sub)
        await self.ctx.edit(content="", embed=em, view=vi)

    async def on_timeout(self):
        try:
            if debug >= 2:
                print(f" Reddit has timed out. ")
            regenbutton = [x for x in self.children if x.custom_id == "reddit_regen"][0]
            regenbutton.disabled = True
            newbutton = [x for x in self.children if x.custom_id == "reddit_new"][0]
            newbutton.disabled = True
            await self.ctx.edit(content="", view=self)
        except:
            if debug >= 2:
                print(f" message was deleted before timeout ")

class View_fitomklasika(View):
    def __init__(self, ctx):
        super().__init__(timeout=settings.data.get('commands').get('default-timeout'))
        self.ctx = ctx

    @discord.ui.button(label="regenerate", style=discord.ButtonStyle.blurple, emoji="🥰", disabled=False, custom_id="regen_pic")
    async def regen_button_callback(self, button, interaction):
        em = await Embeds.fitom_klasika(ctx=interaction.user)
        vi = View_fitomklasika(ctx=self.ctx)

        await interaction.response.edit_message(embed=em, view=vi)


    @discord.ui.button(label="new picture", style=discord.ButtonStyle.red, emoji="😈", disabled=False, custom_id="new_pic")
    async def new_button_callback(self, button, interaction):
        button.disabled = True
        regenbutton = [x for x in self.children if x.custom_id=="regen_pic"][0]
        regenbutton.disabled = True
        await interaction.response.edit_message(content="", view=self)

        self.ctx = await interaction.followup.send(content="loading...")
        em = await Embeds.fitom_klasika(ctx=interaction.user)
        vi = View_fitomklasika(ctx=self.ctx)
        await self.ctx.edit(content="", embed=em, view=vi)

    async def on_timeout(self):
        try:
            if debug >= 2:
                print(f" Fitom-Klasika has timed out. ")
            regenbutton = [x for x in self.children if x.custom_id == "regen_pic"][0]
            regenbutton.disabled = True
            newbutton = [x for x in self.children if x.custom_id == "new_pic"][0]
            newbutton.disabled = True
            await self.ctx.edit(content="", view=self)
        except:
            if debug >= 2:
                print(f" message was deleted before timeout ")

class View_random(View):
        def __init__(self, ctx):
            super().__init__(timeout=settings.data.get('commands').get('default-timeout'))
            self.ctx = ctx

        @discord.ui.button(label="regenerate", style=discord.ButtonStyle.blurple, emoji="🥰", disabled=False,
                           custom_id="random_regen")
        async def random_regen_button_callback(self, button, interaction):
            x = random.choice(["fitom", "reddit"])
            if x == "reddit":
                sub="all"
                await interaction.response.edit_message(content="loading...")
                em = await Embeds.reddit(subreddit=sub, ctx=interaction.user)
                vi = View_random(ctx=self.ctx)
                await self.ctx.edit(content="", embed=em, view=vi)
            elif x == "fitom":
                em = await Embeds.fitom_klasika(ctx=interaction.user)
                vi = View_random(ctx=self.ctx)
                await interaction.response.edit_message(embed=em, view=vi)

        @discord.ui.button(label="new picture", style=discord.ButtonStyle.red, emoji="😈", disabled=False,
                           custom_id="random_new")
        async def random_new_button_callback(self, button, interaction):
            button.disabled = True
            regenbutton = [x for x in self.children if x.custom_id == "random_regen"][0]
            regenbutton.disabled = True
            await interaction.response.edit_message(content="", view=self)

            x = random.choice(["fitom", "reddit"])
            self.ctx = await interaction.followup.send(content="loading...")
            if x == "reddit":
                sub="all"
                em = await Embeds.reddit(subreddit=sub, ctx=interaction.user)
                vi = View_random(ctx=self.ctx)
                await self.ctx.edit(content="", embed=em, view=vi)
            elif x == "fitom":
                em = await Embeds.fitom_klasika(ctx=interaction.user)
                vi = View_random(ctx=self.ctx)
                await self.ctx.edit(content="", embed=em, view=vi)

        async def on_timeout(self):
            try:
                self.disable_all_items()
                await self.ctx.edit(content="", view=self)
                if debug >= 2:
                    print(f" random has timed out ")
            except:
                if debug >= 2:
                    print(f" message was deleted before timeout ")

class View_botowner(View):
    def __init__(self, ctx, user, botownermessage):
        super().__init__(timeout=6969)
        self.ctx = ctx
        self.user = user
        self.botownermessage = botownermessage

    @discord.ui.button(label="Reddit update", style=discord.ButtonStyle.blurple, emoji="<:reddit:987690510481231942>", disabled=False, custom_id="reddit_update")
    async def reddit_update_callback(self, button, interaction):
        button.disabled = True
        await interaction.response.edit_message(view=self)

        for max_subreddits in range(1, 1 + settings.data.get('subreddits').get("max")):
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
                    dict1 = {
                        quantity: {'id': f'{submission}', 'url': f'{submission.url}', 'title': f'{submission.title}',
                                   'author': f'{submission.author}', 'score': submission.score}}
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

        button.disabled = False
        await self.botownermessage.edit(view=self)
        await self.user.send(content="Database of Reddit pictures was updated.")

    @discord.ui.button(label="Update check", style=discord.ButtonStyle.blurple, emoji="⤴", disabled=False, custom_id="check_update")
    async def check_update_callback(self, button, interaction):
        em = Embeds.botowner()
        await interaction.response.edit_message(embed=em)

        await self.user.send(content="Version succesfully checked.", delete_after=10)

        """version_request = requests.get('https://api.github.com/repos/kchulka/p-bot/releases/latest')
        version_json = version_request.json()

        if version != version_json["tag_name"]:
            version_message= f"Newer version {version_json['tag_name']} is available, download [**here**](https://github.com/kchulka/p-bot/releases/latest)."
        else:
            version_message = "You are using the latest version."
            """

    async def on_timeout(self):
        try:
            if debug >= 3:
                print(f" botowner has timed out. ")
            reddit_update = [x for x in self.children if x.custom_id == "reddit_update"][0]
            reddit_update.disabled = True

            check_update = [x for x in self.children if x.custom_id == "check_update"][0]
            check_update.disabled = True

            await self.botownermessage.edit(view=self)

            vi = View_botowner(ctx=self.ctx, user=self.user, botownermessage=self.botownermessage)
            await self.botownermessage.edit(view=vi)
        except:
            if debug >= 3:
                print(f" message was deleted before timeout ")

class View_help(View):
    def __init__(self, ctx):
        super().__init__(timeout=settings.data.get('commands').get('help-timeout'))
        self.ctx = ctx

    @discord.ui.button(style=discord.ButtonStyle.gray, emoji="❌", disabled=False, custom_id="x")
    async def regen_button_callback(self, button, interaction):
        await interaction.response.edit_message(content=" ", delete_after=0.1)

    async def on_timeout(self):
        try:
            self.clear_items()
            await self.ctx.edit(content="", view=self)
        except:
            if debug >= 2:
                print(f" message was deleted before timeout ")

""" ----- COMMANDS ----- """

@bot.command(
    name=settings.data.get('commands').get('random'),
    description="Get a random pic from all categories!"
)
async def picrandom(ctx):
    if debug >= 1:
        print(f"random picture executed by: {ctx.author} ")
    try:
        if ctx.channel.is_nsfw() == False:
            em = Embeds.notnswfchannel()
            await ctx.respond(embed=em, delete_after=10)
        else:
            x = random.choice(["fitom", "reddit"])
            if debug >= 3:
                print(f"random picture: {x} ")
            if x == "reddit":
                sub = "all"
                await ctx.respond(content="loading...")
                em = await Embeds.reddit(subreddit=sub, ctx=ctx.user)
                vi = View_random(ctx=ctx)
                await ctx.edit(content="", embed=em, view=vi)
            elif x == "fitom":
                em = await Embeds.fitom_klasika(ctx=ctx.user)
                vi = View_random(ctx)
                await ctx.respond(embed=em, view=vi)
    except:
        x = random.choice(["fitom", "reddit"])
        if debug >= 3:
            print(f"random picture: {x} ")
        if x == "reddit":
            sub="all"
            await ctx.respond(content="loading...")
            em = await Embeds.reddit(subreddit=sub, ctx=ctx.user)
            vi = View_random(ctx=ctx)
            await ctx.edit(content="", embed=em, view=vi)
        elif x == "fitom":
            em = await Embeds.fitom_klasika(ctx=ctx.user)
            vi = View_random(ctx=ctx)
            await ctx.respond(embed=em, view=vi)

@bot.command(
    name=settings.data.get('commands').get('category'),
    description="Get a random pic from a category chosen by you!"
)
async def piccategory(ctx):
    if debug >= 1:
        print(f"category picture executed by: {ctx.author} ")
    try:
        if ctx.channel.is_nsfw() == False:
            em = Embeds.notnswfchannel()
            await ctx.respond(embed=em, delete_after=10)
        else:
            vi = View_choosecategory(ctx)
            em = Embeds.choose_category()

            await ctx.respond(embed=em, view=vi)
    except:
        vi = View_choosecategory(ctx)
        em = Embeds.choose_category()

        await ctx.respond(embed=em, view=vi)


@bot.command(
    name=settings.data.get('commands').get('help'),
    description="Get some help!"
)
async def help(ctx):
    em = Embeds.help()
    vi = View_help(ctx)
    await ctx.respond(content="", embed=em, view=vi)

""" ----- run ----- """

bot.run(TOKEN)

