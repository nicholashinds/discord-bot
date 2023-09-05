import datetime
import nextcord
from nextcord.ext import commands
from nextcord import Interaction, ButtonStyle
from nextcord.ui import Button, View
from keys import testServerId
import json

helpGuide = json.load(open("./cogs/help.json"))


def createHelpEmbed(pageNum=0, inline=False, interaction=None):
    pageNum = pageNum % len(list(helpGuide))
    pageTitle = list(helpGuide)[pageNum]
    embed = nextcord.Embed(color=nextcord.Color.blue(), title=pageTitle, timestamp=datetime.datetime.now())
    for key, val in helpGuide[pageTitle].items():
        embed.add_field(name=key, value=val, inline=inline)
        embed.set_footer(text=f"Page {pageNum+1} of {len(list(helpGuide))}")
        embed.set_thumbnail(url="https://media.tenor.com/nuKGpea_I4gAAAAi/star-platinum-heritage-for-the-future.gif")
        if interaction is not None:
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
    return embed


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="help", description="Receive info on all the commands")
    async def help(self, interaction: Interaction):
        print(f"{datetime.datetime.now()}: {interaction.user.name} sent /help")
        currentPage = 0

        async def next_callback(interaction2):
            nonlocal currentPage, sent_msg
            currentPage += 1
            await sent_msg.edit(embed=createHelpEmbed(pageNum=currentPage, interaction=interaction), view=myview)

        async def previous_callback(interaction2):
            nonlocal currentPage, sent_msg
            currentPage -= 1
            await sent_msg.edit(embed=createHelpEmbed(pageNum=currentPage, interaction=interaction), view=myview)

        nextButton = Button(label=">", style=ButtonStyle.blurple)
        nextButton.callback = next_callback
        previousButton = Button(label="<", style=ButtonStyle.blurple)
        previousButton.callback = previous_callback

        myview = View(timeout=180)
        myview.add_item(previousButton)
        myview.add_item(nextButton)
        sent_msg = await interaction.send(embed=createHelpEmbed(interaction=interaction), view=myview, ephemeral=True)


def setup(client):
    client.add_cog(Help(client))
