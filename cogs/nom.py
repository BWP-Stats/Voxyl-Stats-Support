import discord
from discord.ext import commands, tasks
import sqlite3
import asyncio
import json
import random
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_commands import create_option, create_choice


class Nom(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @cog_ext.cog_slash(name="nom",
        description="nom"
    )
    async def _nom(self, ctx):
        await ctx.send("NOM", delete_after=60)


def setup(client):
    client.add_cog(Nom(client))
