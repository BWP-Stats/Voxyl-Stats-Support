import nextcord
from nextcord.ext import commands, tasks
from nextcord import Interaction, SlashOption
from nextcord.abc import GuildChannel
import json, sys, os


class Dropdown(nextcord.ui.Select):
    def __init__(self):
        options = [
            nextcord.SelectOption(
                label="Announcement Pings", description="Get mentioned for any announcements"
            ),
            nextcord.SelectOption(
                label="Update Pings", description="Get mentioned when there are any new updates"
            ),
            nextcord.SelectOption(
                label="Downtime Pings", description="Get mentioned when there is any downtime with a system"
            ),
            nextcord.SelectOption(
                label="Giveaway Pings", description="Gte mentioned when there is a giveaway"
            ),
            nextcord.SelectOption(
                label="Poll Pings", description="Get mentioned when we run a poll"
            ),
            nextcord.SelectOption(
                label="Sneak Peak Pings", description="Get mentioned for any sneak peaks of future updates"
            )
        ]
        super().__init__(
            placeholder="Choose which roles you want to be given",
            min_values=1,
            max_values=6,
            options=options,
            custom_id="role_menu_dropdown"
        )

    async def callback(self, ctx: nextcord.Interaction):
        await ctx.response.defer(with_message=False)
        announcements = ctx.guild.get_role(927195791553101825)
        updates = ctx.guild.get_role(927195836046254091)
        downtime = ctx.guild.get_role(927597867231748186)
        giveaway = ctx.guild.get_role(929423518456750122)
        poll = ctx.guild.get_role(928361908409610291)
        sneak_peak = ctx.guild.get_role(929440986814382141)
        adding = []
        removing = []
        if "Announcement Pings" in self.values:
            adding.append(announcements)
        else:
            removing.append(announcements)
        if "Update Pings" in self.values:
            adding.append(updates)
        else:
            removing.append(updates)
        if "Downtime Pings" in self.values:
            adding.append(downtime)
        else:
            removing.append(downtime)
        if "Giveaway Pings" in self.values:
            adding.append(giveaway)
        else:
            removing.append(giveaway)
        if "Poll Pings" in self.values:
            adding.append(poll)
        else:
            removing.append(poll)
        if "Sneak Peak Pings" in self.values:
            adding.append(sneak_peak)
        else:
            removing.append(sneak_peak)
        await ctx.user.add_roles(*adding, atomic=False)
        await ctx.user.remove_roles(*removing, atomic=True)

class RoleClearButton(nextcord.ui.Button):
    def __init__(self):
        super().__init__(label="Clear Roles", custom_id="clearroles", style=nextcord.ButtonStyle.red)
    
    async def callback(self, ctx: nextcord.Interaction):
        announcements = ctx.guild.get_role(927195791553101825)
        updates = ctx.guild.get_role(927195836046254091)
        downtime = ctx.guild.get_role(927597867231748186)
        giveaway = ctx.guild.get_role(929423518456750122)
        poll = ctx.guild.get_role(928361908409610291)
        sneak_peak = ctx.guild.get_role(929440986814382141)
        removing = [announcements, updates, downtime, giveaway, poll, sneak_peak]
        await ctx.user.remove_roles(*removing, atomic=False)
class RoleAddButton(nextcord.ui.Button):
    def __init__(self):
        super().__init__(label="Add All Roles", custom_id="addroles", style=nextcord.ButtonStyle.green)
    
    async def callback(self, ctx: nextcord.Interaction):
        announcements = ctx.guild.get_role(927195791553101825)
        updates = ctx.guild.get_role(927195836046254091)
        downtime = ctx.guild.get_role(927597867231748186)
        giveaway = ctx.guild.get_role(929423518456750122)
        poll = ctx.guild.get_role(928361908409610291)
        sneak_peak = ctx.guild.get_role(929440986814382141)
        adding = [announcements, updates, downtime, giveaway, poll, sneak_peak]
        await ctx.user.add_roles(*adding, atomic=False)

class RoleMenuView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        self.add_item(Dropdown())
        self.add_item(RoleAddButton())
        self.add_item(RoleClearButton())


class SendRoleMenu(commands.Cog):

    def __init__(self, client):
        self.client = client

    

    @nextcord.slash_command(name="sendrolemenu", description="Send the role menu to a channel")
    async def sendrolemenu(
        self,
        ctx : Interaction,
        channel: GuildChannel = SlashOption(
            name="channel",
            description="Channel to send the role menu to",
            required=True,
            channel_types=[nextcord.ChannelType.text]
        ),
        ):
        if ctx.user.guild_permissions.administrator:
            await ctx.response.defer()
            await channel.send("Select the roles you want below", view=RoleMenuView())

        
        


def setup(client):
    client.add_cog(SendRoleMenu(client))
