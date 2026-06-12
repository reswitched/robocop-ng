import discord
import config
from discord.ext import commands
from discord.ext.commands import Cog


class Links(Cog):
    """
    Commands for easily linking to projects.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(hidden=True, aliases=["atmos"])
    async def atmosphere(self, ctx):
        """Link to the Atmosphere repo"""
        await ctx.send("https://github.com/atmosphere-nx/atmosphere")

    @commands.hybrid_command(hidden=True, aliases=["xyproblem"])
    async def xy(self, ctx):
        """Link to the "What is the XY problem?" post from SE"""
        await ctx.send(
            "<https://meta.stackexchange.com/q/66377/285481>\n\n"
            "TL;DR: It's asking about your attempted solution "
            "rather than your actual problem.\n"
            "It's perfectly okay to want to learn about a "
            "solution, but please be clear about your intentions "
            "if you're not actually trying to solve a problem."
        )

    @commands.hybrid_command()
    async def source(self, ctx):
        """Gives link to source code."""
        await ctx.send(
            f"You can find my source at {config.source_url}. "
            "Serious PRs and issues welcome!"
        )


async def setup(bot):
    await bot.add_cog(Links(bot))
