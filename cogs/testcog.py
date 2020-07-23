from discord.ext import commands

class Testcog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def testing(self, ctx):
        await ctx.send(ctx.channel.id)



def setup(bot):
    bot.add_cog(Testcog(bot))