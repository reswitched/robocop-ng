import config
from discord.ext import commands
from discord.ext.commands import Cog
from helpers.checks import check_if_staff


class ModReswitched(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.command(aliases=["pingmods", "summonmods"])
    async def pingmod(self, ctx):
        """Pings mods, only use when there's an emergency."""
        can_ping = any(r.id in config.pingmods_allow for r in ctx.author.roles)
        if can_ping:
            await ctx.send(
                f"<@&{config.pingmods_role}>: {ctx.author.mention} needs assistance."
            )
        else:
            await ctx.send(
                f"{ctx.author.mention}: You need the community role to be able to ping the entire mod team, please pick an online mod (not staff, please!), and ping them instead."
            )

    @commands.guild_only()
    @commands.check(check_if_staff)
    @commands.command(aliases=["togglemod"])
    async def modtoggle(self, ctx):
        """Toggles your mod role, staff only."""
        target_role = ctx.guild.get_role(config.modtoggle_role)

        if target_role in ctx.author.roles:
            await ctx.author.remove_roles(
                target_role, reason="Staff self-unassigned mod role"
            )
            await ctx.send(f"{ctx.author.mention}: Removed your mod role.")
        else:
            await ctx.author.add_roles(
                target_role, reason="Staff self-assigned mod role"
            )
            await ctx.send(f"{ctx.author.mention}: Gave you mod role.")


async def setup(bot):
    await bot.add_cog(ModReswitched(bot))
