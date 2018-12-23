import random
import config
import discord
from discord.ext import commands


class Meme:
    """
    Meme commands.
    """

    def __init__(self, bot):
        self.bot = bot

    def check_if_staff_or_ot(ctx):
        is_ot = (ctx.channel.name == "off-topic")
        is_staff = any(r.id in config.staff_role_ids for r in ctx.author.roles)
        return (is_ot or is_staff)

    @commands.check(check_if_staff_or_ot)
    @commands.command(hidden=True, name="bam")
    async def bam_member(self, ctx, user: discord.Member):
        """Bams a user owo"""
        await ctx.send(f"{self.bot.escape_message(user)} is ̶n͢ow b̕&̡.̷ 👍̡")

    @commands.check(check_if_staff_or_ot)
    @commands.command(hidden=True, name="warm")
    async def warm_member(self, ctx, user: discord.Member):
        """Warms a user :3"""
        await ctx.send(f"{user.mention} warmed."
                       f" User is now {random.randint(0, 100)}°C.")

    @commands.command(hidden=True)
    async def memebercount(self, ctx):
        """Checks memeber count, as requested by dvdfreitag"""
        await ctx.send("There's like, uhhhhh a bunch")

    @commands.command(hidden=True)
    async def frolics(self, ctx):
        """test"""
        await ctx.send("https://www.youtube.com/watch?v=VmarNEsjpDI")


def setup(bot):
    bot.add_cog(Meme(bot))
