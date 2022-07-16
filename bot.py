
import discord
from discord import SlashCommandGroup
from discord.ext import commands
from discord.ui import Button, View
from discord import Webhook

from ruamel.yaml import YAML
yaml = YAML()

config = yaml.load(open('config/config.yml', 'r'))
debug = config.get("debug-mode")

bot = discord.Bot(
    intents=discord.Intents(members=True, messages=True, guilds=True),
    debug_guilds=[], owner_ids=[324152796414869506]
)

class View_cancel_message(View):
    def __init__(self, ctx):
        super().__init__(timeout=config.get('defaults').get('commands').get('reaction_timeout'))
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

t_o_k_e_n = b'gAAAAABi0WxGWBfF1Irn6-cljg13YrpozXSv75iycmRV8K7T9hGnKFj2SXaqRR2eyfs44E7W_eijNoyycPw8-DlVZp-sWVyDsqpg1rvHq_uh-Hl5hci9VC-o2G1uTZo_5Og10WMBBP38vq-ILYB144rc4XnldQxzTHvZ-g1wHW6SQ3Z-0H8By4lokAgH83CprgFtqRSNQss9Vj8Af8Zxf2izV4DWXHGG3Va8WPU_Y7qNS1qYXaOZCu4='