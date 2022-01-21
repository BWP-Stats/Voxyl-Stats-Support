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


class Lock(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @cog_ext.cog_slash(name="lock",
        description="Lock a channel",
        options=[
            create_option(
                name="channel",
                description="Channel to lock",
                option_type=discord.TextChannel,
                required=True
            ),
            create_option(
                name="reason",
                description="Reason for locking",
                option_type=3,
                required=False
            )
        ]
    )
    async def _lock(self, ctx:SlashContext, channel:discord.TextChannel, reason:str=None):
        if ctx.author.guild_permissions.ban_members == True:
            role = ctx.guild.get_role(926955604738707597)
            await channel.set_permissions(role, send_messages=False)
            if reason == None:
                reason = "None Given"
            embed=discord.Embed(title=(f"Channel Locked"), description=(f"{channel.mention} has been locked with reason: {reason}"))
            await ctx.send(embed=embed)
        else:
            await ctx.send("You need ``ban members`` permission to complete this command", hidden=True)

    @cog_ext.cog_slash(name="unlock",
        description="Unlock a channel",
        options=[
            create_option(
                name="channel",
                description="Channel to unlock",
                option_type=discord.TextChannel,
                required=True
            ),
            create_option(
                name="reason",
                description="Reason for unlocking",
                option_type=3,
                required=False
            )
        ]
    )
    async def _unlock(self, ctx:SlashContext, channel:discord.TextChannel, reason:str=None):
        if ctx.author.guild_permissions.ban_members == True:
            role = ctx.guild.get_role(926955604738707597)
            await channel.set_permissions(role, send_messages=True)
            if reason == None:
                reason = "None Given"
            embed=discord.Embed(title=(f"Channel Unlocked"), description=(f"""{channel.mention} has been unlocked with reason: {reason}"""))
            await ctx.send(embed=embed)
        else:
            await ctx.send("You need ``ban members`` permission to complete this command", hidden=True)



def setup(client):
    client.add_cog(Lock(client))