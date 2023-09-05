import datetime
import nextcord
from nextcord.ext import commands, application_checks
from nextcord import Interaction, SlashOption
from keys import testServerId


class Misc(commands.Cog):
    def __init__(self, client):
        self.client = client


def setup(client):
    client.add_cog(Misc(client))