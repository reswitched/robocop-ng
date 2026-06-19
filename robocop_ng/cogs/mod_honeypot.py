import discord
from discord import Message, Embed, utils
from discord.ext.commands import Cog

from robocop_ng.helpers.userlogs import userlog


class ModHoneypot(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message: Message):
        await self.bot.wait_until_ready()
        if not self.bot.intents.message_content:
            return
        if message.channel.id != getattr(self.bot.config, "honeypot_channel", 0):
            return
        if any(r.id in self.bot.config.staff_role_ids for r in message.author.roles):
            return

        has_attachments = len(message.attachments) > 0
        spy_channel = await self.bot.get_channel_safe(self.bot.config.spylog_channel)
        log_channel = await self.bot.get_channel_safe(self.bot.config.modlog_channel)
        ban_reason = "Sent a message in honeypot channel"

        spylog_message = (
            f"🍯 Message sent to honeypot channel by {message.author.mention} "
            f"({message.author.id}):"
            f"\n- Has attachments: {has_attachments}"
        )
        if has_attachments:
            spylog_message += "\n\nAttachments:"
        for attachment in message.attachments:
            spylog_message += (
                f"\n- {attachment.filename} (type: {attachment.content_type}): "
            )
            if attachment.proxy_url is None or len(attachment.proxy_url) == 0:
                spylog_message += f"<{attachment.proxy_url}>"
            else:
                spylog_message += f"<{attachment.url}>"

        spylog_embed = Embed(description=utils.escape_markdown(message.clean_content))
        spylog_embed.set_author(
            name=message.author.display_name, icon_url=message.author.display_avatar.url
        )
        if spy_channel:
            spy_message = await spy_channel.send(spylog_message, embed=spylog_embed)
            log_reason = ban_reason + f", see: {spy_message.jump_url}"
        else:
            log_reason = ban_reason

        userlog(
            self.bot,
            message.author.id,
            self.bot.user,
            log_reason,
            "bans",
            message.author.name,
        )

        dm_message = (
            f"You were banned from {message.guild.name}. "
            f'The given reason is: "{ban_reason}".'
            "\n\nThis ban does not expire."
        )

        try:
            await message.author.send(dm_message)
        except discord.errors.Forbidden:
            pass

        await message.author.ban(
            delete_message_days=1,
            reason=ban_reason,
        )

        safe_name = utils.escape_markdown(str(message.author))
        log_message = (
            f"⛔ **Ban**: {str(self.bot.user)} banned with 1 day of messages deleted "
            f"{message.author.mention} | {safe_name}\n"
            f"🏷 __User ID__: {message.author.id}\n"
            f'✏️ __Reason__: "{log_reason}"'
        )
        if log_channel:
            await log_channel.send(log_message)


async def setup(bot):
    await bot.add_cog(ModHoneypot(bot))
