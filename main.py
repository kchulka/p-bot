
""" ----- The import stuff ----- """

import discord
from discord import SlashCommandGroup
from discord.ext import commands
from discord.ui import  Button, View

#import requests

import random
""" ----- TOKEN ----- """

TOKEN = "ODU2ODI3MTc4NzM4Mzg0ODk2.G_Xhxo.RsvGVgXn1n_70uhwonkjQujBsm17whQCv_NdqM"

""" ----- BOT & INITIALIZATION ----- """

print(f"The bot is starting up... \n")

bot = discord.Bot(
    command_prefix="ph.",
    intents=discord.Intents(members=True, messages=True, guilds=True),
    debug_guilds=[586268358710657024]
)

@bot.event
async def on_ready():
    print(f"Bot has been logged in as {bot.user} \n"
          f"____________________________________")

""" ----- NOT NSWF CHANNEL ----- """

def notnswfchannel():
    notnswfchannelem = discord.Embed(title="This is not a NSWF channel!",
                                     description="I'm sorry, but this command is only allowed in NSWF channels.",
                                     color=0xff0000
                                     )
    notnswfchannelem.set_thumbnail(url="https://i.pinimg.com/originals/c2/ea/1a/c2ea1a0d3e357245661a69cc83ec050a.jpg")
    return notnswfchannelem


""" ----- PIC ----- """

def randompic():
    randompic = discord.Embed(
        title="Enjoy the photo <3",
        color=0x616161
                              )
    y = random.randint(1, 2)
    if y == 1:
        x = random.randint(1, 100)
    elif y == 2:
        x = random.randint(101, 200)
    url = f'https://raw.githubusercontent.com/FitomPlays/klasika/main/{y}/{x}.jpg'
    print("cmd /pic", url)
    randompic.set_image(url=url)
    return randompic


class randompicView(View):
    def __init__(self):
        super().__init__(timeout=2)


    @discord.ui.button(label="regenerate", style=discord.ButtonStyle.blurple, emoji="🥰", disabled=False, custom_id="regen_pick")
    async def regen_button_callback(self, button, interaction):
        print(button)
        button.label = "test"
        print(button)
        em = randompic()
        vi = randompicView()

        await interaction.response.edit_message(embed=em, view=vi)


    @discord.ui.button(label="new picture", style=discord.ButtonStyle.red, emoji="😈", disabled=False, custom_id="new_pick")
    async def new_button_callback(self, button, interaction):
        print(button)
        button.disabled = True
        print(button)
        regenbutton = [x for x in self.children if x.custom_id=="regen_pick"][0]
        regenbutton.disabled = True
        await interaction.response.edit_message(content="", view=self)
        em = randompic()
        vi = randompicView()
        await interaction.followup.send(embed=em, view=vi)


    async def on_timeout(self):
        print("timeout")
        regenbutton = [x for x in self.children if x.custom_id=="regen_pick"][0]
        regenbutton.disabled = True
        await self.message.edit(content="", view=self)


@bot.command(
    description="Get a random pic!"
)
async def pic(ctx):
    if ctx.channel.is_nsfw() == False:
        em = notnswfchannel()
        await ctx.respond(embed=em)
    else:
        em = randompic()
        vi = randompicView()
        await ctx.respond(embed=em, view=vi)










""" ----- The Picture stuff ----- """

picture = SlashCommandGroup(name="picture", description="picture stuff.")
category = picture.create_subgroup("category", "test")



@category.command(
    name="test",
    description="test.",
    guild_ids=[586268358710657024]
)
async def test(ctx):
    await ctx.respond("hm")

bot.add_application_command(picture)

""" ----- The downloader stuff ----- """

downloader = SlashCommandGroup(name="downloader", description="Used for downloading stuff from PH.")

#class View(discord.ui.View): # Create a class called View that subclasses discord.ui.View
#    @discord.ui.button(label="Click me!", style=discord.ButtonStyle.blurple, emoji="😎") # Create a button with the label "😎 Click me!" with color Blurple
#    async def button_callback(self, button, interaction):
#        await interaction.response.send_message("You clicked the button!") # Send a message when the button is clicked

@downloader.command(
    name="phdwnld",
    description="Donwload videos prom pornhub.",
    guild_ids=[586268358710657024])
async def phdwnld(ctx):
    await ctx.respond("This feature is in progress!", view=View())

#bot.add_application_command(downloader)


""" ----- run ----- """

bot.run(TOKEN)



