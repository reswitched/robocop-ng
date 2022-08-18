from discord.ext import commands
from discord.ext.commands import Cog


class Legacy(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True, aliases=["removehacker"])
    async def probate(self, ctx):
        """Use .revoke <user> <role>"""
        await ctx.send(
            "This command was replaced with `.revoke <user> <role>`"
            " on Robocop-NG, please use that instead."
        )

    @commands.command(hidden=True)
    async def softlock(self, ctx):
        """Use .lock True"""
        await ctx.send(
            "This command was replaced with `.lock True`"
            " on Robocop-NG, please use that instead.\n"
            "Also... good luck, and sorry for taking your time. "
            "Lockdown rarely means anything good."
        )

    @commands.command(hidden=True, aliases=["addhacker"])
    async def unprobate(self, ctx):
        """Use .approve <user> <role>"""
        await ctx.send(
            "This command was replaced with `.approve <user> <role>`"
            " on Robocop-NG, please use that instead."
        )


async def setup(bot):
    await bot.add_cog(Legacy(bot))
