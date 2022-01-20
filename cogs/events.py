import discord
from discord.ext import commands, tasks
import json
import asyncio
import datetime
from better_profanity import profanity
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.utils.manage_components import create_select, create_select_option, create_actionrow
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.utils.manage_components import wait_for_component


profanity.load_censor_words_from_file("./filter.txt")
logchannel = 927304057931038800

class Events(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    #@commands.command()
    #async def test(self, ctx):
        #await ctx.send("eeeeeeeeeeeeeeeeeeee")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if not message.author.bot == True:
            channel = self.client.get_channel(logchannel)
            em = discord.Embed(title=f"Message deleted in {message.channel.mention}", description=f"""Message Content: {message.content}""", timestamp=message.created_at)
            em.set_author(name=message.author, icon_url=message.author.avatar_url)
            em.set_footer(text=f"{message.author.id}")
            await channel.send(embed=em)
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if not before.author.bot == True:
            channel = self.client.get_channel(logchannel)
            em = discord.Embed(title=f"Message editted in {before.channel.mention}", description=f"\u200b", timestamp=before.created_at)
            em.add_field(name="Before", value=f"{before.content[:1000]}")
            em.add_field(name="After", value=f"{after.content[:1000]}")
            em.set_author(name=before.author, icon_url=before.author.avatar_url)
            em.set_footer(text=f"{before.author.id}")
            await channel.send(embed=em)
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.client.get_channel(logchannel)
        now = datetime.datetime.now()
        secs = (now - member.created_at).days
        days = 3
        if secs < days:
            try:
                await member.send(f"You were kicked from **Voxyl Stats** due to your account age being below 3 days.")
            except:
                pass
            await member.kick(reason=f"Account age below server limit of {days} days")
            embed = discord.Embed(title=f"Member Kicked", description=f"{member.mention} ({member.id}) was kicked from the server due to their account being below the server limit of 3 days")
            await logchannel.send(embed=embed)
        else:
            em = discord.Embed(title=f"Member Joined", description=f"""Tag: {member}
Mention: {member.mention}
ID: {member.id}
Account Age: {member.created_at}""", colour=0x00FF00)
            em.set_author(name=member, icon_url=member.avatar_url)
            await channel.send(embed=em)
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.client.get_channel(logchannel)
        em = discord.Embed(title=f"Member Left", description=f"""Tag: {member}
Mention: {member.mention}
ID: {member.id}""", colour=0xFF0000)
        em.set_author(name=member, icon_url=member.avatar_url)
        await channel.send(embed=em)
    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            if profanity.contains_profanity(message.content):
                await message.delete()
                msg = await message.channel.send(f"{message.author.mention} you can't say that word.")
                await asyncio.sleep(3)
                await msg.delete()



def setup(client):
    client.add_cog(Events(client))
