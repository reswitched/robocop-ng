import config
from discord.ext import commands
from discord.ext.commands import Cog


class BasicReswitched(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.command()
    async def communitycount(self, ctx):
        """Prints the community member count of the server."""
        community = ctx.guild.get_role(config.named_roles["community"])
        await ctx.send(
            f"{ctx.guild.name} has {len(community.members)} community members!"
        )

    @commands.guild_only()
    @commands.command()
    async def hackercount(self, ctx):
        """Prints the hacker member count of the server."""
        h4x0r = ctx.guild.get_role(config.named_roles["hacker"])
        await ctx.send(
            f"{ctx.guild.name} has {len(h4x0r.members)} people with hacker role!"
        )


async def setup(bot):
    await bot.add_cog(BasicReswitched(bot))
