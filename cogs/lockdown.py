from discord.ext import commands
import config


class Lockdown:
    def __init__(self, bot):
        self.bot = bot

    def check_if_staff(ctx):
        return any(r.id in config.staff_role_ids for r in ctx.author.roles)

    @commands.guild_only()
    @commands.check(check_if_staff)
    @commands.command()
    async def lock(self, ctx, soft: bool = False):
        """Prevents people from speaking in current channel, staff only."""
        log_channel = self.bot.get_channel(config.log_channel)

        if ctx.channel.id in config.community_channels:
            roles = [config.named_roles["community"],
                     config.named_roles["hacker"]]
        else:
            roles = [config.named_roles["participant"],
                     ctx.guild.default_role.id]

        for role in roles:
            await ctx.channel.set_permissions(ctx.guild.get_role(role),
                                              send_messages=False,
                                              reason=str(ctx.author))

        public_msg = "🔒 Channel locked down. "
        if not soft:
            public_msg += "Only staff members may speak. "\
                          "Do not bring the topic to other channels or risk "\
                          "disciplinary actions."

        await ctx.send(public_msg)
        msg = f"🔒 **Lockdown**: {ctx.channel.mention} by {ctx.author.mention} "\
              f"| {self.bot.escape_message(ctx.author)}"
        # ":unlock: Channel unlocked."
        await log_channel.send(msg)

    @commands.guild_only()
    @commands.check(check_if_staff)
    @commands.command()
    async def unlock(self, ctx):
        """Unlocks speaking in current channel, staff only."""
        log_channel = self.bot.get_channel(config.log_channel)

        if ctx.channel.id in config.community_channels:
            roles = [config.named_roles["community"],
                     config.named_roles["hacker"]]
        else:
            roles = [config.named_roles["participant"],
                     ctx.guild.default_role.id]

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
