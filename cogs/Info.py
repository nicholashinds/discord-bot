import datetime
import humanfriendly
import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption, ButtonStyle
from nextcord.ui import Button, View
from functions import get_time
from datetime import datetime


def role_embed_generator(interaction: Interaction):
    guild = interaction.user.guild
    role_list = []
    role_amount = len(guild.roles) - 1
    top_color_counter = 0
    top_color = ""
    everyone_pass = True
    for roles in guild.roles:
        if everyone_pass:
            everyone_pass = False
        else:
            top_color_counter += 1
            if top_color_counter == role_amount:
                top_color = guild.get_role(roles.id).color
            role_list.append(f"<@&{roles.id}>")
    if top_color == "":
        top_color = nextcord.Color.blue()
    elif top_color == nextcord.Color.from_rgb(0, 0, 0):
        top_color = nextcord.Color.blue()

    role_list.reverse()
    role_list_string = "\n".join(role_list)

    role_embed = nextcord.Embed(title=f"Roles ({role_amount})",
                                description=role_list_string, color=top_color, timestamp=datetime.now())
    role_embed.set_footer(text=f"Requested by {interaction.user.name}", icon_url=interaction.user.avatar.url)
    return role_embed


class Info(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="userinfo", description="Find a user's profile info")
    async def userinfo(self, interaction: Interaction, user: nextcord.Member = SlashOption(description="Choose member")):
        print(f"{get_time()}: {interaction.user.name} sent /userinfo for {user.name}")

        role_list = []
        role_amount = len(user.roles) - 1
        top_color_counter = 0
        top_color = ""
        everyone_pass = True
        for roles in user.roles:
            if everyone_pass:
                everyone_pass = False
            else:
                top_color_counter += 1
                if top_color_counter == role_amount:
                    top_color = user.guild.get_role(roles.id).color
                role_list.append(f"<@&{roles.id}>")
        if top_color == "":
            top_color = nextcord.Color.blue()
        elif top_color == nextcord.Color.from_rgb(0,0,0):
            top_color = nextcord.Color.blue()

        role_list.reverse()
        role_list_string = " ".join(role_list)

        embed = nextcord.Embed(color=top_color, timestamp=datetime.now())
        embed.set_author(name=user.name, icon_url=user.avatar.url)
        embed.add_field(name="", value=f"{user.mention} (id: {user.id})", inline=False)
        embed.add_field(name="Account Creation",
                        value=user.created_at.strftime("%a, %b %d, %Y at %I:%M%p"), inline=True)
        embed.add_field(name='\u0020', value='\u0020', inline=True)
        embed.add_field(name="Joined Server", value=user.joined_at.strftime("%a, %b %d, %Y at %I:%M%p"), inline=True)
        embed.add_field(name=f"Roles ({role_amount})",
                        value=role_list_string, inline=False)
        embed.set_footer(text=f"Requested by {interaction.user.name}", icon_url=interaction.user.avatar.url)
        embed.set_thumbnail(user.display_avatar)

        await interaction.send(embed=embed)

    @nextcord.slash_command(name="avatar", description="Generate a user's avatar")
    async def avatar(self, interaction: Interaction, user: nextcord.Member = SlashOption(description="Choose member")):
        print(f"{get_time()}: {interaction.user.name} sent /avatar for {user.name}")
        embed = nextcord.Embed(title=f"Avatar of '{user.name}'", timestamp=datetime.now(),
                               color=nextcord.Color.blue())
        embed.set_image(url=user.avatar.url)
        embed.set_footer(text=f"Requested by {interaction.user.name}", icon_url=interaction.user.avatar.url)
        await interaction.send(embed=embed)

    @nextcord.slash_command(name="serverinfo", description="Get info about the server")
    async def serverinfo(self, interaction: Interaction):
        print(f"{get_time()}: {interaction.user.name} sent /serverinfo")

        guild = interaction.user.guild
        embed = nextcord.Embed(color=nextcord.Color.blue(), timestamp=datetime.now())
        embed.set_author(name=interaction.guild.name, icon_url=interaction.guild.icon.url)
        embed.add_field(name="Owner", value=guild.owner.mention, inline=True)
        embed.add_field(name="Members", value=guild.member_count, inline=True)
        embed.add_field(name="Roles", value=len(guild.roles), inline=True)
        embed.add_field(name="Categories", value=len(guild.categories), inline=True)
        embed.add_field(name="Text Channels", value=len(guild.text_channels), inline=True)
        embed.add_field(name="Voice Channels", value=len(guild.voice_channels), inline=True)
        embed.add_field(name="Created", value=guild.created_at.strftime("%a, %b %d, %Y at %I:%M%p"), inline=True)
        embed.add_field(name="Guild ID", value=guild.id, inline=True)

        if guild.premium_subscription_count < 2:
            guild_string = f"{guild.premium_subscription_count} (Tier 0)"
        elif 2 <= guild.premium_subscription_count < 7:
            guild_string = f"{guild.premium_subscription_count} (Tier 1)"
        elif 7 <= guild.premium_subscription_count < 21:
            guild_string = f"{guild.premium_subscription_count} (Tier 2)"
        else:
            guild_string = f"{guild.premium_subscription_count} (Tier 3)"

        embed.add_field(name="Boosts", value=guild_string)
        embed.set_footer(text=f"Requested by {interaction.user.name}", icon_url=interaction.user.avatar.url)
        embed.set_thumbnail(guild.icon)

        roles_button = Button(label="View Roles", style=ButtonStyle.blurple)
        myview = View(timeout=180)

        async def roll_callback(z):
            print(f"{get_time()}: {interaction.user.name} sent /roles")
            await interaction.send(embed=role_embed_generator(interaction), ephemeral=True)

        roles_button.callback = roll_callback
        myview.add_item(roles_button)
        await interaction.send(embed=embed, view=myview)

    @nextcord.slash_command(name="roles", description="View all the roles on the server")
    async def roles(self, interaction: Interaction):
        print(f"{get_time()}: {interaction.user.name} sent /roles")
        await interaction.send(embed=role_embed_generator(interaction))

    @nextcord.slash_command(name="uptime", description="View current bot uptime")
    async def uptime(self, interaction: Interaction):
        f = open("uptime.txt", "r")
        start_time = datetime.strptime(f.read(), "%Y-%m-%d %H:%M:%S")
        current_time = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
        uptime = current_time - start_time
        time_string = humanfriendly.format_timespan(uptime.total_seconds())
        print(f"{get_time()}: {interaction.user.name} sent /uptime")
        await interaction.response.send_message(f"The current uptime for the bot is `{time_string}`")


def setup(client):
    client.add_cog(Info(client))
