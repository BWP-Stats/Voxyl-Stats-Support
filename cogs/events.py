import nextcord
from nextcord.ext import commands, tasks
from nextcord import Interaction, SlashOption
from nextcord.abc import GuildChannel

class Events(commands.Cog):

    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == 965352171040276500 or message.channel.id == 965360224003326033:
            await message.publish()
        else:
            pass


def setup(client):
    client.add_cog(Events(client))
