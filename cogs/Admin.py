import datetime
import nextcord
from nextcord.ext import commands, application_checks
from nextcord import Interaction, SlashOption
from keys import testServerId


class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="purge", description="Purge specified number of lines")
    @application_checks.has_permissions(administrator=True)
    async def purge(self, interaction: Interaction,
                    lines: int = SlashOption(description="Enter a number of lines to be purged")):
        await interaction.channel.purge(limit=lines)
        await interaction.response.send_message(f"{interaction.user.mention} Purged {lines} line(s)", ephemeral=True)

    @purge.error
    async def purge_error(self, interaction: Interaction, error):
        if isinstance(error, application_checks.ApplicationMissingPermissions):
            await interaction.response.send_message(f"{interaction.user.mention} Error. Insufficient permissions",
                                                    ephemeral=True)

    @nextcord.slash_command(name="userinfo", description="Find a user's profile info")
    @application_checks.has_permissions(administrator=True)
    async def userinfo(self, interaction: Interaction, user: nextcord.Member = SlashOption(description="Choose member")):
        embed = nextcord.Embed(title=user.name, color=nextcord.Color.blue(), timestamp=datetime.datetime.now())
        userData = {
            "User": user.mention,
            "Nickname": user.nick,
            "Created": user.created_at.strftime("%b %d, %Y, %T"),
            "Joined": user.joined_at.strftime("%b %d, %Y, %T"),
            "Server": user.guild,
            "Top Role": user.top_role
        }
        for [fieldName, fieldVal] in userData.items():
            embed.add_field(name=fieldName+":", value=fieldVal, inline=True)
        embed.set_footer(text=f"id: {user.id}")
        embed.set_thumbnail(user.display_avatar)
        await interaction.send(embed=embed, ephemeral=True)

    @userinfo.error
    async def userinfo_error(self, interaction: Interaction, error):
        if isinstance(error, application_checks.ApplicationMissingPermissions):
            await interaction.response.send_message(f"{interaction.user.mention} Error. Insufficient permissions",
                                                    ephemeral=True)

    @nextcord.slash_command(name="avatar", description="Generate a user's avatar")
    @application_checks.has_permissions(administrator=True)
    async def avatar(self, interaction: Interaction, user: nextcord.Member = SlashOption(description="Choose member")):
        embed = nextcord.Embed(title=f"Avatar of '{user.name}'", timestamp=datetime.datetime.now(),
                               color=nextcord.Color.blue())
        embed.set_image(url=user.avatar.url)
        await interaction.send(embed=embed, ephemeral=True)

    @avatar.error
    async def avatar_error(self, interaction: Interaction, error):
        if isinstance(error, application_checks.ApplicationMissingPermissions):
            await interaction.response.send_message(f"{interaction.user.mention} Error. Insufficient permissions",
                                                    ephemeral=True)

    @nextcord.slash_command(name="serverinfo", description="Find server info")
    @application_checks.has_permissions(administrator=True)
    async def serverinfo(self, interaction: Interaction):
        guild = interaction.user.guild
        embed = nextcord.Embed(title=guild.name, color=nextcord.Color.blue(), timestamp=datetime.datetime.now())
        serverData = {
            "Owner": guild.owner.mention,
            "Channels": len(guild.channels),
            "Members": guild.member_count,
            "Created": guild.created_at.strftime("%b %d, %Y, %T"),
            "Description": guild.description
        }
        for [fieldName, fieldVal] in serverData.items():
            embed.add_field(name=fieldName+":", value=fieldVal, inline=True)
        embed.set_footer(text=f"id: {guild.id}")
        embed.set_thumbnail(guild.icon)
        await interaction.send(embed=embed, ephemeral=True)

    @serverinfo.error
    async def avatar_error(self, interaction: Interaction, error):
        if isinstance(error, application_checks.ApplicationMissingPermissions):
            await interaction.response.send_message(f"{interaction.user.mention} Error. Insufficient permissions",
                                                    ephemeral=True)

    @nextcord.slash_command(name="setnick", description="Change a user's nickname")
    @application_checks.has_permissions(administrator=True, manage_nicknames=True)
    async def setnick(self, interaction: Interaction, user: nextcord.Member = SlashOption(description="Choose member"),
                      newnick: str = SlashOption(description="Enter a new nickname")):
        await user.edit(nick=newnick)
        await interaction.response.send_message(f"You have changed the nickname of {user.mention} to {newnick}",
                                                ephemeral=True)

    @setnick.error
    async def setnick(self, interaction: Interaction, error):
        if isinstance(error, application_checks.ApplicationMissingPermissions):
            await interaction.response.send_message(f"{interaction.user.mention} Error. Insufficient permissions",
                                                    ephemeral=True)


def setup(client):
    client.add_cog(Admin(client))
