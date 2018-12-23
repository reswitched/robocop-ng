import discord
from discord.ext import commands
import config


class AdminCog:
    def __init__(self, bot):
        self.bot = bot

    def check_if_staff(ctx):
        return any(r.id in config.staff_role_ids for r in ctx.author.roles)

    @commands.check(check_if_staff)
    @commands.command()
    async def userinfo(self, ctx, *, user: discord.Member):
        """Gets user info, staff only."""
        role = user.top_role.name
        if role == "@everyone":
            role = "@ everyone"
        await ctx.send(f"user = {user}\n"
                       f"id = {user.id}\n"
                       f"avatar = {user.avatar_url}\n"
                       f"bot = {user.bot}\n"
                       f"created_at = {user.created_at}\n"
                       f"display_name = {user.display_name}\n"
                       f"joined_at = {user.joined_at}\n"
                       f"activities = `{user.activities}`\n"
                       f"color = {user.colour}\n"
                       f"top_role = {role}\n")


def setup(bot):
    bot.add_cog(AdminCog(bot))
