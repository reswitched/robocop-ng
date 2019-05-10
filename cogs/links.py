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

    @commands.command(hidden=True)
    async def pegaswitch(self, ctx):
        """Link to the Pegaswitch repo"""
        await ctx.send("https://github.com/reswitched/pegaswitch")

    @commands.command(hidden=True, aliases=["atmos"])
    async def atmosphere(self, ctx):
        """Link to the Atmosphere repo"""
        await ctx.send("https://github.com/atmosphere-nx/atmosphere")

    @commands.command(hidden=True, aliases=["xyproblem"])
    async def xy(self, ctx):
        """Link to the "What is the XY problem?" post from SE"""
        await ctx.send("<https://meta.stackexchange.com/q/66377/285481>\n\n"
                       "TL;DR: It's asking about your attempted solution "
                       "rather than your actual problem.\n"
                       "It's perfectly okay to want to learn about a "
                       "solution, but please be clear about your intentions "
                       "if you're not actually trying to solve a problem.")

    @commands.command(hidden=True, aliases=["guides", "link"])
    async def guide(self, ctx):
        """Link to the guide(s)"""
        await ctx.send("**Generic starter guides:**\n"
                       "AtlasNX's Guide: "
                       "<https://guide.teamatlasnx.com>\n"
                       "\n"
                       "**Specific guides:**\n"
                       "Manually Updating/Downgrading (with HOS): "
                       "<https://guide.sdsetup.com/usingcfw/manualupgrade>\n"
                       "Manually Repairing/Downgrading (without HOS): "
                       "<https://guide.sdsetup.com/usingcfw/manualchoiupgrade>\n"
                       "How to get started developing Homebrew: "
                       "<https://gbatemp.net/threads/"
                       "tutorial-switch-homebrew-development.507284/>\n"
                       "Getting full RAM in homebrew without NSPs: "
                       "as of Atmosphere 0.8.6, hold R while opening any game.")

    @commands.command(hidden=True, aliases=["patron"])
    async def patreon(self, ctx):
        """Link to the patreon"""
        await ctx.send("https://patreon.teamatlasnx.com")    

    @commands.command(hidden=True, aliases=["sdfiles"])
    async def kosmos(self, ctx):
        """Link to the Atmosphere repo"""
        await ctx.send("https://github.com/atlasnx/kosmos")

    @commands.command(hidden=True, aliases=["sd"])
    async def sdsetup(self, ctx):
        """Link to the Atmosphere repo"""
        await ctx.send("https://sdsetup.com")

    @commands.command()
    async def source(self, ctx):
        """Gives link to source code."""
        await ctx.send(f"You can find my source at {config.source_url}. "
                       "Serious PRs and issues welcome!")

def setup(bot):
    bot.add_cog(Links(bot))
