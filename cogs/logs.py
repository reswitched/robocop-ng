import discord
import json
import re
import config
from helpers.restrictions import get_user_restrictions


class Logs:
    """
    Logs join and leave messages, bans and unbans, and member changes.
    """

    def __init__(self, bot):
        self.bot = bot
        self.invite_re = re.compile(r"((discord\.gg|discordapp\.com/"
                                    r"+invite)/+[a-zA-Z0-9-]+)")
        self.name_re = re.compile(r"[a-zA-Z0-9].*")
        self.clean_re = re.compile(r'[\W_]+', re.UNICODE)
        # All lower case, no spaces, nothing non-alphanumeric
        self.susp_words = ["sx", "tx", "reinx", "tinfoil", "dz", "goldleaf",
                           "nsp", "xci", "nut", "doge", "cdnsp"]
        self.ok_words = ["nspwn", "hblnsp", "exefs"]

    async def on_member_join(self, member):
        await self.bot.wait_until_ready()
        log_channel = self.bot.get_channel(config.log_channel)
        # We use this a lot, might as well get it once
        escaped_name = self.bot.escape_message(member)

        # Check if user account is older than 15 minutes
        age = member.joined_at - member.created_at
        if age < config.min_age:
            try:
                await member.send(f"Your account is too new to "
                                  f"join {member.guild.name}."
                                  " Please try again later.")
                sent = True
            except discord.errors.Forbidden:
                sent = False
            await member.kick(reason="Too new")
            msg = f"🚨 **Account too new**: {member.mention} | "\
                  f"{escaped_name}\n"\
                  f"🗓 __Creation__: {member.created_at}\n"\
                  f"🕓 Account age: {age}\n"\
                  f"🏷 __User ID__: {member.id}"
            if not sent:
                msg += "\nThe user has disabled direct messages,"\
                       " so the reason was not sent."
            await log_channel.send(msg)
            return
        msg = f"✅ **Join**: {member.mention} | "\
              f"{escaped_name}\n"\
              f"🗓 __Creation__: {member.created_at}\n"\
              f"🕓 Account age: {age}\n"\
              f"🏷 __User ID__: {member.id}"

        # Handles user restrictions
        # Basically, gives back muted role to users that leave with it.
        rsts = get_user_restrictions(member.id)
        roles = [discord.utils.get(member.guild.roles, id=rst) for rst in rsts]
        await member.add_roles(*roles)

        # Real hell zone.
        with open("data/userlog.json", "r") as f:
            warns = json.load(f)
        try:
            if len(warns[str(member.id)]["warns"]) == 0:
                await log_channel.send(msg)
            else:
                embed = discord.Embed(color=discord.Color.dark_red(),
                                      title=f"Warns for {escaped_name}")
                embed.set_thumbnail(url=member.avatar_url)
                for idx, warn in enumerate(warns[str(member.id)]["warns"]):
                    embed.add_field(name=f"{idx + 1}: {warn['timestamp']}",
                                    value=f"Issuer: {warn['issuer_name']}"
                                          f"\nReason: {warn['reason']}")
                await log_channel.send(msg, embed=embed)
        except KeyError:  # if the user is not in the file
            await log_channel.send(msg)

    async def do_spy(self, message):
        alert = False
        cleancont = self.clean_re.sub('', message.content).lower()
        msg = f"🚨 Suspicious message by {message.author.mention} "\
              f"({message.author.id}):"

        invites = self.invite_re.findall(message.content.lower())
        for invite in invites:
            msg += f"\n- Has invite: https://{invite[0]}"
            alert = True

        for susp_word in self.susp_words:
            if susp_word in cleancont and\
                    not any(ok_word in cleancont for ok_word in self.ok_words):
                msg += f"\n- Contains suspicious word: `{susp_word}`"
                alert = True

        if alert:
            msg += f"\n\nJump: <{message.jump_url}>"
            spy_channel = self.bot.get_channel(config.spylog_channel)
            await spy_channel.send(msg)

    async def do_nickcheck(self, message):
        compliant = self.name_re.fullmatch(message.author.display_name)
        if compliant:
            return

        msg = f"R11 violating name by {message.author.mention} "\
              f"({message.author.id})."

        spy_channel = self.bot.get_channel(config.spylog_channel)
        await spy_channel.send(msg)

    async def on_message(self, message):
        await self.bot.wait_until_ready()
        if message.channel.id not in config.spy_channels:
            return

        await self.do_spy(message)

    async def on_message_edit(self, before, after):
        await self.bot.wait_until_ready()
        if after.channel.id not in config.spy_channels or after.author.bot:
            return

        # If content is the same, just skip over it
        # This usually means that something embedded.
        if before.clean_content == after.clean_content:
            return

        await self.do_spy(after)

        log_channel = self.bot.get_channel(config.log_channel)
        msg = "📝 **Message edit**: \n"\
              f"from {self.bot.escape_message(after.author.name)} "\
              f"({after.author.id}), in {after.channel.mention}:\n"\
              f"`{before.clean_content}` → `{after.clean_content}`"

        # If resulting message is too long, upload to hastebin
        if len(msg) > 2000:
            haste_url = await self.bot.haste(msg)
            msg = f"📝 **Message edit**: \nToo long: <{haste_url}>"

        await log_channel.send(msg)

    async def on_message_delete(self, message):
        await self.bot.wait_until_ready()
        if message.channel.id not in config.spy_channels or message.author.bot:
            return

        log_channel = self.bot.get_channel(config.log_channel)
        msg = "🗑️ **Message delete**: \n"\
              f"from {self.bot.escape_message(message.author.name)} "\
              f"({message.author.id}), in {message.channel.mention}:\n"\
              f"`{message.clean_content}`"

        # If resulting message is too long, upload to hastebin
        if len(msg) > 2000:
            haste_url = await self.bot.haste(msg)
            msg = f"🗑️ **Message delete**: \nToo long: <{haste_url}>"

        await log_channel.send(msg)

    async def on_member_remove(self, member):
        await self.bot.wait_until_ready()
        log_channel = self.bot.get_channel(config.log_channel)
        msg = f"⬅️ **Leave**: {member.mention} | "\
              f"{self.bot.escape_message(member)}\n"\
              f"🏷 __User ID__: {member.id}"
        await log_channel.send(msg)

    async def on_member_ban(self, guild, member):
        await self.bot.wait_until_ready()
        log_channel = self.bot.get_channel(config.modlog_channel)
        msg = f"⛔ **Ban**: {member.mention} | "\
              f"{self.bot.escape_message(member)}\n"\
              f"🏷 __User ID__: {member.id}"
        await log_channel.send(msg)

    async def on_member_unban(self, guild, user):
        await self.bot.wait_until_ready()
        log_channel = self.bot.get_channel(config.modlog_channel)
        msg = f"⚠️ **Unban**: {user.mention} | "\
              f"{self.bot.escape_message(user)}\n"\
              f"🏷 __User ID__: {user.id}"
        # if user.id in self.bot.timebans:
        #     msg += "\nTimeban removed."
        #     self.bot.timebans.pop(user.id)
        #     with open("data/timebans.json", "r") as f:
        #         timebans = json.load(f)
        #     if user.id in timebans:
        #         timebans.pop(user.id)
        #         with open("data/timebans.json", "w") as f:
        #             json.dump(timebans, f)
        await log_channel.send(msg)

    async def on_member_update(self, member_before, member_after):
        await self.bot.wait_until_ready()
        msg = ""
        log_channel = self.bot.get_channel(config.log_channel)
        if member_before.roles != member_after.roles:
            # role removal
            role_removal = []
            for index, role in enumerate(member_before.roles):
                if role not in member_after.roles:
                    role_removal.append(role)
            # role addition
            role_addition = []
            for index, role in enumerate(member_after.roles):
                if role not in member_before.roles:
                    role_addition.append(role)

            if len(role_addition) != 0 or len(role_removal) != 0:
                msg += "\n👑 __Role change__: "
                roles = []
                for role in role_removal:
                    roles.append("_~~" + role.name + "~~_")
                for role in role_addition:
                    roles.append("__**" + role.name + "**__")
                for index, role in enumerate(member_after.roles):
                    if role.name == "@everyone":
                        continue
                    if role not in role_removal and role not in role_addition:
                        roles.append(role.name)
                msg += ", ".join(roles)

        if member_before.name != member_after.name:
            msg += "\n📝 __Username change__: "\
                   f"{self.bot.escape_message(member_before)} → "\
                   f"{self.bot.escape_message(member_after)}"
        if member_before.nick != member_after.nick:
            if not member_before.nick:
                msg += "\n🏷 __Nickname addition__"
            elif not member_after.nick:
                msg += "\n🏷 __Nickname removal__"
            else:
                msg += "\n🏷 __Nickname change__"
            msg += f": {self.bot.escape_message(member_before.nick)} → "\
                   f"{self.bot.escape_message(member_after.nick)}"
        if msg:
            msg = f"ℹ️ **Member update**: {member_after.mention} | "\
                  f"{self.bot.escape_message(member_after)}{msg}"
            await log_channel.send(msg)


def setup(bot):
    bot.add_cog(Logs(bot))
