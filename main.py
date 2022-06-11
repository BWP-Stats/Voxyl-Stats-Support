import nextcord
import json
import os
from cogs.tickets import TicketsView, TicketManagementView, FAQView
from cogs.verifymessage import VerifyView
from cogs.rolemenu import RoleMenuView
from nextcord.ext import commands , tasks
import requests

os.chdir("./")

class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.persistent_views_added = False
        self = self

    async def on_ready(self):
        if not self.persistent_views_added:
            self.add_view(TicketsView())
            self.add_view(TicketManagementView())
            self.add_view(VerifyView())
            self.add_view(FAQView())
            self.add_view(RoleMenuView())
            self.persistent_views_added = True

        print(f"Logged in as {client.user}!")

        await client.change_presence(status = nextcord.Status.online, activity=nextcord.Activity(type=nextcord.ActivityType.playing, name="Support"))

with open('config.json','r') as jsonfile:
    configData = json.load(jsonfile)
    TOKEN = configData["TOKEN"]

intents = nextcord.Intents.default()

intents.members = True
client = Bot(command_prefix = "nom!", intents = intents)

for filename in os.listdir('./cogs'):   
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
        print(f"Loaded {filename} cog")

client.run(TOKEN)














client.run(TOKEN)
