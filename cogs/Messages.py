import datetime
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
        print(f"{datetime.datetime.now()}: {interaction.user.name} sent /hello")
        await interaction.response.send_message(f"Hello! {interaction.user.mention}", ephemeral=True)

    @nextcord.slash_command(name="wave", description="Select a user to wave to")
    async def wave(self, interaction: Interaction, user: nextcord.Member = SlashOption(description="Choose member")):
        print(f"{datetime.datetime.now()}: {interaction.user.name} sent /wave")
        await interaction.response.send_message(f"{interaction.user.mention} waves to {user.mention}!")

    @nextcord.slash_command(name="repeat", description="Tell the bot to repeat a message")
    async def repeat(self, interaction: Interaction,
                     message: str = SlashOption(description="Type a message to be repeated")):
        print(f"{datetime.datetime.now()}: {interaction.user.name} sent /repeat")
        await interaction.response.send_message(f"{message}!")

    @nextcord.slash_command(name="flip", description="Have the bot flip a coin")
    async def flip(self, interaction: Interaction,
                   coins: int = SlashOption(name="coins", description="Enter number of coins to flip")):
        print(f"{datetime.datetime.now()}: {interaction.user.name} sent /flip")
        if coins <= 0 or coins >= 101:
            await interaction.response.send_message(f"Error. `{coins}` is an invalid number of coins to flip. "
                                                    f"Please choose a value between 1 and 100",
                                                    ephemeral=True)
        else:
            flips = []
            final = []
            for i in range(coins):
                flips.append(random.randint(1, 2))
            for results in flips:
                if results == 1:
                    final.append("Tails")
                elif results == 2:
                    final.append("Heads")
                else:
                    final.append("Error")
            await interaction.response.send_message(f"You have flipped `{', '.join(map(str, final))}`")

    @nextcord.slash_command(name="roll", description="Have the bot roll a die")
    async def roll(self, interaction: Interaction,
                   die_value: int = SlashOption(name="die", description="Choose the amount of sides on the die",
                                                choices={"d6": 6, "d12": 12, "d20": 20, "d50": 50, "d100": 100}),
                   die_number: int = SlashOption(description="Enter number of dice to roll")):
        print(f"{datetime.datetime.now()}: {interaction.user.name} sent /roll")
        if die_number <= 0 or die_number >= 101:
            await interaction.response.send_message(f"Error. `{die_number}` is an invalid number of dice to roll. "
                                                    f"Please choice a value between 1 and 100",
                                                    ephemeral=True)
        else:
            rolls = []
            for i in range(die_number):
                rolls.append(random.randint(1, die_value))
            await interaction.response.send_message(f"You have rolled a `{', '.join(map(str, rolls))}`")

    @nextcord.slash_command(name="phart", description="Receive the iconic Phartso gif")
    async def phart(self, interaction: Interaction):
        print(f"{datetime.datetime.now()}: {interaction.user.name} sent /phart")
        await interaction.response.send_message("https://tenor.com/view/marfie-chan-mad-shout-yell-ahhhh-gif-17014848")

    @nextcord.slash_command(name="rps", description="Play rock paper scissors with the bot")
    async def rps(self, interaction: Interaction,
                  number: int = SlashOption(name="hand", description="Choose your hand",
                                            choices={"rock": 1, "paper": 2, "scissors": 3})):
        print(f"{datetime.datetime.now()}: {interaction.user.name} sent /rps")
        options = {"rock": 1, "paper": 2, "scissors": 3}
        cpu_int = random.randint(0, 3)
        if cpu_int == number:
            choice = -1
            for key, val in options.items():
                if val == number:
                    choice = key
            await interaction.response.send_message(f"Tie. I also chose {choice}")

        if number == 1 and cpu_int == 2:  # rock/paper
            await interaction.response.send_message("I chose paper. You lose")
        if number == 1 and cpu_int == 3:  # rock/scissors
            await interaction.response.send_message("I chose scissors. You win")
        if number == 2 and cpu_int == 1:  # paper/rock
            await interaction.response.send_message("I chose rock. You win")
        if number == 2 and cpu_int == 3:  # paper/scissors
            await interaction.response.send_message("I chose scissors. You lose")
        if number == 3 and cpu_int == 1:  # scissors/rock
            await interaction.response.send_message("I chose rock. You lose")
        if number == 3 and cpu_int == 2:  # scissors/paper
            await interaction.response.send_message("I chose paper. You win")

    @nextcord.slash_command(name="dog", description="Generate a random dog picture")
    async def dog(self, interaction: Interaction):
        print(f"{datetime.datetime.now()}: {interaction.user.name} sent /dog")
        response = requests.get("https://api.thedogapi.com/v1/images/search?mime_types=gif",
                                headers={'x-api-key': dogAPI})
        image_link = response.json()[0]["url"]
        await interaction.response.send_message(image_link)

    @nextcord.slash_command(name="cat", description="Generate a random cat picture")
    async def cat(self, interaction: Interaction):
        print(f"{datetime.datetime.now()}: {interaction.user.name} sent /cat")
        response = requests.get("https://api.thecatapi.com/v1/images/search?mime_types=gif",
                                headers={'x-api-key': catAPI})
        image_link = response.json()[0]["url"]
        await interaction.response.send_message(image_link)

    @nextcord.slash_command(name="rng", description="Generate a random number")
    async def rng(self, interaction: Interaction,
                  upper_range: int = SlashOption(name="range", description="Enter upper range for number generation")):
        print(f"{datetime.datetime.now()}: {interaction.user.name} sent /rng")
        if upper_range <= 0:
            await interaction.response.send_message(f"Error. `{upper_range}` is an invalid upper range. "
                                                    f"Please provide a positive nonzero value", ephemeral=True)
        else:
            await interaction.response.send_message(f"The generated number is `{random.randint(1, upper_range)}`")


def setup(client):
    client.add_cog(Messages(client))
