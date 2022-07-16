

""" ----- Bot import ----- """
import bot as b
bot = b.bot
discord = b.discord
View = b.View

""" ----- Module initialization ----- """

""" ----- Module info ----- """

class module_info(): # This whole class is optional. You can delete it if you want to
    module_listed = True
    module_name = "Nsfw"
    module_description = f"ㅤ`/nudes` - sends a random pornographic picture \n" \
                         f"ㅤ`/nudes-category` - choose a category of pictures \n"



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

class View_cancel_message(View):
    def __init__(self, ctx):
        super().__init__(timeout=60)
        self.ctx = ctx

    @discord.ui.button(style=discord.ButtonStyle.gray, emoji="❌", disabled=False, custom_id="x")
    async def regen_button_callback(self, button, interaction):
        await interaction.response.edit_message(content=" ", delete_after=0.1)

    async def on_timeout(self):
        try:
            self.clear_items()
            await self.ctx.edit(content="", view=self)
        except:
            print("message not found")



""" ----- Commands ----- """

@bot.command(name="nsfw-random", description="Get some help!")
async def module_nsfw_random(ctx):
        em = Embeds.help()
        vi = b.View_cancel_message(ctx)
        await ctx.respond(content=" ", embed=em, view=vi)



""" ----- Events & others ----- """

# onything could be here



