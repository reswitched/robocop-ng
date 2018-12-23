import time
import config

from discord.ext import commands


class Basic:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        """Says hello. Duh."""
        await ctx.send(f"Hello {ctx.author.mention}!")

    @commands.command()
    async def source(self, ctx):
        """Gives link to source code."""
        await ctx.send("You can find my source at " +
                       config.source_url +
                       ". Serious PRs and issues welcome!")

    @commands.command(aliases=['p'])
    async def ping(self, ctx):
        """Shows ping values to discord.

        RTT = Round-trip time, time taken to send a message to discord
        GW = Gateway Ping"""
        before = time.monotonic()
        tmp = await ctx.send('Calculating ping...')
        after = time.monotonic()
        rtt_ms = (after - before) * 1000
        gw_ms = self.bot.latency * 1000

        message_text = f":ping_pong: rtt: `{rtt_ms:.1f}ms`, `gw: {gw_ms:.1f}ms`"
        self.bot.log.info(message_text)
        await tmp.edit(content=message_text)


def setup(bot):
    bot.add_cog(Basic(bot))
