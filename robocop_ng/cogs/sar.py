import config
from discord.ext import commands
from discord.ext.commands import Cog
from helpers.checks import check_if_staff_or_ot


class SAR(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.command()
    @commands.check(check_if_staff_or_ot)
    async def sar(self, ctx):
        """Lists self assignable roles."""
        return await ctx.send(
            "Self assignable roles in this guild: "
            + ",".join(config.self_assignable_roles)
            + f"\n\nRun `{config.prefixes[0]}iam role_name_goes_here` to get or remove one."
        )

    @commands.cooldown(1, 30, type=commands.BucketType.user)
    @commands.guild_only()
    @commands.command(aliases=["iamnot"])
    @commands.check(check_if_staff_or_ot)
    async def iam(self, ctx, role: str):
        """Gets you a self assignable role."""
        if role not in config.self_assignable_roles:
            return await ctx.send(
                "There's no self assignable role with that name. Run .sar to see what you can self assign."
            )

        target_role = ctx.guild.get_role(config.self_assignable_roles[role])

        if target_role in ctx.author.roles:
            await ctx.author.remove_roles(target_role, reason=str(ctx.author))
            await ctx.send(
                f"{ctx.author.mention}: Successfully removed your `{role}` role. Run the command again if you want to add it again."
            )
        else:
            await ctx.author.add_roles(target_role, reason=str(ctx.author))
            await ctx.send(
                f"{ctx.author.mention}: Successfully gave you the `{role}` role. Run the command again if you want to remove it."
            )


async def setup(bot):
    await bot.add_cog(SAR(bot))
