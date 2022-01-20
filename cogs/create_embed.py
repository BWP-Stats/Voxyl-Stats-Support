import discord
from discord.ext import commands, tasks
import asyncio
import random
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_commands import create_option, create_choice


class CreateEmbed(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @cog_ext.cog_slash(name="create_embed",
        description="Create an embed",
        options=[
            create_option(
                name="channel",
                description="Channel to send embed to",
                option_type=discord.TextChannel,
                required=True
            )
        ]
    )
    async def _create_embed(self, ctx:SlashContext, channel:discord.TextChannel):
        if ctx.author.guild_permissions.administrator == True:
            try:
                def check(message):
                    return message.author == ctx.author and message.channel == ctx.channel
                await ctx.send("What do you want the title to be?")
                title = await self.client.wait_for('message', check=check)
                await ctx.send("What do you want the description to be?")
                description = await self.client.wait_for("message", check=check)
                if len(title.content) > 255:
                    await ctx.send("Your title must be less than 255 characters")
                elif len(description.content) > 4000:
                    await ctx.send("Your description must be less than 4000 characters")
                else:
                    embed = discord.Embed(title=(f"{title.content}"), description=(f"""{description.content}"""))
                    await channel.send(embed=embed)
                    try:
                        embed = discord.Embed(title=(f"Embed Created"), description=(f"""Embed created and sent to {channel.mention}"""))
                        await ctx.send(embed=embed)
                    except:
                        pass
            except:
                await ctx.send(f"There was an error sending the embed to {channel.mention}. Please make sure I have ``embed_links`` and ``send_messages`` permission in that channel.", hidden=True)

        else:
            await ctx.send("You need ``administrator`` permission to complete this command", hidden=True)




    #@commands.Cog.listener()




def setup(client):
    client.add_cog(CreateEmbed(client))
