import discord
from discord.ext import commands, tasks
import sqlite3
import json
import asyncio
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.utils.manage_components import create_select, create_select_option, create_actionrow
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.utils.manage_components import wait_for_component

logchannel = 927304057931038800

class Events(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    #@commands.command()
    #async def test(self, ctx):
        #await ctx.send("eeeeeeeeeeeeeeeeeeee")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.id == self.client.user.id:
            pass
        else:
            channel = self.client.get_channel(logchannel)
            em = discord.Embed(title=f"Message deleted in {message.channel}", description=f"""Message Content: {message.content}""", timestamp=message.created_at)
            em.set_author(name=message.author, icon_url=message.author.avatar_url)
            em.set_footer(text=f"{message.author.id}")
            await channel.send(embed=em)
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if not before.author.bot == True:
            channel = self.client.get_channel(logchannel)
            em = discord.Embed(title=f"Message editted in {before.channel}", description=f"\u200b", timestamp=message.created_at)
            em.add_field(name="Before", value=f"{before[:2000]}")
            em.add_field(name="After", value=f"{after[:2000]}")
            em.set_author(name=before.author, icon_url=before)
            em.set_footer(text=f"{before.author.id}")




def setup(client):
    client.add_cog(Events(client))