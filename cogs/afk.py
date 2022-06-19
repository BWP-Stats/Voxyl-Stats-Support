import nextcord
from nextcord.ext import commands, tasks
from nextcord import Interaction, SlashOption
from nextcord.abc import GuildChannel
import json, sys, os

class Afk(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @nextcord.slash_command(name="afk", description="Set your status to AFK")
    async def afk(
        self,
        ctx : Interaction):
        await ctx.response.defer()
        with open("afk.json", "r") as f:
            data=json.load(f)
        if not str(ctx.user.id) in data["users"]:
            data["users"].append(str(ctx.user.id))
            await ctx.user.edit(nick=f"[AFK] " + ctx.user.nick if ctx.user.nick != None else "[AFK] " + ctx.user.name)
            with open("afk.json", "w+") as f:
                json.dump(data, f)
            await ctx.send("Your are now **AFK**. Redo this command to cancel this")
        else:
            data["users"].remove(str(ctx.user.id))
            await ctx.user.edit(nick=ctx.user.nick.replace("[AFK] ", "") if ctx.user.nick != None and ctx.user.nick.startswith("[AFK] ") else None)
            with open("afk.json", "w+") as f:
                json.dump(data, f)
            await ctx.send("Your are now no longer **AFK**. Redo this command to cancel this")


        


def setup(client):
    client.add_cog(Afk(client))
