import discord
from discord.ext import commands, tasks
import asyncio
import json
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_commands import create_option, create_choice


class Purge(commands.Cog):

    def __init__(self, client):
        self.client = client
            

    @cog_ext.cog_slash(name="purge",
        description="Purge a channel",
        options=[
            create_option(
                name="amount",
                description="Amount of message to purge (max 100)",
                option_type=4,
                required=True
            ),
            create_option(
                name="member",
                description="Purge a users messages",
                option_type=6,
                required=False
            )
        ]
    )
    async def _purge(self, ctx:SlashContext, amount:int, member:discord.Member=None):
        if ctx.author.guild_permissions.kick_members == True:
            if amount > 100:
                await ctx.send("The purge amount cannot be over 100", hidden=True)
            elif amount <= 0:
                await ctx.send("The purge amount cannot be below 0", hidden=True)
            else:
                if member == None:
                    await ctx.channel.purge(limit=amount)
                    await ctx.send(f"Successfully purged {amount} messages")
                else:
                    def check(msgb):
                        return msgb.author.id == member.id
                    await ctx.channel.purge(limit=amount, check=check)
                    await ctx.send(f"Successfully purged {amount} of {member} messages")
        else:
            await ctx.send("You need ``kick members`` permission to complete this command", hidden=True)




def setup(client):
    client.add_cog(Purge(client))
