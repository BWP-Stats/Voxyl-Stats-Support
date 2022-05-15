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
            logchannel = message.guild.get_channel(948273742700744734)
            if response['attributeScores']['SEVERE_TOXICITY']['summaryScore']['value'] > 0.9:
                await message.delete()
                await message.channel.send(f"{message.author.mention} Your message has been deleted for `SEVERE_TOXICITY`", delete_after=10)
                embed=nextcord.Embed(title="Message Deleted", description=f"{message.author.mention} message has been deleted for `SEVERE_TOXICITY : {response['attributeScores']['SEVERE_TOXICITY']['summaryScore']['value']}`\n\n**Message Content**:\n {message.content[0:3000]}")
                await logchannel.send(embed=embed)
            elif response['attributeScores']['THREAT']['summaryScore']['value'] > 0.85:
                await message.delete()
                await message.channel.send(f"{message.author.mention} Your message has been deleted for `THREAT`", delete_after=10)
                embed=nextcord.Embed(title="Message Deleted", description=f"{message.author.mention} message has been deleted for `THREAT : {response['attributeScores']['THREAT']['summaryScore']['value']}`\n\n**Message Content**:\n {message.content[0:3000]}")
                await logchannel.send(embed=embed)
            elif response['attributeScores']['IDENTITY_ATTACK']['summaryScore']['value'] > 0.85:
                await message.delete()
                await message.channel.send(f"{message.author.mention} Your message has been deleted for `IDENTITY_ATTACK`", delete_after=10)
                embed=nextcord.Embed(title="Message Deleted", description=f"{message.author.mention} message has been deleted for `IDENTITY_ATTACK : {response['attributeScores']['IDENTITY_ATTACK']['summaryScore']['value']}`\n\n**Message Content**:\n {message.content[0:3000]}")
                await logchannel.send(embed=embed)
            elif response['attributeScores']['SEXUALLY_EXPLICIT']['summaryScore']['value'] > 0.85:
                await message.delete()
                await message.channel.send(f"{message.author.mention} Your message has been deleted for `SEXUALLY_EXPLICIT`", delete_after=10)
                embed=nextcord.Embed(title="Message Deleted", description=f"{message.author.mention} message has been deleted for `SEXUALLY_EXPLICIT : {response['attributeScores']['SEXUALLY_EXPLICIT']['summaryScore']['value']}`\n\n**Message Content**:\n {message.content[0:3000]}")
                await logchannel.send(embed=embed)


def setup(client):
    client.add_cog(Events(client))
