import discord
from discord.ext import commands, tasks
import sqlite3
import asyncio
import os
import json
import sys
import random
import string
from captcha.image import ImageCaptcha
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.utils.manage_components import create_select, create_select_option, create_actionrow
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.utils.manage_components import wait_for_component

on_role_cooldown = []


class Oncomp(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    #@commands.command()
    #async def test(self, ctx):
        #await ctx.send("eeeeeeeeeeeeeeeeeeee")

    @commands.Cog.listener()
    async def on_component(self, ctx):
        with open("ticketinfo.json") as f:
            data=json.load(f)
        if ctx.component["custom_id"] == "dbsup":
            if ctx.author.id in data["botusers"]:
                await ctx.send("You already have a ticket of this type open. Please use that ticket instead of creating a new one", hidden=True)
                return
            else:
                await ctx.defer(hidden=True)
                data["botusers"].append(ctx.author.id)
                supcat = ctx.guild.get_channel(927304036078723122)
                channel = await ctx.guild.create_text_channel(name=f"bot-{ctx.author.id}", category=supcat)
                channels = data["channels"]
                channels[channel.id] = {"ownerid" : ctx.author.id, "type" : "bot"}
                with open("ticketinfo.json", "w") as f:
                    json.dump(data, f)
                embed=discord.Embed(title="Discord Bot Support", description=f"""Welcome to your ticket {ctx.author.mention}
                
Please explain any questions you have and a member of staff will help you as soon as possible""")
                buttons = [
                    create_button(style=ButtonStyle.red, label="Close", custom_id="close")
                ]
                await channel.send(embed=embed, components=[create_actionrow(*buttons)])
                await channel.set_permissions(ctx.author, send_messages=True, read_messages=True, attach_files=True, embed_links=True)
                await ctx.send(f"Ticket created in {channel.mention}", hidden=True)
        elif ctx.component["custom_id"] == "close":
            ownerid = data["channels"][f"{ctx.channel.id}"]["ownerid"]
            del data["channels"][f"{ctx.channel.id}"]
            index = data["botusers"].index(ownerid)
            del data["botusers"][index]
            with open("ticketinfo.json", "w") as f:
                json.dump(data, f)
            logchannel = ctx.guild.get_channel(927304057931038800)
            sys.stdout = open(f"ticket-transcript-{ownerid}.txt", "w+")
            async for message in ctx.channel.history(oldest_first = True):
                print(f"{message.author}: {message.content}")

            message = await ctx.channel.history().flatten()
            sys.stdout.close()
            embed=discord.Embed(title="Ticket closed", description=f"Closed By <@{ctx.author.id}> ({ctx.author.id})\nCreate By <@{ownerid}> ({ownerid})")
            await logchannel.send(embed=embed, file=discord.File(f"ticket-transcript-{ownerid}.txt"))
            os.remove(f"ticket-transcript-{ownerid}.txt")
            await ctx.channel.delete()
        elif ctx.component["custom_id"] == "verify":
            role = ctx.guild.get_role(926955604738707597)
            if role in ctx.author.roles:
                await ctx.send("You are already verified", hidden=True)
            else:
                await ctx.author.add_roles(role)
                await ctx.send("You have been successfully verified", hidden=True)
                

            
        



def setup(client):
    client.add_cog(Oncomp(client))