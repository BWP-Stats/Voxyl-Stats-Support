import nextcord
from nextcord.ext import commands, tasks
from nextcord import Interaction, SlashOption
from nextcord.abc import GuildChannel
import json, sys, os

class TicketManagementView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(label="close", style=nextcord.ButtonStyle.red, custom_id="ticket_management_view:close")
    async def close_ticket(self, button: nextcord.ui.Button, ctx: nextcord.Interaction):
        with open("ticketinfo.json") as f:
            data=json.load(f)
        ownerid = data["channels"][f"{ctx.channel.id}"]["ownerid"]
        del data["channels"][f"{ctx.channel.id}"]
        index = data["users"].index(ownerid)
        del data["users"][index]
        with open("ticketinfo.json", "w") as f:
            json.dump(data, f)
        logchannel = ctx.guild.get_channel(927304057931038800)
        sys.stdout = open(f"ticket-transcript-{ownerid}.txt", "w+")
        async for message in ctx.channel.history(oldest_first = True):
            print(f"{message.author}: {message.content}")

        message = await ctx.channel.history().flatten()
        sys.stdout.close()
        embed=nextcord.Embed(title="Ticket closed", description=f"Closed By <@{ctx.user.id}> ({ctx.user.id})\nCreate By <@{ownerid}> ({ownerid})")
        await logchannel.send(embed=embed, file=nextcord.File(f"ticket-transcript-{ownerid}.txt"))
        os.remove(f"ticket-transcript-{ownerid}.txt")
        await ctx.channel.delete()


class TicketsView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(label='Ticket', style=nextcord.ButtonStyle.blurple, custom_id='tickets_view:create')
    async def create_ticket(self, button: nextcord.ui.Button, ctx: nextcord.Interaction):
        with open("ticketinfo.json") as f:
            data=json.load(f)
        if ctx.user.id in data["users"]:
            await ctx.send("You already have a ticket open. Please use that ticket instead of creating a new one", ephemeral=True)
            return
        else:
            await ctx.response.defer(with_message=True, ephemeral=True)
            data["users"].append(ctx.user.id)
            supcat = ctx.guild.get_channel(927304036078723122)
            channel = await ctx.guild.create_text_channel(name=f"support-{ctx.user.id}", category=supcat)
            channels = data["channels"]
            channels[channel.id] = {"ownerid" : ctx.user.id}
            with open("ticketinfo.json", "w") as f:
                json.dump(data, f)
            embed=nextcord.Embed(title="Support", description=f"""Welcome to your ticket {ctx.user.mention}
            
Please explain any questions you have and a member of staff will help you as soon as possible""")
            contmsg = await channel.send(f"{ctx.user.mention}", embed=embed, view=TicketManagementView())
            await contmsg.pin()
            await channel.set_permissions(ctx.user, send_messages=True, read_messages=True, attach_files=True, embed_links=True)
            await ctx.send(f"Ticket created in {channel.mention}", ephemeral=True)

class Tickets(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @nextcord.slash_command(name="sendticket", description="Send a ticket message to a channel", guild_ids=[926955080010301480])
    async def send_ticket(self,
        ctx : Interaction,
        channel : GuildChannel = SlashOption(
            name="channel",
            description="Channel to send embed to",
            required=True,
            channel_types=[nextcord.ChannelType.text]
        )):
        if ctx.user.guild_permissions.administrator == True:
            embed=nextcord.Embed(title="Support", description=f"Click the button bellow to open a support ticket.")
            await channel.send(embed=embed, view=TicketsView())
            await ctx.send("Embed sent", ephemeral=True)
        else:
            await ctx.send("You don't have permission to use that", ephemeral=True)
        


def setup(client):
    client.add_cog(Tickets(client))
