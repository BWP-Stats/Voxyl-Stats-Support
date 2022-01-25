import discord
import json
import os
from discord.ext import commands , tasks
from discord_slash import SlashCommand, SlashContext
import requests
os.chdir("./")

intents = discord.Intents.default()


async def create_thread(self,name,minutes,message):
    token = 'Bot ' + self._state.http.token
    url = f"https://discord.com/api/v9/channels/{self.id}/messages/{message.id}/threads"
    headers = {
        "authorization" : token,
        "content-type" : "application/json"
    }
    data = {
        "name" : name,
        "type" : 11,
        "auto_archive_duration" : minutes
    }
 
    return requests.post(url,headers=headers,json=data).json()


intents.members = True
client = commands.Bot(command_prefix = "s!", intents = intents)
discord.TextChannel.create_thread = create_thread
slash = SlashCommand(client, sync_commands=True, sync_on_cog_reload=True)

client.remove_command("help")




for filename in os.listdir('./cogs'):   
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
        print(f"Loaded {filename} cog")



@client.event
async def on_ready():
    print ("Voxyl Stats Support Ready")

    print(f"Logged in as {client.user}!")

    await client.change_presence(status = discord.Status.online, activity=discord.Activity(type=discord.ActivityType.playing, name="voxyl.net"))





















client.run("ODkwNzIzOTU1Nzc2ODE5Mjgw.YUz9Uw.zljMGP8fS1H6QgbjcXZ8bFGn41Q")
