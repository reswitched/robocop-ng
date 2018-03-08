import time

from discord.ext import commands


class Basic:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def invite(self, ctx):
        """Sends an invite to add the bot"""
        await ctx.send(f"{ctx.author.mention}: You can use "
                       "<https://discordapp.com/api/oauth2/authorize?"
                       f"client_id={self.bot.user.id}"
                       "&permissions=268435456&scope=bot> "
                       "to add RoleBot to your guild.")

    @commands.command()
    async def hello(self, ctx):
        """Says hello. Duh."""
        await ctx.send(f"Hello {ctx.author.mention}!")

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
