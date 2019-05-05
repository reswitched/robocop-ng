import discord
from discord.ext import commands
import config
from helpers.checks import check_if_staff
from helpers.userlogs import userlog
from helpers.restrictions import add_restriction, remove_restriction

import cogs.mod_timed

class Mod:
    def __init__(self, bot):
        self.bot = bot

    def check_if_target_is_staff(self, target):
        return any(r.id in config.staff_role_ids for r in target.roles)

    @commands.guild_only()
    @commands.check(check_if_staff)
    @commands.command()
    async def mute(self, ctx, target: discord.Member, *, reason: str = ""):
        """Mutes a user, staff only."""
        # Hedge-proofing the code
        if target == ctx.author:
            return await ctx.send("You can't do mod actions on yourself.")
        elif self.check_if_target_is_staff(target):
            return await ctx.send("I can't mute this user as "
                                  "they're a member of staff.")

        userlog(target.id, ctx.author, reason, "mutes", target.name)

        safe_name = await commands.clean_content().convert(ctx, str(target))

        dm_message = f"You were muted!"
        if reason:
            dm_message += f" The given reason is: \"{reason}\"."

        try:
            await target.send(dm_message)
        except discord.errors.Forbidden:
            # Prevents kick issues in cases where user blocked bot
            # or has DMs disabled
            pass

        mute_role = ctx.guild.get_role(config.mute_role)

        await target.add_roles(mute_role, reason=str(ctx.author))

        chan_message = f"🔇 **Muted**: {ctx.author.mention} muted "\
                       f"{target.mention} | {safe_name}\n"\
                       f"🏷 __User ID__: {target.id}\n"
        if reason:
            chan_message += f"✏️ __Reason__: \"{reason}\""
        else:
            chan_message += "Please add an explanation below. In the future, "\
                            "it is recommended to use `.mute <user> [reason]`"\
                            " as the reason is automatically sent to the user."

        log_channel = self.bot.get_channel(config.log_channel)
        await log_channel.send(chan_message)
        await ctx.send(f"{target.mention} can no longer speak.")
        add_restriction(target.id, config.mute_role)

    @commands.guild_only()
    @commands.check(check_if_staff)
    @commands.command()
    async def unmute(self, ctx, target: discord.Member):
        """Unmutes a user, staff only."""
        safe_name = await commands.clean_content().convert(ctx, str(target))

        mute_role = ctx.guild.get_role(config.mute_role)
        await target.remove_roles(mute_role, reason=str(ctx.author))

        chan_message = f"🔈 **Unmuted**: {ctx.author.mention} unmuted "\
                       f"{target.mention} | {safe_name}\n"\
                       f"🏷 __User ID__: {target.id}\n"

        log_channel = self.bot.get_channel(config.log_channel)
        await log_channel.send(chan_message)
        await ctx.send(f"{target.mention} can now speak again.")
        remove_restriction(target.id, config.mute_role)

    @commands.guild_only()
    @commands.bot_has_permissions(kick_members=True)
    @commands.check(check_if_staff)
    @commands.command()
    async def kick(self, ctx, target: discord.Member, *, reason: str = ""):
        """Kicks a user, staff only."""
        # Hedge-proofing the code
        if target == ctx.author:
            return await ctx.send("You can't do mod actions on yourself.")
        elif self.check_if_target_is_staff(target):
            return await ctx.send("I can't kick this user as "
                                  "they're a member of staff.")

        userlog(target.id, ctx.author, reason, "kicks", target.name)

        safe_name = await commands.clean_content().convert(ctx, str(target))

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
                            ", it is recommended to use "\
                            "`.kick <user> [reason]`"\
                            " as the reason is automatically sent to the user."

        log_channel = self.bot.get_channel(config.log_channel)
        await log_channel.send(chan_message)

    @commands.guild_only()
    @commands.bot_has_permissions(ban_members=True)
    @commands.check(check_if_staff)
    @commands.command()
    async def ban(self, ctx, target: discord.Member, *, reason: str = ""):
        """Bans a user, staff only."""
        # Hedge-proofing the code
        if target == ctx.author:
            return await ctx.send("You can't do mod actions on yourself.")
        elif self.check_if_target_is_staff(target):
            return await ctx.send("I can't ban this user as "
                                  "they're a member of staff.")

        userlog(target.id, ctx.author, reason, "bans", target.name)

        safe_name = await commands.clean_content().convert(ctx, str(target))

        dm_message = f"You were banned from {ctx.guild.name}."
        if reason:
            dm_message += f" The given reason is: \"{reason}\"."
        dm_message += "\n\nThis ban does not expire."

        try:
            await target.send(dm_message)
        except discord.errors.Forbidden:
            # Prevents ban issues in cases where user blocked bot
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

        log_channel = self.bot.get_channel(config.log_channel)
        await log_channel.send(chan_message)
        await ctx.send(f"{safe_name} is now b&. 👍")

    @commands.guild_only()
    @commands.bot_has_permissions(ban_members=True)
    @commands.check(check_if_staff)
    @commands.command(aliases=["softban"])
    async def hackban(self, ctx, target: int, *, reason: str = ""):
        """Bans a user with their ID, doesn't message them, staff only."""
        target_user = await self.bot.get_user_info(target)
        target_member = ctx.guild.get_member(target)
        # Hedge-proofing the code
        if target == ctx.author.id:
            return await ctx.send("You can't do mod actions on yourself.")
        elif target_member and self.check_if_target_is_staff(target_member):
            return await ctx.send("I can't ban this user as "
                                  "they're a member of staff.")

        userlog(target, ctx.author, reason, "bans", target_user.name)

        safe_name = await commands.clean_content().convert(ctx, str(target))

        await ctx.guild.ban(target_user,
                            reason=f"{ctx.author}, reason: {reason}",
                            delete_message_days=0)
        chan_message = f"⛔ **Hackban**: {ctx.author.mention} banned "\
                       f"{target_user.mention} | {safe_name}\n"\
                       f"🏷 __User ID__: {target}\n"
        if reason:
            chan_message += f"✏️ __Reason__: \"{reason}\""
        else:
            chan_message += "Please add an explanation below. In the future"\
                            ", it is recommended to use "\
                            "`.hackban <user> [reason]`."

        log_channel = self.bot.get_channel(config.log_channel)
        await log_channel.send(chan_message)
        await ctx.send(f"{safe_name} is now b&. 👍")

    @commands.guild_only()
    @commands.bot_has_permissions(ban_members=True)
    @commands.check(check_if_staff)
    @commands.command()
    async def silentban(self, ctx, target: discord.Member, *, reason: str = ""):
        """Bans a user, staff only."""
        # Hedge-proofing the code
        if target == ctx.author:
            return await ctx.send("You can't do mod actions on yourself.")
        elif self.check_if_target_is_staff(target):
            return await ctx.send("I can't ban this user as "
                                  "they're a member of staff.")

        userlog(target.id, ctx.author, reason, "bans", target.name)

        safe_name = await commands.clean_content().convert(ctx, str(target))

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

        log_channel = self.bot.get_channel(config.log_channel)
        await log_channel.send(chan_message)

    @commands.guild_only()
    @commands.check(check_if_staff)
    @commands.command()
    async def approve(self, ctx, target: discord.Member,
                      role: str = config.default_named_role):
        """Add a role to a user (default: config.default_named_role), staff only."""
        if role not in config.named_roles:
            return await ctx.send("No such role! Available roles: " +
                                  ','.join(config.named_roles))

        log_channel = self.bot.get_channel(config.log_channel)
        target_role = ctx.guild.get_role(config.named_roles[role])

        if target_role in target.roles:
            return await ctx.send("Target already has this role.")

        await target.add_roles(target_role, reason=str(ctx.author))

        await ctx.send(f"Approved {target.mention} to `{role}` role.")

        await log_channel.send(f"✅ Approved: {ctx.author.mention} added"
                               f" {role} to {target.mention}")

    @commands.guild_only()
    @commands.check(check_if_staff)
    @commands.command(aliases=["unapprove"])
    async def revoke(self, ctx, target: discord.Member,
                     role: str = config.default_named_role):
        """Remove a role from a user (default: config.default_named_role), staff only."""
        if role not in config.named_roles:
            return await ctx.send("No such role! Available roles: " +
                                  ','.join(config.named_roles))

        log_channel = self.bot.get_channel(config.log_channel)
        target_role = ctx.guild.get_role(config.named_roles[role])

        if target_role not in target.roles:
            return await ctx.send("Target doesn't have this role.")

        await target.remove_roles(target_role, reason=str(ctx.author))

        await ctx.send(f"Un-approved {target.mention} from `{role}` role.")

        await log_channel.send(f"❌ Un-approved: {ctx.author.mention} removed"
                               f" {role} from {target.mention}")

    @commands.guild_only()
    @commands.check(check_if_staff)
    @commands.command(aliases=["clear"])
    async def purge(self, ctx, limit: int, channel: discord.TextChannel = None):
        """Clears a given number of messages, staff only."""
        log_channel = self.bot.get_channel(config.log_channel)
        if not channel:
            channel = ctx.channel
        await channel.purge(limit=limit)
        msg = f"🗑 **Purged**: {ctx.author.mention} purged {limit} "\
              f"messages in {channel.mention}."
        await log_channel.send(msg)

    @commands.guild_only()
    @commands.check(check_if_staff)
    @commands.command()
    async def warn(self, ctx, target: discord.Member, *, reason: str = ""):
        """Warns a user, staff only."""
        # Hedge-proofing the code
        if target == ctx.author:
            return await ctx.send("You can't do mod actions on yourself.")
        elif self.check_if_target_is_staff(target):
            return await ctx.send("I can't warn this user as "
                                  "they're a member of staff.")

        log_channel = self.bot.get_channel(config.log_channel)
        warn_count = userlog(target.id, ctx.author, reason,
                             "warns", target.name)

        msg = f"You were warned on {ctx.guild.name}."
        if reason:
            msg += " The given reason is: " + reason
        msg += f"\n\nPlease read the rules in {config.rules_url}. "\
               f"This is warn #{warn_count}."
        if warn_count == 2:
            msg += " __You have been muted for 15 minutes__"
            cogs.mod_timed.timeban.callback(ctx, target, 900, reason)
        if warn_count == 3:
            msg += " __You have been muted for 60 minutes__"
            cogs.mod_timed.timeban.callback(ctx, target, 3600, reason)
        if warn_count == 4:
            msg += " __You have been muted for 30 days__"
            cogs.mod_timed.timeban.callback(ctx, target, 2592000, reason)
        if warn_count == 5:
            msg += "\n\nYou were automatically banned due to five warnings."
        try:
            await target.send(msg)
        except discord.errors.Forbidden:
            # Prevents log issues in cases where user blocked bot
            # or has DMs disabled
            pass

        if warn_count >= 5:  # just in case
            await target.ban(reason="exceeded warn limit",
                             delete_message_days=0)
        await ctx.send(f"{target.mention} warned. "
                       f"User has {warn_count} warning(s).")

        safe_name = await commands.clean_content().convert(ctx, str(target))
        msg = f"⚠️ **Warned**: {ctx.author.mention} warned {target.mention}"\
              f" (warn #{warn_count}) | {safe_name}\n"

        if reason:
            msg += f"✏️ __Reason__: \"{reason}\""
        else:
            msg += "Please add an explanation below. In the future"\
                   ", it is recommended to use `.ban <user> [reason]`"\
                   " as the reason is automatically sent to the user."
        await log_channel.send(msg)

    @commands.guild_only()
    @commands.check(check_if_staff)
    @commands.command(aliases=["setnick", "nick"])
    async def nickname(self, ctx, target: discord.Member, *, nick: str = ""):
        """Sets a user's nickname, staff only.

        Just send .nickname <user> to wipe the nickname."""

        if nick:
            await target.edit(nick=nick, reason=str(ctx.author))
        else:
            await target.edit(nick=None, reason=str(ctx.author))

        await ctx.send("Successfully set nickname.")

    @commands.guild_only()
    @commands.check(check_if_staff)
    @commands.command(aliases=['echo'])
    async def say(self, ctx, *, the_text: str):
        """Repeats a given text, staff only."""
        await ctx.send(the_text)

    @commands.guild_only()
    @commands.check(check_if_staff)
    @commands.command()
    async def speak(self, ctx, channel: discord.TextChannel, *, the_text: str):
        """Repeats a given text in a given channel, staff only."""
        await channel.send(the_text)

    @commands.guild_only()
    @commands.check(check_if_staff)
    @commands.command(aliases=["setplaying", "setgame"])
    async def playing(self, ctx, *, game: str = ""):
        """Sets the bot's currently played game name, staff only.

        Just send .playing to wipe the playing state."""
        if game:
            await self.bot.change_presence(activity=discord.Game(name=game))
        else:
            await self.bot.change_presence(activity=None)

        await ctx.send("Successfully set game.")

    @commands.guild_only()
    @commands.check(check_if_staff)
    @commands.command(aliases=["setbotnick", "botnick", "robotnick"])
    async def botnickname(self, ctx, *, nick: str = ""):
        """Sets the bot's nickname, staff only.

        Just send .botnickname to wipe the nickname."""

        if nick:
            await ctx.guild.me.edit(nick=nick, reason=str(ctx.author))
        else:
            await ctx.guild.me.edit(nick=None, reason=str(ctx.author))

        await ctx.send("Successfully set bot nickname.")


def setup(bot):
    bot.add_cog(Mod(bot))
