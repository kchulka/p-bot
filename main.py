
print(f"The bot is starting up... \n")

""" ----- The import stuff ----- """

import discord
from discord import SlashCommandGroup
from discord.ext import commands
from discord.ui import Button, View

import asyncpraw

import random

import re

import yaml
from yaml import Loader

""" ----- settings stuff ----- """

class settings:
    def __init__(self):
        self.file = open('resources/settings.yml', 'r')
        self.data = yaml.load(self.file, Loader=Loader)
        #print(self.data)
settings = settings()


""" ----- TOKEN ----- """

TOKEN = settings.data.get("TOKEN")

""" ----- reddet ----- """

reddit = asyncpraw.Reddit(
    client_id = settings.data.get("reddit_login").get("client_id"),
    client_secret = settings.data.get("reddit_login").get("client_secret"),
    username = settings.data.get("reddit_login").get("username"),
    password = settings.data.get("reddit_login").get("password"),
    user_agent = settings.data.get("reddit_login").get("user_agent")
)

""" ----- BOT & INITIALIZATION ----- """

bot = discord.Bot(
    command_prefix="notused",
    intents=discord.Intents(members=True, messages=True, guilds=True),
    debug_guilds=[]
)

@bot.event
async def on_ready():
    print(f"Bot has been logged in as {bot.user} \n"
          f"____________________________________")

""" ----- embeds ----- """

class Embeds():

    def notnswfchannel(slef=None):
        embed = discord.Embed(
            title="This is not a NSWF room!",
            description="I'm sorry, but this command is only allowed in NSWF rooms.",
            color=0xff0000
            )
        embed.set_thumbnail(url="https://i.pinimg.com/originals/c2/ea/1a/c2ea1a0d3e357245661a69cc83ec050a.jpg")
        return embed

    def fitom_klasika(slef=None):
        embed = discord.Embed(
            title="Enjoy the photo <3",
            color=0x616161
        )
        y = random.randint(1, 4)
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
        url = f'https://raw.githubusercontent.com/FitomPlays/klasika/main/{y}/{x}.jpg'
        #print("Fitom-klasika url:", url)
        embed.set_image(url=url)
        return embed

    def choose_category(slef=None):
        embed = discord.Embed(
            title="Choose category",
            description="You can pick here between Reddit and Fitom-Klasika.",
            color=0x616161
            )
        embed.set_thumbnail(url="https://www.electrokit.com/uploads/productimage/41017/ksr18_3.jpg")
        return embed

    def timeout_category(slef=None):
        embed = discord.Embed(
            title="Time's up!",
            description="Please execute the command again!",
            color=0x616161
            )
        embed.set_thumbnail(url="https://www.electrokit.com/uploads/productimage/41017/ksr18_3.jpg")
        return embed

    def reddit_category(self=None):
        embed = discord.Embed(
            title="Choose your favourite subreddit",
            description="You can pick here between multiple choices.",
            color=0x616161
            )
        embed.set_thumbnail(url="https://www.electrokit.com/uploads/productimage/41017/ksr18_3.jpg")
        return embed

    async def reddit(subreddit):
        print(subreddit)
        if subreddit == "all":
            subreddit = random.choice(["nsfw", "nudes", "toocuteforporn", "pussy", "ass"])
            print("chosen from all:", subreddit)
        sub = await reddit.subreddit(subreddit)
        all_subs = []
        top = sub.hot(limit=100)

        async for submission in top:
            all_subs.append(submission)

        random_sub = random.choice(all_subs)

        check = r"(?:http\:|https\:)?\/\/.*\.(?:png|jpg)"
        matches = re.search(check, random_sub.url, re.IGNORECASE)
        print(matches)
        while matches == None:
            random_sub = random.choice(all_subs)
            matches = re.search(check, random_sub.url, re.IGNORECASE)
            print(matches)

        else:

            name = random_sub.title
            embed = discord.Embed(
                title=name,
                color=0x616161
            )

            embed.set_image(url=random_sub.url)

            return embed


""" ----- CATEGORIES / Views ----- """

class View_choosecategory(View):
    def __init__(self, ctx):
        super().__init__(timeout=30)
        self.ctx = ctx

    @discord.ui.button(label="Reddit", style=discord.ButtonStyle.gray, emoji="<:reddit:987690510481231942>", disabled=False, custom_id="reddit_category")
    async def reddit_button_callback(self, button, interaction):
        print(self.ctx)
        em = Embeds.reddit_category()
        vi = View_redditcategory(ctx=self.ctx)
        await interaction.response.edit_message(content="", embed=em, view=vi)


    @discord.ui.button(label="Fitom-Klasika", style=discord.ButtonStyle.gray, emoji="<:fitom:987691880085073981>", disabled=False, custom_id="fitom_category")
    async def fitom_button_callback(self, button, interaction):
        await interaction.response.edit_message(content=" ", delete_after=0.1)

        self.ctx = await self.ctx.channel.send(content="loading...")
        em = Embeds.fitom_klasika()
        vi = View_fitomklasika(ctx=self.ctx)
        await self.ctx.edit(content="", embed=em, view=vi)

    async def on_timeout(self):
        #print("timeout")
        try:
            em = Embeds.timeout_category()
            redditbutton = [x for x in self.children if x.custom_id == "reddit_category"][0]
            redditbutton.disabled = True
            fitombutton = [x for x in self.children if x.custom_id == "fitom_category"][0]
            fitombutton.disabled = True
            # print(self.ctx)
            await self.ctx.edit(content="", embed=em, view=self)
        except:
            print("message was deleted")


class View_redditcategory(View):
    def __init__(self, ctx):
        super().__init__(timeout=30)
        self.ctx = ctx


    @discord.ui.button(label="All", style=discord.ButtonStyle.red, emoji="<:reddit:987690510481231942>", disabled=False, custom_id="reddit_c_all")
    async def all_button_callback(self, button, interaction):
        await interaction.response.edit_message(content=" ", delete_after=0.1)
        sub="all"
        self.ctx = await self.ctx.channel.send(content="loading...")
        em = await Embeds.reddit(subreddit=sub)
        vi = View_reddit(ctx=self.ctx, subreddit=sub)
        await self.ctx.edit(content="", embed=em, view=vi)


    @discord.ui.button(label="NSFW", style=discord.ButtonStyle.red, emoji="<:reddit:987690510481231942>", disabled=False, custom_id="reddit_c_nsfw")
    async def nsfw_button_callback(self, button, interaction):
        await interaction.response.edit_message(content=" ", delete_after=0.1)
        sub="nsfw"
        self.ctx = await self.ctx.channel.send(content="loading...")
        em = await Embeds.reddit(subreddit=sub)
        vi = View_reddit(ctx=self.ctx, subreddit=sub)
        await self.ctx.edit(content="", embed=em, view=vi)


    @discord.ui.button(label="Nudes", style=discord.ButtonStyle.red, emoji="<:reddit:987690510481231942>", disabled=False, custom_id="reddit_c_Nudes")
    async def nudes_button_callback(self, button, interaction):
        await interaction.response.edit_message(content=" ", delete_after=0.1)
        sub="nudes"
        self.ctx = await self.ctx.channel.send(content="loading...")
        em = await Embeds.reddit(subreddit=sub)
        vi = View_reddit(ctx=self.ctx, subreddit=sub)
        await self.ctx.edit(content="", embed=em, view=vi)

    @discord.ui.button(label="Pussy", style=discord.ButtonStyle.red, emoji="<:reddit:987690510481231942>", disabled=False, custom_id="reddit_c_pussy")
    async def pussy_button_callback(self, button, interaction):
        await interaction.response.edit_message(content=" ", delete_after=0.1)
        sub="pussy"
        self.ctx = await self.ctx.channel.send(content="loading...")
        em = await Embeds.reddit(subreddit=sub)
        vi = View_reddit(ctx=self.ctx, subreddit=sub)
        await self.ctx.edit(content="", embed=em, view=vi)

    @discord.ui.button(label="Ass", style=discord.ButtonStyle.red, emoji="<:reddit:987690510481231942>", disabled=False, custom_id="reddit_c_ass")
    async def ass_button_callback(self, button, interaction):
        await interaction.response.edit_message(content=" ", delete_after=0.1)
        sub="ass"
        self.ctx = await self.ctx.channel.send(content="loading...")
        em = await Embeds.reddit(subreddit=sub)
        vi = View_reddit(ctx=self.ctx, subreddit=sub)
        await self.ctx.edit(content="", embed=em, view=vi)

    @discord.ui.button(label="Too cute for porn", style=discord.ButtonStyle.red, emoji="<:reddit:987690510481231942>", disabled=False, custom_id="reddit_c_tcfp")
    async def tcfp_button_callback(self, button, interaction):
        await interaction.response.edit_message(content=" ", delete_after=0.1)
        sub="toocuteforporn"
        self.ctx = await self.ctx.channel.send(content="loading...")
        em = await Embeds.reddit(subreddit=sub)
        vi = View_reddit(ctx=self.ctx, subreddit=sub)
        await self.ctx.edit(content="", embed=em, view=vi)

class View_reddit(View):
    def __init__(self, ctx, subreddit):
        super().__init__(timeout=30)
        self.ctx = ctx
        self.sub = subreddit


    @discord.ui.button(label="regenerate", style=discord.ButtonStyle.blurple, emoji="🥰", disabled=False, custom_id="reddit_regen")
    async def regen_button_callback(self, button, interaction):
        await interaction.response.edit_message(content="Loading...")
        em = await Embeds.reddit(subreddit=self.sub)
        await self.ctx.edit(content="", embed=em)


    @discord.ui.button(label="new picture", style=discord.ButtonStyle.red, emoji="😈", disabled=False, custom_id="reddit_new")
    async def new_button_callback(self, button, interaction):
        button.disabled = True
        regenbutton = [x for x in self.children if x.custom_id=="reddit_regen"][0]
        regenbutton.disabled = True
        await interaction.response.edit_message(content="", view=self)


        self.ctx = await self.ctx.channel.send(content="loading...")
        em = await Embeds.reddit(subreddit=self.sub)
        vi = View_reddit(ctx=self.ctx, subreddit=self.sub)
        await self.ctx.edit(content="", embed=em, view=vi)

    async def on_timeout(self):
        try:
            #print("timeout")
            regenbutton = [x for x in self.children if x.custom_id == "reddit_regen"][0]
            regenbutton.disabled = True
            newbutton = [x for x in self.children if x.custom_id == "reddit_new"][0]
            newbutton.disabled = True
            #print(self.ctx)
            await self.ctx.edit(content="", view=self)
        except:
            print("message was deleted")

class View_fitomklasika(View):
    def __init__(self, ctx):
        super().__init__(timeout=30)
        self.ctx = ctx

    @discord.ui.button(label="regenerate", style=discord.ButtonStyle.blurple, emoji="🥰", disabled=False, custom_id="regen_pic")
    async def regen_button_callback(self, button, interaction):
        em = Embeds.fitom_klasika()
        vi = View_fitomklasika(ctx=self.ctx)

        await interaction.response.edit_message(embed=em, view=vi)


    @discord.ui.button(label="new picture", style=discord.ButtonStyle.red, emoji="😈", disabled=False, custom_id="new_pic")
    async def new_button_callback(self, button, interaction):
        button.disabled = True
        regenbutton = [x for x in self.children if x.custom_id=="regen_pic"][0]
        regenbutton.disabled = True
        await interaction.response.edit_message(content="", view=self)

        em = Embeds.fitom_klasika()
        vi = View_fitomklasika(ctx=self.ctx)
        self.ctx = await interaction.followup.send(embed=em, view=vi)

    async def on_timeout(self):
        try:
            #print("timeout")
            regenbutton = [x for x in self.children if x.custom_id == "regen_pic"][0]
            regenbutton.disabled = True
            newbutton = [x for x in self.children if x.custom_id == "new_pic"][0]
            newbutton.disabled = True
            #print(self.ctx)
            await self.ctx.edit(content="", view=self)
        except:
            print("message was deleted")

""" ----- COMMANDS ----- """

@bot.command(
    name="pic-random",
    description="Get a random pic from all categories!"
)
async def picrandom(ctx):
    if ctx.channel.is_nsfw() == False:
        em = Embeds.notnswfchannel()
        await ctx.respond(embed=em, delete_after=10)
    else:
        em = Embeds.fitom_klasika()
        vi = View_fitomklasika(ctx)
        print(ctx)
        await ctx.respond(embed=em, view=vi)

@bot.command(
    name="pic-category",
    description="Get a random pic from a category chosen by you!"
)
async def piccategory(ctx):
    if ctx.channel.is_nsfw() == False:
        em = Embeds.notnswfchannel()
        await ctx.respond(embed=em, delete_after=10)

    else:
        vi = View_choosecategory(ctx)
        em = Embeds.choose_category()

        await ctx.respond(content="", embed=em, view=vi)

@bot.command(
    name="help",
    description="Get some help!"
)
async def help(ctx):
    em = Embeds.notnswfchannel()
    vi = View_fitomklasika(ctx)
    print(ctx)
    await ctx.respond(content="help")

""" ----- run ----- """

bot.run(TOKEN)



