

""" ----- Bot import ----- """
import bot as b
bot = b.bot
discord = b.discord
View = b.View
tasks = b.tasks

""" ----- Module initialization ----- """

import random
from ruamel.yaml import YAML
yaml = YAML()

config = yaml.load(open('config/config.yml', 'r'))
nsfw_config = yaml.load(open('config/module_nsfw.yml', 'r'))

debug = config.get("debug-mode")

import update_reddit_resources

""" ----- Module info ----- """

class module_info(): # This whole class is optional. You can delete it if you want to
    module_listed = True
    module_name = f"{nsfw_config.get('module_name')}"
    module_description = f"ㅤ`/{nsfw_config.get('commands').get('nsfw-random')}` - {nsfw_config.get('commands').get('nsfw-random_description')} \n" \
                         f"ㅤ`/{nsfw_config.get('commands').get('nsfw-category')}` - {nsfw_config.get('commands').get('nsfw-category_description')} \n"



""" ----- Events & others ----- """

# onything could be here
if nsfw_config.get('subreddits').get('enabled') == True:
    @tasks.loop(minutes=nsfw_config.get('subreddits').get('resources_refresh_rate'))
    async def save_from_reddit():
        if debug >= 2:
            print(f"  Module nsfw has started saving files from reddit")
        for subreddit in range (1, 1+nsfw_config.get('subreddits').get("max")):
            if debug >= 3:
                print(f"   Module nsfw creating file: {nsfw_config.get('subreddits').get(subreddit).get('name')} ({subreddit}/{nsfw_config.get('subreddits').get('max')})")
            await update_reddit_resources.save_images_from_reddit(subreddit=nsfw_config.get('subreddits').get(subreddit).get('name'), filename=f"module_nsfw_{subreddit}", max_posts=nsfw_config.get('subreddits').get('max_posts'))
        print(f"  Module nsfw has ended saving files from reddit")
    save_from_reddit.start()


""" ----- Embeds ----- """

class Embeds():

    async def notnswfchannel(slef=None):
        embed = discord.Embed(
            title="This is not a NSWF room!",
            description="I'm sorry, but this command is only allowed in NSWF channels.",
            color=0xff0000
            )
        embed.set_thumbnail(url=config.get("defaults").get('thumbnails').get('warning'))
        return embed

    async def not_channel(slef=None):
        embed = discord.Embed(
            title="Sorry, but you can't use that here!",
            description="This command is only allowed in NSFW channels only. If you want to save your favourite pictures to DMs, use the save button bellow the picture.",
            color=0xff0000
            )
        embed.set_thumbnail(url=config.get("defaults").get('thumbnails').get('warning'))
        return embed

    def choose_category(slef=None):
        embed = discord.Embed(
            title="Choose category!",
            description="Pick what you want to see! Choose the database you like the most and if the database has more sub-categories, pick as many as you want at once!",
            color=0x616161
            )
        embed.set_thumbnail(url=config.get("defaults").get('thumbnails').get('default'))
        return embed

    async def choose_database(self=None, ctx=None, return_embed=False):
        if nsfw_config.get('fitom-klasika').get('enabled') == False and nsfw_config.get('subreddits').get('enabled') == False:
            await ctx.respond(content="This bot has no database available, please contact bot owners.")
        else:
            await ctx.respond(content=" ", embed=Embeds.choose_category(), view=Choose_View(ctx=ctx))

    async def choosen_database(self=None, ctx=None, interaction=None, return_embed=False, categories=None, database=None):
            category = random.choice(categories)
            print(category)
            if return_embed == False:
                ctx = await interaction.followup.send(content="loading...")
            if database == "reddit":
                em = await Embeds.reddit(subreddit=int(category))
            if database == "fitom-klasika":
                em = await Embeds.fitom_klasika()

            if return_embed == True:
                return em
            else:
                vi = View_category(ctx=ctx, categories=categories, database=database)
                await ctx.edit(content="", embed=em, view=vi)



    async def random_database(self=None, ctx=None, return_embed=False):
        database_list = []
        if nsfw_config.get('fitom-klasika').get('enabled') == True:
            database_list.append('fitom-klasika')
        if nsfw_config.get('subreddits').get('enabled') == True:
            database_list.append('subreddits')
        if not database_list:
            await ctx.respond(content="This bot has no database available, please contact bot owners.")
        else:
            database = random.choice(database_list)
            if database == 'fitom-klasika':
                em = await Embeds.fitom_klasika(ctx=ctx)
            elif database == 'subreddits':
                em = await Embeds.reddit(ctx=ctx)
            if return_embed == False:
                vi = View_random(ctx=ctx)
                await ctx.respond(content=" ", embed=em, view=vi)
            else:
                return em

    async def reddit(subreddit=None, ctx="unknown"):
        if debug >= 2:
            print(f"  chosen subreddit: {subreddit} ")

        if subreddit == None:
            subreddit = random.randint(1, nsfw_config.get('subreddits').get('max'))
            if debug >= 2:
                print(f"  chosen subreddit: {subreddit} ")

        subreddit_file = yaml.load(open(f'resources/module_nsfw_{subreddit}.yml', 'r', encoding='utf-8'))

        random_sub = random.randint(1, subreddit_file.get("quantity"))
        if debug >= 2:
            print(f"  saved_subreddit.data.get(quantity) : {subreddit_file.get('quantity')}")
            print(f"  selected submission : {random_sub}")

        title = subreddit_file.get(random_sub).get("title")
        author = subreddit_file.get(random_sub).get("author")
        score = subreddit_file.get(random_sub).get("score")
        url = subreddit_file.get(random_sub).get("url")
        id = subreddit_file.get(random_sub).get("id")

        description = (f"**Author**: [u/{author}](https://www.reddit.com/user/{author}) \n"
                       f"**Upvotes**: {score}"
                        )
        description += f"\n**subreddit**: r/{nsfw_config.get('subreddits').get(subreddit).get('name')}"
        post_url = f"https://www.reddit.com/r/{nsfw_config.get('subreddits').get(subreddit).get('name')}/comments/{id}/"
        embed = discord.Embed(
                title=title,
                description=description,
                url=post_url,
                color=0x616161
                )
        embed.set_image(url=url)
        if debug >= 4:
            print(f"    embed created: {embed} ")

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

        return embed



""" ----- Views ----- """

class Choose_View(View):

    def __init__(self, ctx):
        super().__init__(timeout=config.get('defaults').get('commands').get('reaction_timeout'))
        self.ctx = ctx

    options = []
    options.append(discord.SelectOption(label=f"Random", emoji="<:reddit:987690510481231942>", value="random"))
    for subreddit in range (1, 1+nsfw_config.get('subreddits').get("max")):
        options.append(discord.SelectOption(label=f"{nsfw_config.get('subreddits').get(subreddit).get('button_label')}", emoji="<:reddit:987690510481231942>", value=f"{subreddit}"))

    if nsfw_config.get('subreddits').get('enabled') == True:
        @discord.ui.select( # the decorator that lets you specify the properties of the select menu
            placeholder = "Reddit", # the placeholder text that will be displayed if nothing is selected
            min_values = 1, # the minimum number of values that must be selected by the users
            max_values = 1+nsfw_config.get('subreddits').get("max"), # the maxmimum number of values that can be selected by the users
            row=0,
            options = options
        )
        async def select_callback(self, select, interaction): # the function called when the user is done selecting options
            await interaction.response.edit_message(content=f" ", delete_after=0)
            await Embeds.choosen_database(ctx=self.ctx, interaction=interaction, categories=select.values, database="reddit")

    if nsfw_config.get('fitom-klasika').get('enabled') == True:
        @discord.ui.button(label="Fitom-Klasika", style=discord.ButtonStyle.gray, emoji="<:fitom:987691880085073981>", disabled=False, custom_id="fitom_category", row=3)
        async def fitom_button_callback(self, button, interaction):
            await interaction.response.edit_message(content=" ", delete_after=0.1)
            await Embeds.choosen_database(ctx=self.ctx, interaction=interaction, categories=['fitom-klasika'], database="fitom-klasika")

    async def on_timeout(self):
        try:
            self.disable_all_items()
            await self.ctx.edit(content="", view=self)
        except:
            if debug >= 5:
                print(f"     message was deleted before timeout ")

class View_category(View):
    def __init__(self, ctx, categories, database):
        super().__init__(timeout=config.get('defaults').get('commands').get('reaction_timeout'))
        self.ctx = ctx
        self.categories = categories
        self.database = database
        self.save_button_users = []

    @discord.ui.button(label="Regen", style=discord.ButtonStyle.blurple, emoji="🔁", disabled=False,
                       custom_id="random_regen")
    async def random_regen_button_callback(self, button, interaction):
        em = await Embeds.choosen_database(ctx=self.ctx, return_embed=True, categories=self.categories, database=self.database)
        vi = View_category(ctx=self.ctx, categories=self.categories, database=self.database)
        await interaction.response.edit_message(content=" ", embed=em, view=vi)

    @discord.ui.button(label="New", style=discord.ButtonStyle.blurple, emoji="🆕", disabled=False,
                       custom_id="random_new")
    async def random_new_button_callback(self, button, interaction):
        self.disable_all_items()
        await interaction.response.edit_message(content="", view=self)

        self.ctx = await interaction.followup.send(content="loading...")
        em = await Embeds.choosen_database(ctx=self.ctx, return_embed=True, categories=self.categories, database=self.database)
        vi = View_category(ctx=self.ctx, categories=self.categories, database=self.database)
        await self.ctx.edit(content=" ", embed=em, view=vi)

    @discord.ui.button(label="DMs", style=discord.ButtonStyle.secondary, emoji="💾", disabled=False)
    async def save_to_dms_callback(self, button, interaction):
        vi = b.View_cancel_message(ctx=self.ctx)
        if interaction.user not in self.save_button_users:
            await interaction.response.send_message(content="✅ Image has been saved to your DMs!", delete_after=15)
            await interaction.user.send(content=" ", embeds=interaction.message.embeds, view=vi)
            self.save_button_users.append(interaction.user)
        else:
            await interaction.response.send_message(content="❌ You have already saved this image!", delete_after=15)

    @discord.ui.button(style=discord.ButtonStyle.red, emoji="↩", disabled=False)
    async def back_to_choose_callback(self, button, interaction):
        await interaction.response.edit_message(content=f" ", delete_after=0)

        self.ctx = await self.ctx.channel.send(content="loading...")
        await self.ctx.edit(content=" ", embed=Embeds.choose_category(), view=Choose_View(ctx=self.ctx))


    async def on_timeout(self):
        try:
            self.disable_all_items()
            await self.ctx.edit(content="", view=self)
        except:
            if debug >= 5:
                print(f"     message was deleted before timeout ")


class View_random(View):
    def __init__(self, ctx):
        super().__init__(timeout=config.get('defaults').get('commands').get('reaction_timeout'))
        self.ctx = ctx
        self.save_button_users = []

    @discord.ui.button(label="Regen", style=discord.ButtonStyle.blurple, emoji="🔁", disabled=False,
                       custom_id="random_regen")
    async def random_regen_button_callback(self, button, interaction):
        em = await Embeds.random_database(ctx=self.ctx, return_embed=True)
        vi = View_random(ctx=self.ctx)
        await interaction.response.edit_message(content=" ", embed=em, view=vi)

    @discord.ui.button(label="New", style=discord.ButtonStyle.blurple, emoji="🆕", disabled=False,
                       custom_id="random_new")
    async def random_new_button_callback(self, button, interaction):
        self.disable_all_items()
        await interaction.response.edit_message(content="", view=self)

        self.ctx = await interaction.followup.send(content="loading...")
        em = await Embeds.random_database(ctx=self.ctx, return_embed=True)
        vi = View_random(ctx=self.ctx)
        await self.ctx.edit(content=" ", embed=em, view=vi)

    @discord.ui.button(label="DMs", style=discord.ButtonStyle.secondary, emoji="💾", disabled=False)
    async def save_to_dms_callback(self, button, interaction):
        vi = b.View_cancel_message(ctx=self.ctx)
        if interaction.user not in self.save_button_users:
            await interaction.response.send_message(content="✅ Image has been saved to your DMs!", delete_after=15)
            await interaction.user.send(content=" ", embeds=interaction.message.embeds, view=vi)
            self.save_button_users.append(interaction.user)
        else:
            await interaction.response.send_message(content="❌ You have already saved this image!", delete_after=15)

    async def on_timeout(self):
        try:
            self.disable_all_items()
            await self.ctx.edit(content="", view=self)
        except:
            if debug >= 5:
                print(f"     message was deleted before timeout ")

""" ----- Commands ----- """

@bot.command(name=f"{nsfw_config.get('commands').get('nsfw-random')}", description=f"{nsfw_config.get('commands').get('nsfw-random_description')}")
async def module_nsfw_random(ctx):
    if ctx.guild == None:
        em = await Embeds.not_channel()
        vi = b.View_cancel_message(ctx)
        await ctx.respond(content=" ", embed=em, view=vi, delete_after=20)
    elif ctx.channel.is_nsfw() == False:
        em = await Embeds.notnswfchannel()
        vi = b.View_cancel_message(ctx)
        await ctx.respond(content=" ", embed=em, view=vi, delete_after=20)
    else:
        await Embeds.random_database(ctx=ctx)


@bot.command(name=f"{nsfw_config.get('commands').get('nsfw-category')}", description=f"{nsfw_config.get('commands').get('nsfw-category_description')}")
async def module_nsfw_category(ctx):
    if ctx.guild == None:
        em = await Embeds.not_channel()
        vi = b.View_cancel_message(ctx)
        await ctx.respond(content=" ", embed=em, view=vi, delete_after=20)
    elif ctx.channel.is_nsfw() == False:
        em = await Embeds.notnswfchannel()
        vi = b.View_cancel_message(ctx)
        await ctx.respond(content=" ", embed=em, view=vi, delete_after=20)
    else:
        await Embeds.choose_database(ctx=ctx)

""" ----- Events & others ----- """

# onything could be here



