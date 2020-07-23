from discord.ext import commands

class Debugger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def channel(self, ctx):
        """Shows in which channel you are"""
        await ctx.send(ctx.channel)


def setup(bot):
    bot.add_cog(Debugger(bot))