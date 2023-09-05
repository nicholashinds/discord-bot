import random
import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
from keys import testServerId, dogAPI, catAPI
import requests


class Messages(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="hello", description="Receive a hello message")
    async def hello(self, interaction: Interaction):
        await interaction.response.send_message(f"Hello! {interaction.user.mention}", ephemeral=True)

    @nextcord.slash_command(name="wave", description="Select a user to wave to")
    async def wave(self, interaction: Interaction, user: nextcord.Member = SlashOption(description="Choose member")):
        await interaction.response.send_message(f"{interaction.user.mention} waves to {user.mention}!")

    @nextcord.slash_command(name="repeat", description="Tell the bot to repeat a message")
    async def repeat(self, interaction: Interaction,
                     message: str = SlashOption(description="Type a message to be repeated")):
        await interaction.response.send_message(f"{message}!")

    @nextcord.slash_command(name="flip", description="Have the bot flip a coin")
    async def flip(self, interaction: Interaction):
        flipInt = random.randint(0, 2)
        if flipInt == 1:
            await interaction.response.send_message("Tails")
        else:
            await interaction.response.send_message("Heads")
    
    @nextcord.slash_command(name="roll", description="Have the bot roll a die")
    async def roll(self, interaction: Interaction):
        rollInt = random.randint(0, 6)
        await interaction.response.send_message(f"You have rolled a {rollInt}")

    @nextcord.slash_command(name="phart", description="Receive the iconic Phartso gif")
    async def phart(self, interaction: Interaction):
        await interaction.response.send_message("https://tenor.com/view/marfie-chan-mad-shout-yell-ahhhh-gif-17014848")

    @nextcord.slash_command(name="rps", description="Play rock paper scissors with the bot")
    async def rps(self, interaction: Interaction,
                  number: int = SlashOption(name="hand", description="Choose your hand",
                                            choices={"rock": 1, "paper": 2, "scissors": 3})):
        cpuInt = random.randint(0, 3)
        if cpuInt == number:
            await interaction.response.send_message("Tie!")
        if number == 1 and cpuInt == 2:
            await interaction.response.send_message("I chose paper. You lose")
        if number == 1 and cpuInt == 3:
            await interaction.response.send_message("I chose scissors. You win")
        if number == 2 and cpuInt == 1:
            await interaction.response.send_message("I chose rock. You win")
        if number == 2 and cpuInt == 3:
            await interaction.response.send_message("I chose scissors. You lose")
        if number == 3 and cpuInt == 1:
            await interaction.response.send_message("I chose rock. You lose")
        if number == 3 and cpuInt == 2:
            await interaction.response.send_message("I chose paper. You win")

    @nextcord.slash_command(name="dog", description="Generate a random dog picture")
    async def dog(self, interaction: Interaction):
        response = requests.get("https://api.thedogapi.com/v1/images/search?mime_types=gif",
                                headers={'x-api-key': dogAPI})
        image_link = response.json()[0]["url"]
        await interaction.response.send_message(image_link)

    @nextcord.slash_command(name="cat", description="Generate a random cat picture")
    async def cat(self, interaction: Interaction):
        response = requests.get("https://api.thecatapi.com/v1/images/search?mime_types=gif",
                                headers={'x-api-key': catAPI})
        image_link = response.json()[0]["url"]
        await interaction.response.send_message(image_link)


def setup(client):
    client.add_cog(Messages(client))
