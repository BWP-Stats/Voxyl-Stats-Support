import discord
from discord.ext import commands, tasks
import json
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.utils.manage_components import create_select, create_select_option, create_actionrow
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.utils.manage_components import wait_for_component

class createpanel(commands.Cog):

    def __init__(self, client):
        self.client = client



    @cog_ext.cog_slash(name="createpanel",
        description="Send a ticket panel in the selected channel",
        options=[
            create_option(
                name="channel",
                description="What channel do you want me to send the panel in",
                option_type=discord.TextChannel,
                required=True
            )
        ]
    )
    async def _panel(self, ctx, channel:discord.TextChannel):
        if ctx.author.guild_permissions.administrator == True:
            embed = discord.Embed(title="Voxyl Stats Support", description="Please click the the button corresponding to what type of support you need")
            buttons = [
                create_button(style=ButtonStyle.blue, label="Discord Bot Support", custom_id="dbsup"),
                create_button(style=ButtonStyle.blue, label="Overlay Support", custom_id="ovsup", disabled=False),
                create_button(style=ButtonStyle.blue, label="Website Support", custom_id="websup", disabled=True),
                create_button(style=ButtonStyle.blue, label="Premium Support", custom_id="presup", disabled=False),
                create_button(style=ButtonStyle.blue, label="Other", custom_id="otsup", disabled=False),
            ]
            await channel.send(embed=embed, components=[create_actionrow(*buttons)])


        else:
            await ctx.reply("You need ``administrator`` permissions to complete that command", hidden=True)




def setup(client):
    client.add_cog(createpanel(client))
