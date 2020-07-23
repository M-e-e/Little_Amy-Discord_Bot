from discord.ext import commands
import random


class random_behaviour(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



def setup(bot):
    bot.add_cog(random_behaviour(bot))