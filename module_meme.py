

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
meme_config = yaml.load(open('config/module_meme.yml', 'r'))

debug = config.get("debug-mode")

import update_reddit_resources

""" ----- Module info ----- """

class module_info(): # This whole class is optional. You can delete it if you want to
    module_listed = True
    module_name = f"{meme_config.get('module_name')}"
    module_description = f"ㅤ`/{meme_config.get('commands').get('meme-random')}` - {meme_config.get('commands').get('meme-random_description')} \n" \
                         f"ㅤ`/{meme_config.get('commands').get('meme-category')}` - {meme_config.get('commands').get('meme-category_description')} \n"



""" ----- Events & others ----- """

# onything could be here
if meme_config.get('subreddits').get('enabled') == True:
    @tasks.loop(minutes=meme_config.get('subreddits').get('resources_refresh_rate'))
    async def save_from_reddit():
        if debug >= 2:
            print(f"  Module meme has started saving files from reddit")
        for subreddit_category in range (1, 1+meme_config.get('subreddits').get("max")):
            for subreddit in meme_config.get('subreddits').get(subreddit_category).get('name'):
                if debug >= 3:
                    print(f"   Module meme creating file: {subreddit} ({subreddit_category}/{meme_config.get('subreddits').get('max')})")
                await update_reddit_resources.save_images_from_reddit(subreddit=subreddit, filename=f"module_meme_{subreddit}", max_posts=meme_config.get('subreddits').get('max_posts'))
        print(f"  Module meme has ended saving files from reddit")

    @bot.listen('on_ready')
    async def start_loop():
        save_from_reddit.start()


""" ----- Embeds ----- """

class Embeds():

    def help(slef=None):
        title = "EXAMPLE!"
        description= f"This is an example embed.\n"
        embed = discord.Embed(
                title=title,
                description=description,
                color=0xff0000
                )
        embed.set_footer(text=f"Bot creator: Kchulka#4766")
        return embed



""" ----- Views ----- """





""" ----- Commands ----- """

@bot.command(name="meme", description="Memes!")
async def meme(ctx):
        em = Embeds.help()
        vi = b.View_cancel_message(ctx)
        await ctx.respond(content=" ", embed=em, view=vi)



""" ----- Events & others ----- """

# onything could be here



