import discord
from discord.ext import commands, tasks
import asyncio
import random
import json
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_commands import create_option, create_choice


class Tags(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @cog_ext.cog_subcommand(base="tag", 
        name="create",
        description="Create a new tag",
        options=[
            create_option(
                name="name",
                description="Tag name",
                option_type=str,
                required=True
            )
        ]
    )
    async def _tag_create(self, ctx:SlashContext, name:str):
        if ctx.author.guild_permissions.administrator == True:
            
            def check(message):
                return message.author == ctx.author and message.channel == ctx.channel
            await ctx.send("What do you want the description to be?")
            description = await self.client.wait_for("message", check=check)
            if len(description.content) > 3900:
                await ctx.send("Your description must be less than 4000 characters", hidden=True)
            else:
                with open("tags.json") as f:
                    data=json.load(f)
                tags = data["tags"]
                if name in data["tags"]:
                    await ctx.send("That is already a tag name. Please choose a different name.")
                    return
                tags[name] = {"name" : name, "description" : description.content}
                with open("tags.json", "w") as f:
                    json.dump(data, f)
                await ctx.send("Successfully created tag")
        else:
            await ctx.send("You need ``administrator`` permission to complete this command", hidden=True)
    @cog_ext.cog_subcommand(base="tag", 
        name="use",
        description="Use a tag",
        options=[
            create_option(
                name="name",
                description="Tag name",
                option_type=str,
                required=True
            ),
            create_option(
                name="member",
                description="Member to mention (Dev only)",
                option_type=discord.Member,
                required=False
            )
        ]
    )
    async def _tag_use(self, ctx:SlashContext, name:str, member:discord.Member=None):
        role = ctx.guild.get_role(926955425704869938)
        with open("tags.json") as f:
            data = json.load(f)
        if name in data["tags"]:
            desc = data["tags"][name]["description"]
            embed=discord.Embed(title=f"{name}", description=desc)
            if not role in ctx.author.roles or member == None:
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"{member.mention}", embed=embed)
    @cog_ext.cog_subcommand(base="tag", 
        name="list",
        description="Get a list of current tags",
    )
    async def _tag_list(self, ctx:SlashContext):
        with open("tags.json") as f:
            data = json.load(f)
        taglist = ""
        for ctag in data["tags"]:
            taglist = taglist + "\n - " + data["tags"][ctag]["name"]
        embed=discord.Embed(title="Tag list", description=f"{taglist}")
        await ctx.send(embed=embed)

    @cog_ext.cog_subcommand(base="tag", 
        name="remove",
        description="Remove a tag",
        options=[
            create_option(
                name="name",
                description="Tag name",
                option_type=str,
                required=True
            )
        ]
    )
    async def _tag_remove(self, ctx:SlashContext, name:str):
        if ctx.author.guild_permissions.administrator == True:
            with open("tags.json") as f:
                data = json.load(f)
            if name in data["tags"]:
                del data["tags"][name]
                with open("tags.json", "w") as f:
                    json.dump(data, f)
                await ctx.send("Successfully removed tag")
            else:
                await ctx.send("Tag not found")
        else:
            await ctx.send("You need ``administrator`` permission to complete this command", hidden=True)
    





    #@commands.Cog.listener()




def setup(client):
    client.add_cog(Tags(client))