from discord.ext import commands


class Legacy:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True, aliases=["removehacker"])
    async def probate(self, ctx):
        """Use .revoke <user> <role>"""
        await ctx.send("This command was replaced with `.revoke <user> <role>`"
                       " on Robocop-NG, please use that instead.")

    @commands.command(hidden=True, aliases=["addhacker"])
    async def unprobate(self, ctx):
        """Use .approve <user> <role>"""
        await ctx.send("This command was replaced with `.approve <user> <role>`"
                       " on Robocop-NG, please use that instead.")


def setup(bot):
    bot.add_cog(Legacy(bot))
