import discord
from discord.ext import commands, tasks
import json
import asyncio
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.utils.manage_components import create_select, create_select_option, create_actionrow
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.utils.manage_components import wait_for_component

class createpanelveri(commands.Cog):

    def __init__(self, client):
        self.client = client



    @cog_ext.cog_slash(name="verifymessage",
        description="Send a verify message to a channel",
        options=[
            create_option(
                name="channel",
                description="What channel do you want me to send the verify message to?",
                option_type=discord.TextChannel,
                required=True
            ),
            create_option(
                name="custom",
                description="If enabled, you will be taken through the process of creating your own embed",
                option_type=5,
                required=False,
            )
        ]
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _verifymessage(self, ctx, channel:discord.TextChannel, custom : str=None):
        if ctx.author.guild_permissions.administrator == True:
            if custom == True:
                def check(message):
                    return message.author == ctx.author and message.channel == ctx.channel
                try:
                    q1 = await ctx.send("What do you want the title to be?")
                    title = await self.client.wait_for('message', check=check, timeout = 300)
                    q2 = await ctx.send("What do you want the description to be?")
                    description = await self.client.wait_for("message", check=check, timeout=300)
                    if len(title.content) > 255:
                        await ctx.send("Your title must be less than 255 characters")
                    elif len(description.content) > 3900:
                        await ctx.send("Your description must be less than 3900 characters")
                    elif len(title.content) + len(description.content) > 4000:
                        await ctx.send("You description and title must be below 4000 characters")
                    else:
                        embed = discord.Embed(title=(f"{title.content}"), description=(f'{description.content}'))
                        buttons = [
                            create_button(style=ButtonStyle.green, label="Verify", custom_id="verify"),
                        ]
                        action_row = create_actionrow(*buttons)
                        msg1 = await ctx.send(f"Sending verify message to {channel.mention}")
                        try:
                            await channel.send(embed=embed,
                                components=[action_row]
                            )
                        except:
                            await msg1.edit("There was an error when sending the verification message. Please make sure I have permissions to send messages and embed links in that channel. If this error continues please contact support in the support server.")
                except asyncio.TimeoutError:
                    await ctx.send("You ran out of time, please try again")
            else:  
                embed = discord.Embed(title=(f"Verification"), description=(f'Click the "verify" button on this message to verify.'))
                buttons = [
                    create_button(style=ButtonStyle.green, label="Verify", custom_id="verify"),
                ]
                action_row = create_actionrow(*buttons)

                msg1 = await ctx.send(f"Sending verify message to {channel.mention}")
                try:
                    await channel.send(embed=embed,
                        components=[action_row]
                    )
                except:
                    await msg1.edit("There was an error when sending the verification message. Please make sure I have permissions to send messages and embed links in that channel. If this error continues please contact support in the support server.")




def setup(client):
    client.add_cog(createpanelveri(client))
