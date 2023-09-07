import datetime
import humanfriendly
import nextcord
from nextcord.ext import commands, application_checks
from nextcord import Interaction, SlashOption
from functions import get_time


def insuff_perms_embed(interaction: Interaction):
    embed = nextcord.Embed(color=nextcord.Color.red(),
                           description=f"❌ {interaction.user.mention} **Error.** Insufficient permissions")
    return embed


def unknown_error_embed(interaction: Interaction):
    embed = nextcord.Embed(color=nextcord.Color.red(),
                           description=f"❌ {interaction.user.mention} **Error.** Unknown error occurred. "
                                       f"Please check your input and try again")
    return embed


class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="purge", description="Purge specified number of lines")
    @application_checks.has_permissions(administrator=True)
    async def purge(self, interaction: Interaction,
                    lines: int = SlashOption(description="Enter a number of lines to be purged")):
        print(f"{get_time()}: {interaction.user.name} sent /purge with {lines} lines")
        embed = nextcord.Embed(color=nextcord.Color.green(),
                               description=f"✅ **Success.** Purged {lines} line(s)")
        await interaction.channel.purge(limit=lines)
        await interaction.send(embed=embed, ephemeral=True)

    @purge.error
    async def purge_error(self, interaction: Interaction, error):
        print(f"{get_time()}: {interaction.user.name} sent /purge with insufficient perms")
        if isinstance(error, application_checks.ApplicationMissingPermissions):
            await interaction.send(embed=insuff_perms_embed(interaction), ephemeral=True)
        else:
            await interaction.send(embed=unknown_error_embed(interaction), ephemeral=True)

    @nextcord.slash_command(name="setnick", description="Change a user's nickname")
    @application_checks.has_permissions(administrator=True)
    async def setnick(self, interaction: Interaction, user: nextcord.Member = SlashOption(description="Choose member"),
                      newnick: str = SlashOption(description="Enter a new nickname", required=False)):
        print(f"{get_time()}: {interaction.user.name} sent /setnick for {user.name}")
        await user.edit(nick=newnick)
        if newnick is None:
            embed = nextcord.Embed(color=nextcord.Color.green(),
                                   description=f"✅ **Success.** You have reset the nickname of {user.mention}")
            await interaction.send(embed=embed, ephemeral=True)
        else:
            embed = nextcord.Embed(color=nextcord.Color.green(),
                                   description=f"✅ **Success.** You have "
                                               f"changed the nickname of {user.mention} to {newnick}")
            await interaction.send(embed=embed, ephemeral=True)

    @setnick.error
    async def setnick_error(self, interaction: Interaction, error):
        print(f"{get_time()}: {interaction.user.name} sent /setnick with insufficient perms")
        if isinstance(error, application_checks.ApplicationMissingPermissions):
            await interaction.send(embed=insuff_perms_embed(interaction), ephemeral=True)
        else:
            await interaction.send(embed=unknown_error_embed(interaction), ephemeral=True)

    @nextcord.slash_command(name="kick", description="Kick a member from the server")
    @application_checks.has_permissions(administrator=True)
    async def kick(self, interaction: Interaction, user: nextcord.Member = SlashOption(description="Choose member"),
                   reason: str = SlashOption(description="Enter a reason for kick", required=False)):
        if reason is None:
            print(f"{get_time()}: {interaction.user.name} sent /kick for {user.name} Reason: None listed")
            await user.kick(reason=f"Kicked by {interaction.user.name}")
            embed = nextcord.Embed(color=nextcord.Color.green(),
                                   description=f"✅ **Success.** You have kicked {user.mention} for reason: None listed")
            await interaction.send(embed=embed, ephemeral=True)
        else:
            print(f"{get_time()}: {interaction.user.name} sent /kick for {user.name} Reason: {reason}")
            await user.kick(reason=reason)
            embed = nextcord.Embed(color=nextcord.Color.green(),
                                   description=f"✅ **Success.** You have kicked {user.mention} for reason: {reason}")
            await interaction.send(embed=embed, ephemeral=True)

    @kick.error
    async def kick_error(self, interaction: Interaction, error):
        print(f"{get_time()}: {interaction.user.name} sent /kick with insufficient perms")
        if isinstance(error, application_checks.ApplicationMissingPermissions):
            await interaction.send(embed=insuff_perms_embed(interaction), ephemeral=True)
        else:
            await interaction.send(embed=unknown_error_embed(interaction), ephemeral=True)

    @nextcord.slash_command(name="ban", description="Ban a member from the server")
    @application_checks.has_permissions(administrator=True)
    async def ban(self, interaction: Interaction, user: nextcord.Member = SlashOption(description="Choose member"),
                  reason: str = SlashOption(description="Enter a reason for ban", required=False)):
        if reason is None:
            print(f"{get_time()}: {interaction.user.name} sent /ban for {user.name} Reason: None listed")
            await user.ban(reason=f"Banned by {interaction.user.name}")
            embed = nextcord.Embed(color=nextcord.Color.green(),
                                   description=f"✅ **Success.** You have banned {user.mention} for reason: None listed")
            await interaction.send(embed=embed, ephemeral=True)
        else:
            print(f"{get_time()}: {interaction.user.name} sent /ban for {user.name} Reason: {reason}")
            await user.ban(reason=reason)
            embed = nextcord.Embed(color=nextcord.Color.green(),
                                   description=f"✅ **Success.** You have banned {user.mention} for reason: {reason}")
            await interaction.send(embed=embed, ephemeral=True)

    @ban.error
    async def ban_error(self, interaction: Interaction, error):
        print(f"{get_time()}: {interaction.user.name} sent /ban with insufficient perms")
        if isinstance(error, application_checks.ApplicationMissingPermissions):
            await interaction.send(embed=insuff_perms_embed(interaction), ephemeral=True)
        else:
            await interaction.send(embed=unknown_error_embed(interaction), ephemeral=True)

    @nextcord.slash_command(name="unban", description="Unban a member from the server")
    @application_checks.has_permissions(administrator=True)
    async def unban(self, interaction: Interaction, user: nextcord.User = SlashOption(description="Enter user id"),
                    reason: str = SlashOption(description="Enter a reason for ban", required=False)):
        if reason is None:
            print(f"{get_time()}: {interaction.user.name} sent /unban for {user.name} Reason: None listed")
            await interaction.user.guild.unban(user=user, reason=f"Unbanned by {interaction.user.name}")
            embed = nextcord.Embed(color=nextcord.Color.green(),
                                   description=f"✅ **Success.** You have unbanned {user.mention} for reason: None listed")
            await interaction.send(embed=embed, ephemeral=True)
        else:
            print(f"{get_time()}: {interaction.user.name} sent /unban for {user.name} Reason: {reason}")
            await interaction.user.guild.unban(user=user, reason=reason)
            embed = nextcord.Embed(color=nextcord.Color.green(),
                                   description=f"✅ **Success.** You have unbanned {user.mention} for reason: {reason}")
            await interaction.send(embed=embed, ephemeral=True)

    @unban.error
    async def unban_error(self, interaction: Interaction, error):
        print(f"{get_time()}: {interaction.user.name} sent /unban with insufficient perms")
        if isinstance(error, application_checks.ApplicationMissingPermissions):
            await interaction.send(embed=insuff_perms_embed(interaction), ephemeral=True)
        else:
            await interaction.send(embed=unknown_error_embed(interaction), ephemeral=True)

    @nextcord.slash_command(name="mute", description="Mute a member of the server")
    @application_checks.has_permissions(administrator=True)
    async def mute(self, interaction: Interaction, user: nextcord.Member = SlashOption(description="Choose a member"),
                   time_str: str = SlashOption(name="time", description="Enter a time for mute (ms, s, m, h, d, w, y)"),
                   reason: str = SlashOption(description="Enter a reason for mute", required=False)):
        time = humanfriendly.parse_timespan(time_str)
        if reason is None:
            print(f"{get_time()}: {interaction.user.name} sent /mute for {user.name} Reason: None listed")
            await user.edit(timeout=nextcord.utils.utcnow()+datetime.timedelta(seconds=time),
                            reason=f"Muted by {interaction.user.name} for {time_str}")
            embed = nextcord.Embed(color=nextcord.Color.green(),
                                   description=f"✅ **Success.** You have muted {user.mention} for {time_str}. "
                                               f"Reason: None listed")
            await interaction.send(embed=embed, ephemeral=True)
        else:
            print(f"{get_time()}: {interaction.user.name} sent /mute for {user.name} Reason: {reason}")
            await user.edit(timeout=nextcord.utils.utcnow()+datetime.timedelta(seconds=time), reason=reason)
            embed = nextcord.Embed(color=nextcord.Color.green(),
                                   description=f"✅ **Success.** You have muted {user.mention} for {time_str}. "
                                               f"Reason: {reason}")
            await interaction.send(embed=embed, ephemeral=True)

    @mute.error
    async def mute_error(self, interaction: Interaction, error):
        print(f"{get_time()}: {interaction.user.name} sent /mute with insufficient perms")
        if isinstance(error, application_checks.ApplicationMissingPermissions):
            await interaction.send(embed=insuff_perms_embed(interaction), ephemeral=True)
        else:
            await interaction.send(embed=unknown_error_embed(interaction), ephemeral=True)

    @nextcord.slash_command(name="unmute", description="Unmute a member of the server")
    @application_checks.has_permissions(administrator=True)
    async def unmute(self, interaction: Interaction, user: nextcord.Member = SlashOption(description="Choose a member"),
                     reason: str = SlashOption(description="Enter a reason for unmute", required=False)):
        if reason is None:
            print(f"{get_time()}: {interaction.user.name} sent /unmute for {user.name} Reason: None listed")
            await user.edit(timeout=None, reason=f"Unmuted by {interaction.user.name}")
            embed = nextcord.Embed(color=nextcord.Color.green(),
                                   description=f"✅ **Success.** "
                                               f"You have unmuted {user.mention} for reason: None listed")
            await interaction.send(embed=embed, ephemeral=True)
        else:
            print(f"{get_time()}: {interaction.user.name} sent /unmute for {user.name} Reason: {reason}")
            await user.edit(timeout=None, reason=reason)
            embed = nextcord.Embed(color=nextcord.Color.green(),
                                   description=f"✅ **Success.** You have unmuted {user.mention} for reason: {reason}")
            await interaction.send(embed=embed, ephemeral=True)

    @unmute.error
    async def unmute_error(self, interaction: Interaction, error):
        print(f"{get_time()}: {interaction.user.name} sent /unmute with insufficient perms")
        if isinstance(error, application_checks.ApplicationMissingPermissions):
            await interaction.send(embed=insuff_perms_embed(interaction), ephemeral=True)
        else:
            await interaction.send(embed=unknown_error_embed(interaction), ephemeral=True)

    @nextcord.slash_command(name="softban", description="Softban a user")
    @application_checks.has_permissions(administrator=True)
    async def softban(self, interaction: Interaction, user: nextcord.Member = SlashOption(description="Choose a member"),
                      reason: str = SlashOption(description="Enter a reason for unmute", required=False)):
        if reason is None:
            print(f"{get_time()}: {interaction.user.name}"
                  f" sent /softban for {user.name} Reason: None listed")
            await user.ban(reason=f"Softbanned by {interaction.user.name}")
            await interaction.user.guild.unban(user=user, reason=f"Softban continuation by {interaction.user.name}")
            embed = nextcord.Embed(color=nextcord.Color.green(),
                                   description=f"✅ **Success.** "
                                               f"You have softbanned {user.mention} for reason: None listed")
            await interaction.send(embed=embed, ephemeral=True)
        else:
            print(f"{get_time()}: {interaction.user.name}"
                  f" sent /softban for {user.name} Reason: None listed")
            await user.ban(reason=reason)
            await interaction.user.guild.unban(user=user, reason=f"Softban continuation by {interaction.user.name}")
            embed = nextcord.Embed(color=nextcord.Color.green(),
                                   description=f"✅ **Success.** You have banned {user.mention} for reason: {reason}")
            await interaction.send(embed=embed, ephemeral=True)

    @softban.error
    async def softban_error(self, interaction: Interaction, error):
        print(f"{get_time()}: {interaction.user.name} sent /softban with insufficient perms")
        if isinstance(error, application_checks.ApplicationMissingPermissions):
            await interaction.send(embed=insuff_perms_embed(interaction), ephemeral=True)
        else:
            await interaction.send(embed=unknown_error_embed(interaction), ephemeral=True)


def setup(client):
    client.add_cog(Admin(client))
