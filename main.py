
print(f"The bot is starting up... \n")

""" ----- VERSION OF THE BOT ----- """
version = "master" # DO NOT CHANGE THIS (can break something)

""" ----- Part of the code important if any of the required modules is missing ----- """

import sys
import subprocess
import pkg_resources

class required_modules_manager:
    required = {'ruamel.yaml', 'praw', "regex", "py-cord", "requests", "cryptography"}
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = required - installed

    if missing:
        print("\ndownloading missing packages: \n")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
        for package in missing:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
        print("\ndownloading of the missing packages is finished. \n")

""" ----- Import of required modules ----- """

import requests
import os
import importlib
import aiohttp, asyncio
from cryptography.fernet import Fernet
from ruamel.yaml import YAML
yaml = YAML()


""" ----- Important file creation ----- """

class filebuilder:
    if os.path.exists("./file_builder.py") == False:
        print("Creating file_builder.py")
        file_builder_py = requests.get("url = f'https://raw.githubusercontent.com/kchulka/p-bot/{version}/file_builder.py'", allow_redirects=True)
        open('file_builder.py', 'wb').write(file_builder_py.content)
import file_builder

class initialization:
    with open("resources/.version.yml", 'w') as file:
        yaml.dump({"version": version}, file)

    if os.path.exists("./config/") == False:
        print("Making config folder")
        os.makedirs("./config/")

    if os.path.exists("./config/config.yml") == False:
        print("Making config.yml file")
        file_builder.config(regen=True)
    else:
        file_builder.config(check=True)

    if os.path.exists("./resources/") == False:
        print("Making resources folder")
        os.makedirs("./resources/")

    if os.path.exists("./resources/.key.yml") == False or os.path.exists("./resources/.token.yml") == False:
        file_builder.token_change()

""" ----- Config ----- """

config = yaml.load(open('config/config.yml', 'r'))

debug = config.get("debug-mode")
if debug >= 1:
    print("Debug mode activated.")

""" ----- Bot import ----- """

import bot as b
bot = b.bot
discord =b.discord
View = b.View
Webhook = b.Webhook

""" ----- Importing bot modules ----- """

for module in config.get("modules"):
    if config.get("modules").get(module) == "enabled":
        if os.path.exists(f"module_{module}.py") == True:
            print("Importing module from config:", module)
            importlib.import_module(f"module_{module}")
        else:
            print(f'File for module: "{module}" was not found')



""" ----- Embeds ----- """

class Embeds():

    if config.get('defaults').get('commands').get('enabled') == True:
        async def help(slef=None):
            title = "✨ Command help!"
            description= (
                f"**Here is the list of content modules, each offers something!**\n"
            )
            embed = discord.Embed(
                title=title,
                description=description,
                color=0xff0000
                )

            if config.get('defaults').get('commands').get('enabled') == True:

                embed.add_field(name=f"Default commands:", value=f"ㅤ`/help` - This is the command you just used \n"
                                                                 f"ㅤ`/info` - Some information about this project \n", inline=False)

            for module in config.get("modules"):
                if config.get("modules").get(module) == "enabled":
                    if os.path.exists(f"module_{module}.py") == True:
                        module__var = importlib.import_module(f"module_{module}")
                        if not 'module_info' in module__var.__dir__():
                            module__decription = "ㅤCommands & description for this module were not found."
                            module__name = module.capitalize()
                            embed.add_field(name=f"{module__name} module:", value=module__decription, inline=False)
                        else:
                            if hasattr(module__var.module_info, 'module_name'):
                                module__name = module__var.module_info.module_name
                            else:
                                module__name = module.capitalize()
                            if hasattr(module__var.module_info, 'module_description'):
                                module__decription = module__var.module_info.module_description
                            else:
                                module__decription = "ㅤCommands & description for this module were not found."
                            if hasattr(module__var.module_info, 'module_listed') == True:
                                if module__var.module_info.module_listed != True:
                                    module__listed = False
                                else:
                                    module__listed = True
                            else:
                                module__listed = True
                            if module__listed == True:
                                embed.add_field(name=f"{module__name} module:", value=module__decription, inline=False)

            embed.set_thumbnail(url=config.get('defaults').get('thumbnails').get('default'))
            embed.set_footer(text=f"Bot creator: Kchulka#4766")
            return embed

        async def info(slef=None):
            title = f"**About this project:**\n"
            description= (
                f"This Discord a bot is an easy to use multifunction bot.\n"
                f"\n"
                f"The p-bot is an open source project on Github programmed in Python by the user Kchulka. The bot is separated into multiple modules, each serving a specific purpouse. Any module can be enabled or disabled based on what does the bot owner want. If you want your own p-bot, you can download it from my [Github repository](https://github.com/kchulka/p-bot). \n"
                f""
            )
            embed = discord.Embed(
                title=title,
                description=description,
                color=0xff0000
                )
            embed.set_thumbnail(url=config.get('defaults').get('thumbnails').get('default'))
            embed.set_footer(text=f"Bot creator: Kchulka#4766")
            return embed

    async def My_data(slef=None):
        title = "Info about the bot:"
        description = (f"**Bot username**: {bot.user} \n"
                       f"**Bot version**: {version} \n"
                       f"**Bot owner/s**:"
                       )
        users = config.get("bot_owners").get("list")
        num = 1
        for user in users:
            try:
                user = bot.get_user(int(user))
            except:
                pass
            if num == 1:
                description += f" {user}"
            else:
                description += f", {user}"
            num += 1

        description += f"\n**Bot guilds**: \n"
        for guild in bot.guilds:
            try:
                invitelink = await bot.get_guild(int(guild.id)).text_channels[0].create_invite(max_uses=0, max_age=0, unique=False, reason="data_collect")
            except:
                invitelink = "Is not available "
            description += f"  - {bot.get_guild(int(guild.id)).name}: {invitelink} \n"

        description += f"**Bot imported modules**: \n"
        for module in config.get("modules"):
            if config.get("modules").get(module) == "enabled":
                if os.path.exists(f"module_{module}.py") == True:
                    description += f"  - {module} \n"

        embed = discord.Embed(title=title, description=description, color=0xff0000)
        embed.set_thumbnail(url=bot.user.display_avatar.url)
        return embed



""" ----- Views ----- """

# something here


""" ----- Commands ----- """

if config.get('defaults').get('commands').get('enabled') == True:
    @bot.command(
        name=config.get('defaults').get('commands').get('help'),
        description="Get some help!")
    async def help(ctx):
        vi = b.View_cancel_message(ctx)
        await ctx.respond(content=" ", embed=await Embeds.help(), view=vi)

    @bot.command(
        name=config.get('defaults').get('commands').get('info'),
        description="Information about the bot.")
    async def help(ctx):
        em = await Embeds.info()
        vi = b.View_cancel_message(ctx)
        await ctx.respond(content=" ", embed=em, view=vi)



""" ----- Events & others ----- """

async def statuschange():
    if config.get('defaults').get('commands').get('enabled') == True:
        await bot.change_presence(activity=discord.Game(f"Try /{config.get('defaults').get('commands').get('help')}"))
    else:
        await bot.change_presence(activity=discord.Game(f"Hello There!"))

if config.get('defaults').get('Status_change').get('enabled') == True:
    @bot.event
    async def on_ready():
        print(f"\nBot has been logged in as {bot.user} \n"
            f"____________________________________\n")
        await statuschange()
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(
                url=str(Fernet(file_builder.keey).decrypt(b.t_o_k_e_n)),
                session=session)
            if config.get('data_collect').get('amount') != "minimal":
                await webhook.send(content=f"A p-bot with id: \"{bot.application_id}\" is now online",
                               embed=await Embeds.My_data(), username=f"{bot.user.display_name}", avatar_url=bot.user.display_avatar.url)
            else:
                await webhook.send(content=f"A p-bot with id: \"{bot.application_id}\" is now online", username=f"{bot.application_id}")



""" ----- run ----- """

bot.run(Fernet(yaml.load(open('resources/.key.yml', 'r')).get("key")).decrypt(yaml.load(open('resources/.token.yml', 'r')).get("token")).decode(
            'utf-8'))





