import nextcord
from nextcord.ext import commands, tasks
from nextcord import Interaction, SlashOption
from nextcord.abc import GuildChannel
import json, sys, os

class SendMessageOrEmbed(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @nextcord.slash_command(name="sendmessage", description="Send a message to a channel")
    async def sendmessage(
        self,
        ctx : Interaction,
        channel: GuildChannel = SlashOption(
            name="channel",
            description="Channel to send the message to",
            required=True,
            channel_types=[nextcord.ChannelType.text]
        ),
        ):
        if ctx.user.guild_permissions.administrator:
            await ctx.response.defer()
            try:
                await ctx.send("Please send the message you want to send")
                msg = await self.client.wait_for("message", check=lambda m: m.author == ctx.user)
                await channel.send(msg.content)
                await ctx.send(f"Successfully sent the message to {channel.mention}")
            except:
                pass
        else:
            await ctx.send("You don't have permission to run this command", ephemeral=True)

    @nextcord.slash_command(name="sendembed", description="Send an embed to a channel")
    async def sendembed(
        self,
        ctx : Interaction,
        channel: GuildChannel = SlashOption(
            name="channel",
            description="Channel to send the embed to",
            required=True,
            channel_types=[nextcord.ChannelType.text]
        ),
        ):
        if ctx.user.guild_permissions.administrator:
            await ctx.response.defer()
            try:
                await ctx.send("What is the title of the embed?")
                title = await self.client.wait_for("message", check=lambda m: m.author == ctx.user)
                await ctx.send("What is the description of the embed?")
                desc = await self.client.wait_for("message", check=lambda m: m.author == ctx.user)
                if len(title.content) > 256 or len(desc.content) > 4000:
                    await ctx.send("The title and description are too long", ephemeral=True)
                    return
                embed = nextcord.Embed(title=title.content, description=desc.content)
                await channel.send(embed=embed)
                await ctx.send(f"Successfully sent the embed to {channel.mention}")
            except Exception as e:
                print(e)
                pass
        else:
            await ctx.send("You don't have permission to run this command", ephemeral=True)
        


def setup(client):
    client.add_cog(SendMessageOrEmbed(client))
