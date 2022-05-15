import nextcord, json
from nextcord.ext import commands, tasks
from nextcord import Interaction, SlashOption
from nextcord.abc import GuildChannel
from googleapiclient import discovery

class Events(commands.Cog):

    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == 965352171040276500 or message.channel.id == 965360224003326033:
            await message.publish()
        else:
            if message.author.id == self.client.user.id:
                return
            with open("config.json") as f:
                data = json.load(f)
                API_KEY = data["GOOGLE_API_KEY"]

            client = discovery.build(
                "commentanalyzer",
                "v1alpha1",
                developerKey=API_KEY,
                discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
                static_discovery=False,
            )

            analyze_request = {
                'comment': { 'text': f'{message.content}' },
                'requestedAttributes': {'SEVERE_TOXICITY': {}, "THREAT": {}, "IDENTITY_ATTACK": {}, "SEXUALLY_EXPLICIT": {}}
            }

            response = client.comments().analyze(body=analyze_request).execute()
            print(json.dumps(response, indent=2))
            if response['attributeScores']['SEVERE_TOXICITY']['summaryScore']['value'] > 0.9:
                await message.reply("Would delete with a value of: {} for SEVERE_TOXICITY".format(response['attributeScores']['SEVERE_TOXICITY']['summaryScore']['value']))
            elif response['attributeScores']['THREAT']['summaryScore']['value'] > 0.85:
                await message.reply("Would delete with a value of: {} for THREAT".format(response['attributeScores']['THREAT']['summaryScore']['value']))
            elif response['attributeScores']['IDENTITY_ATTACK']['summaryScore']['value'] > 0.85:
                await message.reply("Would delete with a value of: {} for IDENTITY_ATTACK".format(response['attributeScores']['IDENTITY_ATTACK']['summaryScore']['value']))
            elif response['attributeScores']['SEXUALLY_EXPLICIT']['summaryScore']['value'] > 0.85:
                await message.reply("Would delete with a value of: {} for SEXUALLY_EXPLICIT".format(response['attributeScores']['SEXUALLY_EXPLICIT']['summaryScore']['value']))
            else:
                message.reply("Would not delete")


def setup(client):
    client.add_cog(Events(client))
