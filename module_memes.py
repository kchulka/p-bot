
""" ----- Bot import ----- """
import bot as b
bot = b.bot
discord = b.discord
View = b.View

""" ----- Module initialization ----- """

""" ----- Module info ----- """

class module_info():
    module_name = "Reddit memes"
    module_description = f"ㅤ`/meme` - send a random meme \n" \
                         f"ㅤ`/meme-category` - sends a meme from the chosen category \n"


""" ----- Events & others ----- """

# onything could be here



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



