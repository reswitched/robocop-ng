from discord.ext import commands
import config
import discord
from helpers.checks import check_if_staff


class Lockdown:
    def __init__(self, bot):
        self.bot = bot

    async def unlock_for_staff(self, channel: discord.TextChannel, issuer):
        for role in config.staff_role_ids:
            try:
                await channel.set_permissions(channel.guild.get_role(role),
                                              send_messages=False,
                                              reason=str(issuer))
            except:
                pass

    @commands.guild_only()
    @commands.check(check_if_staff)
    @commands.command()
    async def lock(self, ctx, channel: discord.TextChannel = None,
                   soft: bool = False):
        """Prevents people from speaking in a channel, staff only.

        Defaults to current channel."""
        if not channel:
            channel = ctx.channel
        log_channel = self.bot.get_channel(config.log_channel)

        if channel.id in config.community_channels:
            roles = [config.named_roles["community"],
                     config.named_roles["hacker"]]
        else:
            roles = [config.named_roles["participant"],
                     ctx.guild.default_role.id]

        for role in roles:
            await channel.set_permissions(channel.guild.get_role(role),
                                          send_messages=False,
                                          reason=str(ctx.author))

        await self.unlock_for_staff(channel, ctx.author)

        public_msg = "🔒 Channel locked down. "
        if not soft:
            public_msg += "Only staff members may speak. "\
                          "Do not bring the topic to other channels or risk "\
                          "disciplinary actions."

        await ctx.send(public_msg)
        msg = f"🔒 **Lockdown**: {ctx.channel.mention} by {ctx.author.mention} "\
              f"| {self.bot.escape_message(ctx.author)}"
        await log_channel.send(msg)

    @commands.guild_only()
    @commands.check(check_if_staff)
    @commands.command()
    async def unlock(self, ctx, channel: discord.TextChannel = None):
        """Unlocks speaking in current channel, staff only."""
        if not channel:
            channel = ctx.channel
        log_channel = self.bot.get_channel(config.log_channel)

        if ctx.channel.id in config.community_channels:
            roles = [config.named_roles["community"],
                     config.named_roles["hacker"]]
        else:
            roles = [config.named_roles["participant"],
                     ctx.guild.default_role.id]

        await self.unlock_for_staff(channel, ctx.author)

        for role in roles:
            await ctx.channel.set_permissions(ctx.guild.get_role(role),
                                              send_messages=True,
                                              reason=str(ctx.author))

        await ctx.send("🔓 Channel unlocked.")
        msg = f"🔓 **Unlock**: {ctx.channel.mention} by {ctx.author.mention} "\
              f"| {self.bot.escape_message(ctx.author)}"
        await log_channel.send(msg)


def setup(bot):
    bot.add_cog(Lockdown(bot))
