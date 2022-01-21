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


class Slowmode(commands.Cog):

    def __init__(self, client):
        self.client = client
    

    @cog_ext.cog_slash(name="slowmode",
        description="Set a slowmode for a channel",
        options=[
            create_option(
                name="channel",
                description="Channel to add slowmode to",
                option_type=discord.TextChannel,
                required=True
            ),
            create_option(
                name="seconds",
                description="Number of seconds for slowmode",
                option_type=4,
                required=True
            )
        ]
    )
    async def _slowmode(self, ctx:SlashContext, channel:discord.TextChannel, seconds:int):
        if ctx.author.guild_permissions.kick_members == True:
            if seconds < 0:
                await ctx.send("Must be above 0 seconds", hidden=True)
                return
            if seconds > 21600:
                await ctx.send("Your slowmode can't be that high. Please use a number below 21600.", hidden=True)
            else:
                await channel.edit(slowmode_delay=seconds)
                embed=discord.Embed(title=(f"Channel Slowmode"), description=(f"The slowmode for {channel.mention} has been set to {seconds}"))
                await ctx.send(embed=embed)
        else:
            await ctx.send("You need ``kick members`` permission to complete this command", hidden=True)
                

        

    #@commands.Cog.listener()




def setup(client):
    client.add_cog(Slowmode(client))