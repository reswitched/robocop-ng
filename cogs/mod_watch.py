import discord
from discord.ext import commands
from discord.ext.commands import Cog
from helpers.checks import check_if_staff
from helpers.userlogs import setwatch


class ModWatch(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.check(check_if_staff)
    @commands.command()
    async def watch(self, ctx, target: discord.Member, *, note: str = ""):
        """Puts a user under watch, staff only."""
        setwatch(target.id, ctx.author, True, target.name)
        await ctx.send(f"{ctx.author.mention}: user is now on watch.")


    @commands.guild_only()
    @commands.check(check_if_staff)
    @commands.command()
    async def unwatch(self, ctx, target: discord.Member, *, note: str = ""):
        """Removes a user from watch, staff only."""
        setwatch(target.id, ctx.author, False, target.name)
        await ctx.send(f"{ctx.author.mention}: user is now not on watch.")

def setup(bot):
    bot.add_cog(ModWatch(bot))
