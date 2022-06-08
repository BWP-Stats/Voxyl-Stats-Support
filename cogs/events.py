import nextcord, json, pymysql, asyncio
from nextcord.ext import commands, tasks
from nextcord import Interaction, SlashOption
from nextcord.abc import GuildChannel
from googleapiclient import discovery

invc = 0
meminvc = []
beingmoved = []

class SuggestionTypeView(nextcord.ui.View):
    def __init__(self, suggester):
        self.suggester = suggester
        super().__init__(timeout=120)

    @nextcord.ui.button(label="Discord Bot", style=nextcord.ButtonStyle.blurple, custom_id="suggestion_type_discord_bot")
    async def discord_bot_suggestion_type(self, button: nextcord.ui.Button, ctx: nextcord.Interaction):
        if self.suggester == ctx.user.id:
            await ctx.channel.edit(name=f"discordbot-{ctx.channel.name}")
            await ctx.message.delete()
    @nextcord.ui.button(label="Overlay", style=nextcord.ButtonStyle.blurple, custom_id="suggestion_type_overlay")
    async def overlay_suggestion_type(self, button: nextcord.ui.Button, ctx: nextcord.Interaction):
        if self.suggester == ctx.user.id:
            await ctx.channel.edit(name=f"overlay-{ctx.channel.name}")
            await ctx.message.delete()
    @nextcord.ui.button(label="Website", style=nextcord.ButtonStyle.blurple, custom_id="suggestion_type_website")
    async def website_suggestion_type(self, button: nextcord.ui.Button, ctx: nextcord.Interaction):
        if self.suggester == ctx.user.id:
            await ctx.channel.edit(name=f"website-{ctx.channel.name}")
            await ctx.message.delete()
    @nextcord.ui.button(label="In-game Bot", style=nextcord.ButtonStyle.blurple, custom_id="suggestion_type_igbot")
    async def igbot_suggestion_type(self, button: nextcord.ui.Button, ctx: nextcord.Interaction):
        if self.suggester == ctx.user.id:
            await ctx.channel.edit(name=f"igbot-{ctx.channel.name}")
            await ctx.message.delete()

class Events(commands.Cog):

    def __init__(self, client):
        self.client = client
        with open('config.json','r') as jsonfile:
            configData = json.load(jsonfile)
            self.DBUSER = configData["DBUSER"]
            self.DBPASS = configData["DBPASS"]
            self.DBNAME = configData["DBNAME"]
            self.DBENDPOINT = configData["DBENDPOINT"]
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.type is nextcord.MessageType.pins_add and message.author.id == self.client.user.id:
            await message.delete()
        if message.channel.id == 965352171040276500 or message.channel.id == 965360224003326033:
            await message.publish()
        else:
            if message.author.id == self.client.user.id:
                return
            with open("config.json") as f:
                data = json.load(f)

            API_KEY = data["GOOGLE_API_KEY"]
            try:
                client = discovery.build(
                    "commentanalyzer",
                    "v1alpha1",
                    developerKey=API_KEY,
                    discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
                    static_discovery=False,
                )

                analyze_request = {
                    'comment': { 'text': f'{message.content}' },
                    'requestedAttributes': {'SEVERE_TOXICITY': {}, "THREAT": {}, "IDENTITY_ATTACK": {}}
                }

                response = client.comments().analyze(body=analyze_request).execute()
                print(response)
                logchannel = message.guild.get_channel(927304057931038800)
                if response['attributeScores']['SEVERE_TOXICITY']['summaryScore']['value'] > 0.5:
                    await message.delete()
                    await message.channel.send(f"{message.author.mention} Your message has been deleted for `SEVERE_TOXICITY`", delete_after=10)
                    embed=nextcord.Embed(title="Message Deleted", description=f"{message.author.mention} message has been deleted for `SEVERE_TOXICITY : {response['attributeScores']['SEVERE_TOXICITY']['summaryScore']['value']}`\n\n**Message Content**:\n {message.content[0:3000]}")
                    await logchannel.send(embed=embed)
                elif response['attributeScores']['THREAT']['summaryScore']['value'] > 0.5:
                    await message.delete()
                    await message.channel.send(f"{message.author.mention} Your message has been deleted for `THREAT`", delete_after=10)
                    embed=nextcord.Embed(title="Message Deleted", description=f"{message.author.mention} message has been deleted for `THREAT : {response['attributeScores']['THREAT']['summaryScore']['value']}`\n\n**Message Content**:\n {message.content[0:3000]}")
                    await logchannel.send(embed=embed)
                elif response['attributeScores']['IDENTITY_ATTACK']['summaryScore']['value'] > 0.5:
                    await message.delete()
                    await message.channel.send(f"{message.author.mention} Your message has been deleted for `IDENTITY_ATTACK`", delete_after=10)
                    embed=nextcord.Embed(title="Message Deleted", description=f"{message.author.mention} message has been deleted for `IDENTITY_ATTACK : {response['attributeScores']['IDENTITY_ATTACK']['summaryScore']['value']}`\n\n**Message Content**:\n {message.content[0:3000]}")
                    await logchannel.send(embed=embed)
                else:
                    client = discovery.build(
                        "commentanalyzer",
                        "v1alpha1",
                        developerKey=API_KEY,
                        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
                        static_discovery=False,
                    )

                    analyze_request = {
                        'comment': { 'text': f'{message.content}' },
                        'requestedAttributes': {'SEVERE_TOXICITY_EXPERIMENTAL': {}, "THREAT_EXPERIMENTAL": {}, "IDENTITY_ATTACK_EXPERIMENTAL": {}, "SEXUALLY_EXPLICIT": {}}
                    }

                    response = client.comments().analyze(body=analyze_request).execute()
                    print(response)
                    if response['attributeScores']['SEXUALLY_EXPLICIT']['summaryScore']['value'] > 0.5:
                        await message.delete()
                        await message.channel.send(f"{message.author.mention} Your message has been deleted for `SEXUALLY_EXPLICIT`", delete_after=10)
                        embed=nextcord.Embed(title="Message Deleted", description=f"{message.author.mention} message has been deleted for `SEXUALLY_EXPLICIT : {response['attributeScores']['SEXUALLY_EXPLICIT']['summaryScore']['value']}`\n\n**Message Content**:\n {message.content[0:3000]}")
                        await logchannel.send(embed=embed)
                    elif response['attributeScores']['SEVERE_TOXICITY_EXPERIMENTAL']['summaryScore']['value'] > 0.5:
                        await message.delete()
                        await message.channel.send(f"{message.author.mention} Your message has been deleted for `SEVERE_TOXICITY`", delete_after=10)
                        embed=nextcord.Embed(title="Message Deleted", description=f"{message.author.mention} message has been deleted for `SEVERE_TOXICITY_EXPERIMENTAL : {response['attributeScores']['SEXUALLY_EXPLICIT']['summaryScore']['value']}`\n\n**Message Content**:\n {message.content[0:3000]}")
                        await logchannel.send(embed=embed)
                    elif response['attributeScores']['IDENTITY_ATTACK_EXPERIMENTAL']['summaryScore']['value'] > 0.5:
                        await message.delete()
                        await message.channel.send(f"{message.author.mention} Your message has been deleted for `IDENTITY_ATTACK`", delete_after=10)
                        embed=nextcord.Embed(title="Message Deleted", description=f"{message.author.mention} message has been deleted for `IDENTITY_ATTACK_EXPERIMENTAL : {response['attributeScores']['SEXUALLY_EXPLICIT']['summaryScore']['value']}`\n\n**Message Content**:\n {message.content[0:3000]}")
                        await logchannel.send(embed=embed)
                    elif response['attributeScores']['THREAT_EXPERIMENTAL']['summaryScore']['value'] > 0.5:
                        await message.delete()
                        await message.channel.send(f"{message.author.mention} Your message has been deleted for `THREAT`", delete_after=10)
                        embed=nextcord.Embed(title="Message Deleted", description=f"{message.author.mention} message has been deleted for `THREAT_EXPERIMENTAL : {response['attributeScores']['SEXUALLY_EXPLICIT']['summaryScore']['value']}`\n\n**Message Content**:\n {message.content[0:3000]}")
                        await logchannel.send(embed=embed)
            except Exception as e:
                print(e)
                logchannel = message.guild.get_channel(927304057931038800)
                if "kys" in message.content.lower():
                    await message.delete()
                    await message.channel.send(f"{message.author.mention} Your message has been deleted for `THREAT`", delete_after=10)
                    embed=nextcord.Embed(title="Message Deleted", description=f"{message.author.mention} message has been deleted for `THREAT`\n\n**Message Content**:\n {message.content[0:3000]}")
                    await logchannel.send(embed=embed)
        try:
            if not message.author.bot:
                if message.channel.id == 927194633631576124 or message.channel.id == 978381668480061461:
                    thread = await message.channel.create_thread(name=f"suggestion-{message.author}", message=message, auto_archive_duration=10080)
                    await thread.send(f"{message.author.mention} What is your suggestion for?", view=SuggestionTypeView(suggester=message.author.id), delete_after=120)
        except Exception as e:
            print(e)
            pass

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before=None, after=None):
        global invc, beingmoved
        if before.channel:
            if before.channel.category.id == 982291594856255518 and not before.channel.id == 982291673310720082:
                if len(before.channel.members) == 0:
                    conn = pymysql.connect(host=self.DBENDPOINT, port=3306, user=self.DBUSER, password=self.DBPASS, db=self.DBNAME)
                    cur = conn.cursor()
                    cur.execute(f"SELECT * FROM private_calls WHERE channel='{before.channel.id}'")
                    data=cur.fetchall()
                    cur.execute(f"DELETE FROM private_calls WHERE channel='{before.channel.id}'")
                    conn.commit()
                    await before.channel.delete()
                    textchannel = before.channel.guild.get_channel(int(data[0][2]))
                    await textchannel.delete()
        if after.channel:
            if after.channel.id == 982291673310720082:
                if len(after.channel.members) >= 0:
                    conn = pymysql.connect(host=self.DBENDPOINT, port=3306, user=self.DBUSER, password=self.DBPASS, db=self.DBNAME)
                    cur = conn.cursor()
                    cur.execute(f"SELECT * FROM private_calls WHERE owner='{member.id}'")
                    data = cur.fetchall()
                    if data:
                        currentchannel = after.channel.guild.get_channel(int(data[0][1]))
                        await member.move_to(currentchannel)
                        currenttext = after.channel.guild.get_channel(int(data[0][2]))
                        await currenttext.send(f"{member.mention} You have been moved to {currentchannel.mention} as it is the channel you currently own. To make a new channel please transfer this channnel to someone else using `/vc transfer`.")
                    else:
                        category = after.channel.guild.get_channel(982291594856255518)
                        vcchannel = await after.channel.guild.create_voice_channel(name=f"{member.name}'s Private", category=category)
                        textchannel = await after.channel.guild.create_text_channel(name=f"priv-{member.name}", category=category)
                        cur.execute(f"INSERT INTO private_calls (owner, channel, text) VALUES ('{member.id}', '{vcchannel.id}', '{textchannel.id}')")
                        conn.commit()
                        await vcchannel.set_permissions(member, view_channel=True, connect=True, speak=True)
                        await textchannel.set_permissions(member, view_channel=True, send_messages=True, read_messages=True)
                        try:
                            await member.move_to(vcchannel)
                            await after.channel.set_permissions(member, connect=False)
                            embed=nextcord.Embed(title=f"Private Channel", description=f"""Welcome to your private Voice & Text Channel. You can do whatever you want here (within the rules) without anyone disturbing you. Before are a list of commands you can use to manage your private channels:
                        
`/vc invite <member>` - Invite a member to join your channels
`/vc block <member>` - Block a member from your channels
`/vc public` - Make your **voice** channel public. (Won't affect your text channel)
`/vc private` - Make your **voice** channel private so only people you invite can join""")
                            embed.set_footer(text="Private channels from Voxyl Stats")
                            await textchannel.send(f"{member.mention}", embed=embed)
                            await asyncio.sleep(10)
                            await after.channel.set_permissions(member, overwrite=None)
                        except:
                            cur.execute(f"DELETE FROM private_calls WHERE channel='{vcchannel.id}'")
                            conn.commit()
                            await vcchannel.delete()
                            await textchannel.delete()
                            await after.channel.set_permissions(member, connect=False)
                            await asyncio.sleep(10)
                            await after.channel.set_permissions(member, overwrite=None)
                            return



def setup(client):
    client.add_cog(Events(client))
