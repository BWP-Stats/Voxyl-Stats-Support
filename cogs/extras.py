import discord
from discord.ext import commands, tasks
import sqlite3
import asyncio
import json
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_commands import create_option, create_choice


class Extras(commands.Cog):

    def __init__(self, client):
        self.client = client
            

    @cog_ext.cog_slash(name="links",
        description="Gives the url to any important links",
    )
    async def _links(self, ctx:SlashContext):
        embed = discord.Embed(title="Important Links", description=f"""[Invite Link](https://discord.com/api/oauth2/authorize?client_id=926814210321707028&permissions=277025442816&scope=bot%20applications.commands)
[Support Server](https://discord.gg/fBnfWXSDpu)
[Buymeacoffee](https://www.buymeacoffee.com/voxlystats/)
Website (Soon)""")
        buttons = [
            create_button(style=ButtonStyle.URL, label="Invite", url="https://discord.com/api/oauth2/authorize?client_id=926814210321707028&permissions=277025442816&scope=bot%20applications.commands", disabled=False),
            create_button(style=ButtonStyle.URL, label="Support Server", url="https://discord.gg/fBnfWXSDpu", disabled=False),
            create_button(style=ButtonStyle.URL, label="Buymeacoffee", url="https://www.buymeacoffee.com/voxlystats/", disabled=False),
            create_button(style=ButtonStyle.URL, label="Website (Soon)", url="https://discord.gg/fBnfWXSDpu", disabled=True),
        ]
        await ctx.send(embed=embed, components=[create_actionrow(*buttons)])




def setup(client):
    client.add_cog(Extras(client))