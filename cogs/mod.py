import discord
from discord.ext import commands
import config


class ModCog:
    def __init__(self, bot):
        self.bot = bot

    def check_if_staff(ctx):
        return any(r.id in config.staff_role_ids for r in ctx.author.roles)

    def check_if_target_is_staff(self, target):
        return any(r.id in config.staff_role_ids for r in target.roles)

    @commands.bot_has_permissions(kick_members=True)
    @commands.check(check_if_staff)
    @commands.command()
    async def kick(self, ctx, target: discord.Member, *, reason: str = ""):
        """Kicks a user, staff only."""
        if self.check_if_target_is_staff(target):
            return await ctx.send("I can't kick this user as "
                                  "they're a member of staff.")

        safe_name = self.bot.escape_message(str(target))

        dm_message = f"You were kicked from {ctx.guild.name}."
        if reason:
            dm_message += f" The given reason is: \"{reason}\"."
        dm_message += "\n\nYou are able to rejoin the server,"\
                      " but please be sure to behave when participating again."

        try:
            await target.send(dm_message)
        except discord.errors.Forbidden:
            # Prevents kick issues in cases where user blocked bot
            # or has DMs disabled
            pass

        await target.kick(reason=f"{ctx.author}, reason: {reason}")
        chan_message = f"👢 **Kick**: {ctx.author.mention} kicked "\
                       f"{target.mention} | {safe_name}\n"\
                       f"🏷 __User ID__: {target.id}\n"
        if reason:
            chan_message += f"✏️ __Reason__: \"{reason}\""
        else:
            chan_message += "Please add an explanation below. In the future"\
                            ", it is recommended to use `.ban <user> [reason]`"\
                            " as the reason is automatically sent to the user."

        modlog_channel = self.bot.get_channel(config.modlog_channel)
        await modlog_channel.send(chan_message)

    @commands.bot_has_permissions(ban_members=True)
    @commands.check(check_if_staff)
    @commands.command()
    async def ban(self, ctx, target: discord.Member, *, reason: str = ""):
        """Bans a user, staff only."""
        if self.check_if_target_is_staff(target):
            return await ctx.send("I can't ban this user as "
                                  "they're a member of staff.")

        safe_name = self.bot.escape_message(str(target))

        dm_message = f"You were banned from {ctx.guild.name}."
        if reason:
            dm_message += f" The given reason is: \"{reason}\"."
        dm_message += "\n\nThis ban does not expire."

        try:
            await target.send(dm_message)
        except discord.errors.Forbidden:
            # Prevents kick issues in cases where user blocked bot
            # or has DMs disabled
            pass

        await target.ban(reason=f"{ctx.author}, reason: {reason}",
                         delete_message_days=0)
        chan_message = f"⛔ **Ban**: {ctx.author.mention} banned "\
                       f"{target.mention} | {safe_name}\n"\
                       f"🏷 __User ID__: {target.id}\n"
        if reason:
            chan_message += f"✏️ __Reason__: \"{reason}\""
        else:
            chan_message += "Please add an explanation below. In the future"\
                            ", it is recommended to use `.ban <user> [reason]`"\
                            " as the reason is automatically sent to the user."

        modlog_channel = self.bot.get_channel(config.modlog_channel)
        await modlog_channel.send(chan_message)
        await ctx.send(f"{safe_name} is now b&. 👍")

    @commands.bot_has_permissions(ban_members=True)
    @commands.check(check_if_staff)
    @commands.command()
    async def silentban(self, ctx, target: discord.Member, *, reason: str = ""):
        """Bans a user, staff only."""
        if self.check_if_target_is_staff(target):
            return await ctx.send("I can't ban this user as "
                                  "they're a member of staff.")

        safe_name = self.bot.escape_message(str(target))

        await target.ban(reason=f"{ctx.author}, reason: {reason}",
                         delete_message_days=0)
        chan_message = f"⛔ **Silent ban**: {ctx.author.mention} banned "\
                       f"{target.mention} | {safe_name}\n"\
                       f"🏷 __User ID__: {target.id}\n"
        if reason:
            chan_message += f"✏️ __Reason__: \"{reason}\""
        else:
            chan_message += "Please add an explanation below. In the future"\
                            ", it is recommended to use `.ban <user> [reason]`"\
                            " as the reason is automatically sent to the user."

        modlog_channel = self.bot.get_channel(config.modlog_channel)
        await modlog_channel.send(chan_message)

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
    bot.add_cog(ModCog(bot))
