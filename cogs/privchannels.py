import nextcord
from nextcord.ext import commands, tasks
from nextcord import Interaction, SlashOption
import json, pymysql

class PrivateCalls(commands.Cog):

    def __init__(self, client):
        self.client = client
        with open('config.json','r') as jsonfile:
            configData = json.load(jsonfile)
            self.DBUSER = configData["DBUSER"]
            self.DBPASS = configData["DBPASS"]
            self.DBNAME = configData["DBNAME"]
            self.DBENDPOINT = configData["DBENDPOINT"]

    @nextcord.slash_command(name="vc", description="VC Base Command")
    async def vc(ctx:Interaction):
        pass
    
    @vc.subcommand(name="invite", description="Invite someone to your private channel")
    async def invite_to_call(self,
        ctx: Interaction,
        member : nextcord.Member = SlashOption(
            name="member",
            description="Member to invite to call",
            required=True
        ),
        member2 : nextcord.Member = SlashOption(
            name="member2",
            description="Member to invite to call",
            required=False
        ),
        member3 : nextcord.Member = SlashOption(
            name="member3",
            description="Member to invite to call",
            required=False
        ),
        member4 : nextcord.Member = SlashOption(
            name="member4",
            description="Member to invite to call",
            required=False
        ),
        member5 : nextcord.Member = SlashOption(
            name="member5",
            description="Member to invite to call",
            required=False
        ),
        member6 : nextcord.Member = SlashOption(
            name="member6",
            description="Member to invite to call",
            required=False
        ),
        member7 : nextcord.Member = SlashOption(
            name="member7",
            description="Member to invite to call",
            required=False
        ),
        member8 : nextcord.Member = SlashOption(
            name="member8",
            description="Member to invite to call",
            required=False
        ),
        member9 : nextcord.Member = SlashOption(
            name="member9",
            description="Member to invite to call",
            required=False
        )):
        await ctx.response.defer()
        conn = pymysql.connect(host=self.DBENDPOINT, port=3306, user=self.DBUSER, password=self.DBPASS, db=self.DBNAME)
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM private_calls WHERE owner='{ctx.user.id}'")
        data= cur.fetchall()
        if data:
            channel = ctx.guild.get_channel(int(data[0][1]))
            textchannel = ctx.guild.get_channel(int(data[0][2]))
            if member2 or member3 or member4 or member5 or member6 or member7 or member8 or member9:
                await channel.set_permissions(member, view_channel=True, connect=True, speak=True)
                await textchannel.set_permissions(member, view_channel=True, send_messages=True, read_messages=True)
                msgsofar = f"\nYou have invited {member.mention} to {channel.mention}"
                msg = await ctx.send("Inviting...")
                if member2:
                    await channel.set_permissions(member2, view_channel=True, connect=True, speak=True)
                    await textchannel.set_permissions(member2, view_channel=True, send_messages=True, read_messages=True)
                    msgsofar = msgsofar + f"\nYou have invited {member2.mention} to {channel.mention}"
                if member3:
                    await channel.set_permissions(member3, view_channel=True, connect=True, speak=True)
                    await textchannel.set_permissions(member3, view_channel=True, send_messages=True, read_messages=True)
                    msgsofar = msgsofar + f"\nYou have invited {member3.mention} to {channel.mention}"
                if member4:
                    await channel.set_permissions(member4, view_channel=True, connect=True, speak=True)
                    await textchannel.set_permissions(member4, view_channel=True, send_messages=True, read_messages=True)
                    msgsofar = msgsofar + f"\nYou have invited {member4.mention} to {channel.mention}"
                if member5:
                    await channel.set_permissions(member5, view_channel=True, connect=True, speak=True)
                    await textchannel.set_permissions(member5, view_channel=True, send_messages=True, read_messages=True)
                    msgsofar = msgsofar + f"\nYou have invited {member5.mention} to {channel.mention}"
                if member6:
                    await channel.set_permissions(member6, view_channel=True, connect=True, speak=True)
                    await textchannel.set_permissions(member6, view_channel=True, send_messages=True, read_messages=True)
                    msgsofar = msgsofar + f"\nYou have invited {member6.mention} to {channel.mention}"
                if member7:
                    await channel.set_permissions(member7, view_channel=True, connect=True, speak=True)
                    await textchannel.set_permissions(member7, view_channel=True, send_messages=True, read_messages=True)
                    msgsofar = msgsofar + f"\nYou have invited {member7.mention} to {channel.mention}"
                if member8:
                    await channel.set_permissions(member8, view_channel=True, connect=True, speak=True)
                    await textchannel.set_permissions(member8, view_channel=True, send_messages=True, read_messages=True)
                    msgsofar = msgsofar + f"\nYou have invited {member8.mention} to {channel.mention}"
                if member9:
                    await channel.set_permissions(member9, view_channel=True, connect=True, speak=True)
                    await textchannel.set_permissions(member9, view_channel=True, send_messages=True, read_messages=True)
                    msgsofar = msgsofar + f"\nYou have invited {member9.mention} to {channel.mention}"
                await msg.edit(content=msgsofar)
                return
                
            if not member.id == int(data[0][0]):
                await channel.set_permissions(member, view_channel=True, connect=True, speak=True)
                await textchannel.set_permissions(member, view_channel=True, send_messages=True, read_messages=True)
                await ctx.send(f"You have invited {member.mention} to {channel.mention}")
            else:
                await ctx.send("You can't invite yourself to your own channel")
        else:
            await ctx.send("You must be the owner of a channel to use that")
    @vc.subcommand(name="block", description="Block someone from your private channel")
    async def kick_from_call(self,
        ctx: Interaction,
        member : nextcord.Member = SlashOption(
            name="member",
            description="Member to invite to call",
            required=True
        )):
        await ctx.response.defer()
        conn = pymysql.connect(host=self.DBENDPOINT, port=3306, user=self.DBUSER, password=self.DBPASS, db=self.DBNAME)
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM private_calls WHERE owner='{ctx.user.id}'")
        data= cur.fetchall()
        if data:
            if not member.id == int(data[0][0]):
                channel = ctx.guild.get_channel(int(data[0][1]))
                textchannel = ctx.guild.get_channel(int(data[0][2]))
                await channel.set_permissions(member, view_channel=False, connect=False, speak=False)
                await textchannel.set_permissions(member, view_channel=False, send_messages=False, read_messages=False)
                if member in channel.members:
                    await member.move_to(None)
                await ctx.send(f"You have blocked {member.mention} from {channel.mention}")
            else:
                await ctx.send("You can't block yourself from your own channel")
        else:
            await ctx.send("You must be the owner of a channel to use that")
    @vc.subcommand(name="public", description="Make you call public so anyone can join")
    async def public_call(self,
        ctx: Interaction):
        await ctx.response.defer()
        conn = pymysql.connect(host=self.DBENDPOINT, port=3306, user=self.DBUSER, password=self.DBPASS, db=self.DBNAME)
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM private_calls WHERE owner='{ctx.user.id}'")
        data= cur.fetchall()
        if data:
            channel = ctx.guild.get_channel(int(data[0][1]))
            role = ctx.guild.get_role(926955604738707597)
            await channel.set_permissions(role, view_channel=True, connect=True, speak=True)
            await ctx.send(f"You have made {channel.mention} public so anyone can join. *Please Note: You will still need to `/vc invite` anyone you want to have access to your text channel*")
        else:
            await ctx.send("You must be the owner of a channel to use that")
    @vc.subcommand(name="private", description="Make you call private so only people you invite can join")
    async def private_call(self,
        ctx: Interaction):
        await ctx.response.defer()
        conn = pymysql.connect(host=self.DBENDPOINT, port=3306, user=self.DBUSER, password=self.DBPASS, db=self.DBNAME)
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM private_calls WHERE owner='{ctx.user.id}'")
        data= cur.fetchall()
        if data:
            channel = ctx.guild.get_channel(int(data[0][1]))
            role = ctx.guild.get_role(926955604738707597)
            await channel.set_permissions(role, view_channel=False, connect=False, speak=False)
            await ctx.send(f"You have made {channel.mention} private so only people you invite can join")
        else:
            await ctx.send("You must be the owner of a channel to use that")
    @vc.subcommand(name="transfer", description="Transfer ownership of your private channel to someone else")
    async def transfer_call(self,
        ctx: Interaction,
        member : nextcord.Member = SlashOption(
            name="member",
            description="Member to transfer call to",
            required=True
        )):
        await ctx.response.defer()
        if member == ctx.user:
            await ctx.send("You can't transfer the call to yourself")
            return
        conn = pymysql.connect(host=self.DBENDPOINT, port=3306, user=self.DBUSER, password=self.DBPASS, db=self.DBNAME)
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM private_calls WHERE owner='{ctx.user.id}'")
        data= cur.fetchall()
        if data:
            channel = ctx.guild.get_channel(int(data[0][1]))
            if member in channel.members:
                cur.execute(f"UPDATE private_calls SET owner='{member.id}' WHERE owner='{ctx.user.id}'")
                conn.commit()
                await ctx.send(f"You have transferred ownership of your private channel to {member.mention}")
            else:
                await ctx.send(f"You need to transfer the channel to someone else in the voice call")
        else:
            await ctx.send("You must be the owner of a channel to use that")


def setup(client):
    client.add_cog(PrivateCalls(client))