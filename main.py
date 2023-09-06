import nextcord
from nextcord.ext import commands
import os
from keys import botToken
from functions import get_time

client = commands.Bot(intents=nextcord.Intents.all())
client.remove_command(name="help")


@client.event
async def on_ready():
    await client.change_presence(status=nextcord.Status.do_not_disturb,
                                 activity=nextcord.Activity(type=nextcord.ActivityType.listening, name="/help"))
    print(f'Bot started: {get_time()}')
    print()

initial_extensions = []

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        initial_extensions.append("cogs." + filename[:-3])

if __name__ == '__main__':
    for extension in initial_extensions:
        client.load_extension(extension)

client.run(botToken)
