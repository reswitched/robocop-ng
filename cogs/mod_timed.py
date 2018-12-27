import discord
import config
import time
from discord.ext import commands
from helpers.checks import check_if_staff
from helpers.robocronp import add_job
from helpers.userlogs import userlog
from helpers.restrictions import add_restriction


class ModTimed:
    def __init__(self, bot):
        self.bot = bot

    def check_if_target_is_staff(self, target):
        return any(r.id in config.staff_role_ids for r in target.roles)

    @commands.guild_only()
    @commands.bot_has_permissions(ban_members=True)
    @commands.check(check_if_staff)
    @commands.command()
    async def timeban(self, ctx, target: discord.Member,
                      hours: int, *, reason: str = ""):
        """Bans a user for a specified amount of hours, staff only."""
        # Hedge-proofing the code
        if target == ctx.author:
            return await ctx.send("You can't do mod actions on yourself.")
        elif self.check_if_target_is_staff(target):
            return await ctx.send("I can't ban this user as "
                                  "they're a member of staff.")

        userlog(target.id, ctx.author, f"{reason} (Timed, for {hours}h)",
                "bans", target.name)

        safe_name = self.bot.escape_message(str(target))

        dm_message = f"You were banned from {ctx.guild.name}."
        if reason:
            dm_message += f" The given reason is: \"{reason}\"."
        dm_message += f"\n\nThis ban will expire in {hours} hours."

        try:
            await target.send(dm_message)
        except discord.errors.Forbidden:
            # Prevents ban issues in cases where user blocked bot
            # or has DMs disabled
            pass

        await target.ban(reason=f"{ctx.author}, reason: {reason}",
                         delete_message_days=0)
        chan_message = f"⛔ **Timed Ban**: {ctx.author.mention} banned "\
                       f"{target.mention} for {hours} hours | {safe_name}\n"\
                       f"🏷 __User ID__: {target.id}\n"
        if reason:
            chan_message += f"✏️ __Reason__: \"{reason}\""
        else:
            chan_message += "Please add an explanation below. In the future"\
                            ", it is recommended to use `.ban <user> [reason]`"\
                            " as the reason is automatically sent to the user."

        expiry_timestamp = time.time() + (hours * 3600)
        add_job("unban", target.id, {"guild": ctx.guild.id}, expiry_timestamp)

        log_channel = self.bot.get_channel(config.log_channel)
        await log_channel.send(chan_message)
        await ctx.send(f"{safe_name} is now b& for {hours} hours. 👍")

    @commands.guild_only()
    @commands.check(check_if_staff)
    @commands.command()
    async def timemute(self, ctx, target: discord.Member,
                       hours: int, *, reason: str = ""):
        """Mutes a user for a specified amount of hours, staff only."""
        # Hedge-proofing the code
        if target == ctx.author:
            return await ctx.send("You can't do mod actions on yourself.")
        elif self.check_if_target_is_staff(target):
            return await ctx.send("I can't mute this user as "
                                  "they're a member of staff.")

        userlog(target.id, ctx.author, f"{reason} (Timed, for {hours}h)",
                "mutes", target.name)

        safe_name = self.bot.escape_message(str(target))

        dm_message = f"You were muted!"
        if reason:
            dm_message += f" The given reason is: \"{reason}\"."
        dm_message += f"\n\nThis mute will expire in {hours} hours."

        try:
            await target.send(dm_message)
        except discord.errors.Forbidden:
            # Prevents kick issues in cases where user blocked bot
            # or has DMs disabled
            pass

        mute_role = ctx.guild.get_role(config.mute_role)

        await target.add_roles(mute_role, reason=str(ctx.author))

        chan_message = f"🔇 **Timed Mute**: {ctx.author.mention} muted "\
                       f"{target.mention} for {hours} hours | {safe_name}\n"\
                       f"🏷 __User ID__: {target.id}\n"
        if reason:
            chan_message += f"✏️ __Reason__: \"{reason}\""
        else:
            chan_message += "Please add an explanation below. In the future, "\
                            "it is recommended to use `.mute <user> [reason]`"\
                            " as the reason is automatically sent to the user."

        expiry_timestamp = time.time() + (hours * 3600)
        add_job("unmute", target.id, {"guild": ctx.guild.id}, expiry_timestamp)

        log_channel = self.bot.get_channel(config.log_channel)
        await log_channel.send(chan_message)
        await ctx.send(f"{target.mention} can no longer speak.")
        add_restriction(target.id, config.mute_role)


def setup(bot):
    bot.add_cog(ModTimed(bot))
