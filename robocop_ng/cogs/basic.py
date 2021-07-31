import time
import config
import discord
from discord.ext import commands
from discord.ext.commands import Cog


class Basic(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        """Says hello. Duh."""
        await ctx.send(f"Hello {ctx.author.mention}!")

    @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.command(name="hex")
    async def _hex(self, ctx, num: int):
        """Converts base 10 to 16 (for emummc sector calculation)"""
        hex_val = hex(num).upper().replace("0X", "0x")
        await ctx.send(f"{ctx.author.mention}: {hex_val}")

    @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.command(name="dec")
    async def _dec(self, ctx, num):
        """Converts base 10 to 16"""
        await ctx.send(f"{ctx.author.mention}: {int(num, 16)}")

    @commands.guild_only()
    @commands.command()
    async def membercount(self, ctx):
        """Prints the member count of the server."""
        await ctx.send(f"{ctx.guild.name} has {ctx.guild.member_count} members!")

    @commands.command(aliases=["robocopng", "robocop-ng"])
    async def robocop(self, ctx):
        """Shows a quick embed with bot info."""
        embed = discord.Embed(
            title="Robocop-NG", url=config.source_url, description=config.embed_desc
        )

        embed.set_thumbnail(url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(aliases=["p"])
    async def ping(self, ctx):
        """Shows ping values to discord.

        RTT = Round-trip time, time taken to send a message to discord
        GW = Gateway Ping"""
        before = time.monotonic()
        tmp = await ctx.send("Calculating ping...")
        after = time.monotonic()
        rtt_ms = (after - before) * 1000
        gw_ms = self.bot.latency * 1000

        message_text = (
            f":ping_pong:\nrtt: `{rtt_ms:.1f}ms`\ngw: `{gw_ms:.1f}ms`"
        )
        self.bot.log.info(message_text)
        await tmp.edit(content=message_text)


def setup(bot):
    bot.add_cog(Basic(bot))
