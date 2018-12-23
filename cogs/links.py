from discord.ext import commands


class Links:
    """
    Commands for easily linking to projects.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    async def pegaswitch(self, ctx):
        """Link to the Pegaswitch repo"""
        await ctx.send("https://github.com/reswitched/pegaswitch")

    @commands.command(hidden=True, aliases=["atmos"])
    async def atmosphere(self, ctx):
        """Link to the Atmosphere repo"""
        await ctx.send("https://github.com/atmosphere-nx/atmosphere")

    @commands.command(hidden=True, aliases=["guides"])
    async def guide(self, ctx):
        """Link to the guide(s)"""
        await ctx.send("*AtlasNX's Guide:* https://guide.teamatlasnx.com\n"
                       "*Noirscape's Guide:* http://switchguide.xyz/\n"
                       "*Pegaswitch Guide:* https://switch.hacks.guide/")


def setup(bot):
    bot.add_cog(Links(bot))
