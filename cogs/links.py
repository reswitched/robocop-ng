from discord.ext import commands


class Links:
    """
    Commands for easily linking to projects.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    async def pegaswitch(self, ctx):
        """test"""
        await ctx.send("https://github.com/reswitched/pegaswitch")


def setup(bot):
    bot.add_cog(Links(bot))
