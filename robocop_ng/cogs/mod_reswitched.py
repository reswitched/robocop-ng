import config
from discord.ext import commands
from discord.ext.commands import Cog
from helpers.checks import check_if_staff
from helpers.memberlogs import log_own_member_update


class ModReswitched(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.hybrid_command(aliases=["pingmods", "summonmods"])
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
    @commands.hybrid_command(aliases=["togglemod"])
    async def modtoggle(self, ctx):
        """Toggles your mod role, staff only."""
        target_role = ctx.guild.get_role(config.modtoggle_role)

        if target_role in ctx.author.roles:
            await ctx.author.remove_roles(
                target_role, reason="Staff self-unassigned mod role"
            )
            await log_own_member_update(
                self.bot, ctx.author, remove_roles=[target_role]
            )
            await ctx.send(f"{ctx.author.mention}: Removed your mod role.")
        else:
            await ctx.author.add_roles(
                target_role, reason="Staff self-assigned mod role"
            )
            await log_own_member_update(self.bot, ctx.author, add_roles=[target_role])
            await ctx.send(f"{ctx.author.mention}: Gave you mod role.")


async def setup(bot):
    await bot.add_cog(ModReswitched(bot))
