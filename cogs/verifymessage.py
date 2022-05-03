import nextcord
from nextcord.ext import commands, tasks
from nextcord import Interaction, SlashOption
from nextcord.abc import GuildChannel
import json, sys, os



class VerifyView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(label='Verify', style=nextcord.ButtonStyle.blurple, custom_id='verify_view:verify')
    async def create_ticket(self, button: nextcord.ui.Button, ctx: nextcord.Interaction):
        role = ctx.guild.get_role(926955604738707597)
        if not role in ctx.user.roles:
            ctx.user.add_roles(926955604738707597)
            await ctx.send("Successfully verified", ephemeral=True)
        else:
            await ctx.send("You are already verified", ephemeral=True)

class Verify(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @nextcord.slash_command(name="sendverify", description="Send a verification message to a channel", guild_ids=[926955080010301480])
    async def send_ticket(self,
        ctx : Interaction,
        channel : GuildChannel = SlashOption(
            name="channel",
            description="Channel to send embed to",
            required=True,
            channel_types=[nextcord.ChannelType.text]
        )):
        if ctx.user.guild_permissions.administrator == True:
            embed=nextcord.Embed(title="Verify", description=f"Click the button bellow to verify")
            await channel.send(embed=embed, view=VerifyView())
            await ctx.send("Embed sent", ephemeral=True)
        else:
            await ctx.send("You don't have permission to use that", ephemeral=True)
        


def setup(client):
    client.add_cog(Verify(client))
