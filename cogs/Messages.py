import random
import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
from keys import dogAPI, catAPI
import requests
from functions import get_time


class Messages(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="hello", description="Receive a hello message")
    async def hello(self, interaction: Interaction):
        print(f"{get_time()}: {interaction.user.name} sent /hello")
        await interaction.response.send_message(f"Hello! {interaction.user.mention}", ephemeral=True)

    @nextcord.slash_command(name="wave", description="Select a user to wave to")
    async def wave(self, interaction: Interaction, user: nextcord.Member = SlashOption(description="Choose member")):
        print(f"{get_time()}: {interaction.user.name} sent /wave")
        await interaction.response.send_message(f"{interaction.user.mention} waves to {user.mention}!")

    @nextcord.slash_command(name="repeat", description="Tell the bot to repeat a message")
    async def repeat(self, interaction: Interaction,
                     message: str = SlashOption(description="Type a message to be repeated")):
        print(f"{get_time()}: {interaction.user.name} sent /repeat")
        await interaction.response.send_message(f"{message}!")

    @nextcord.slash_command(name="flip", description="Have the bot flip a coin")
    async def flip(self, interaction: Interaction,
                   coins: int = SlashOption(name="coins", description="Enter number of coins to flip")):
        print(f"{get_time()}: {interaction.user.name} sent /flip")
        if coins <= 0 or coins >= 101:
            embed = nextcord.Embed(color=nextcord.Color.red(),
                                   description=f"❌ **Error.** {coins} is an invalid number of coins to flip. "
                                               f"Please choose a value between 1 and 100")
            await interaction.send(embed=embed, ephemeral=True)
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
            await interaction.response.send_message(f"You have flipped {', '.join(map(str, final))}")

    @nextcord.slash_command(name="roll", description="Have the bot roll a die")
    async def roll(self, interaction: Interaction,
                   die_value: int = SlashOption(name="sides", description="Choose the amount of sides on the die"),
                   die_number: int = SlashOption(name="rolls", description="Enter number of dice to roll")):
        print(f"{get_time()}: {interaction.user.name} sent /roll")
        if die_number <= 0 or die_number >= 101:
            embed = nextcord.Embed(color=nextcord.Color.red(),
                                   description=f"❌ **Error.** {die_number} is an invalid number of dice to roll. "
                                               f"Please choose a value between 1 and 100")
            await interaction.send(embed=embed, ephemeral=True)

        else:
            rolls = []
            for i in range(die_number):
                rolls.append(random.randint(1, die_value))
            await interaction.response.send_message(f"You have rolled a {', '.join(map(str, rolls))}")

    @nextcord.slash_command(name="phart", description="Receive the iconic Phartso gif")
    async def phart(self, interaction: Interaction):
        print(f"{get_time()}: {interaction.user.name} sent /phart")
        await interaction.response.send_message("https://tenor.com/view/marfie-chan-mad-shout-yell-ahhhh-gif-17014848")

    @nextcord.slash_command(name="rps", description="Play rock paper scissors with the bot")
    async def rps(self, interaction: Interaction,
                  number: int = SlashOption(name="hand", description="Choose your hand",
                                            choices={"rock": 1, "paper": 2, "scissors": 3})):
        print(f"{get_time()}: {interaction.user.name} sent /rps")
        options = {"rock": 1, "paper": 2, "scissors": 3}
        cpu_int = random.randint(1, 3)
        if cpu_int == number:
            choice = -1
            for key, val in options.items():
                if val == number:
                    choice = key
            await interaction.response.send_message(f"Tie. I also chose {choice}")
        else:
            outcome = {"1/2": "I chose paper. You lose",
                       "1/3": "I chose scissors. You win",
                       "2/1": "I chose rock. You win",
                       "2/3": "I chose scissors. You lose",
                       "3/1": "I chose rock. You lose",
                       "3/2": "I chose paper. You win"}
            game_string = f"{number}/{cpu_int}"
            await interaction.response.send_message(outcome[game_string])

    @nextcord.slash_command(name="dog", description="Generate a random dog picture")
    async def dog(self, interaction: Interaction):
        print(f"{get_time()}: {interaction.user.name} sent /dog")
        response = requests.get("https://api.thedogapi.com/v1/images/search?mime_types=gif",
                                headers={'x-api-key': dogAPI})
        image_link = response.json()[0]["url"]
        await interaction.response.send_message(image_link)

    @nextcord.slash_command(name="cat", description="Generate a random cat picture")
    async def cat(self, interaction: Interaction):
        print(f"{get_time()}: {interaction.user.name} sent /cat")
        response = requests.get("https://api.thecatapi.com/v1/images/search?mime_types=gif",
                                headers={'x-api-key': catAPI})
        image_link = response.json()[0]["url"]
        await interaction.response.send_message(image_link)

    @nextcord.slash_command(name="rng", description="Generate a random number")
    async def rng(self, interaction: Interaction,
                  upper_range: int = SlashOption(name="range", description="Enter upper range for number generation")):
        print(f"{get_time()}: {interaction.user.name} sent /rng")
        if upper_range <= 0:
            embed = nextcord.Embed(color=nextcord.Color.red(),
                                   description=f"❌ **Error.** {upper_range} is an invalid upper range. "
                                               f"Please provide a positive nonzero value")
            await interaction.send(embed=embed, ephemeral=True)

        else:
            await interaction.response.send_message(f"The generated number is {random.randint(1, upper_range)}")


def setup(client):
    client.add_cog(Messages(client))
