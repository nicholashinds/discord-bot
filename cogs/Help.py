import datetime
import nextcord
from nextcord.ext import commands
from nextcord import Interaction, ButtonStyle
from nextcord.ui import Button, View
from keys import testServerId
import json

helpGuide = json.load(open("./cogs/help.json"))


def create_help_embed(page_num=0, interaction=None):
    page_num = page_num % len(list(helpGuide))
    page_title = list(helpGuide)[page_num]
    embed = nextcord.Embed(color=nextcord.Color.blue(), title=page_title, timestamp=datetime.datetime.now())
    page_description = ""
    current_field_name = ""
    for key, val in helpGuide[page_title].items():
        if "Title:" in key:
            current_field_name = key[7:]
        elif "update" in key:
            embed.add_field(name=current_field_name, value=page_description, inline=False)
            current_field_name = ""
            page_description = ""
        else:
            page_description += f"**/{key}** - {val}\n"

    embed.add_field(name=current_field_name, value=page_description, inline=False)
    embed.set_footer(text=f"Page {page_num + 1} of {len(list(helpGuide))}")
    embed.set_thumbnail(
        url="https://media.tenor.com/nuKGpea_I4gAAAAi/star-platinum-heritage-for-the-future.gif")
    if interaction is not None:
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
    return embed


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="help", description="Receive info on all the commands")
    async def help(self, interaction: Interaction):
        print(f"{datetime.datetime.now()}: {interaction.user.name} sent /help")
        current_page = 0

        async def next_callback(z):
            nonlocal current_page, sent_msg
            current_page += 1
            await sent_msg.edit(embed=create_help_embed(page_num=current_page, interaction=interaction), view=myview)

        async def previous_callback(z):
            nonlocal current_page, sent_msg
            current_page -= 1
            await sent_msg.edit(embed=create_help_embed(page_num=current_page, interaction=interaction), view=myview)

        next_button = Button(label=">", style=ButtonStyle.blurple)
        next_button.callback = next_callback
        previous_button = Button(label="<", style=ButtonStyle.blurple)
        previous_button.callback = previous_callback

        myview = View(timeout=180)
        myview.add_item(previous_button)
        myview.add_item(next_button)
        sent_msg = await interaction.send(embed=create_help_embed(interaction=interaction), view=myview, ephemeral=True)


def setup(client):
    client.add_cog(Help(client))
