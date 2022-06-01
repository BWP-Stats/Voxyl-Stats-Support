import nextcord
from nextcord.ext import commands, tasks
from nextcord import Interaction, SlashOption
from nextcord.abc import GuildChannel
import json, sys, os

class Settings(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @nextcord.slash_command(name="admin", description="Base admin cmd")
    async def admin(ctx : Interaction):
        pass

    @admin.subcommand(name="setfaq", description="Set the faq message")
    async def setfaq(
        self,
        ctx : Interaction,
        type: str = SlashOption(
            name="type",
            description="Type of faq to change",
            required=True,
            choices={"discordbot": "bot", "overlay": "overlay",  "website": "web", "ingamebot": "igbot"}
        )):
        role = ctx.guild.get_role(926955425704869938)
        if role in ctx.user.roles or ctx.user.guild_permissions.administrator:
            await ctx.response.defer()
            await ctx.send("Please send the message you want to set")
            msg = await self.client.wait_for("message", check=lambda m: m.author == ctx.user)
            with open("config.json", "r") as f:
                data=json.load(f)
            data[str(type)] = msg.content
            with open("config.json", "w+") as f:
                json.dump(data, f)
            await ctx.send("Successfully set the faq", ephemeral=True)
        else:
            await ctx.send("You don't have permission to run this command", ephemeral=True)
        


def setup(client):
    client.add_cog(Settings(client))
