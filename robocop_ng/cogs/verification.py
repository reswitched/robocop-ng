from discord.ext import commands
from discord.ext.commands import Cog
import asyncio
import config
import random
from inspect import cleandoc
import hashlib
from helpers.checks import check_if_staff


class Verification(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hash_choice = random.choice(config.welcome_hashes)

        # Export reset channel functions
        self.bot.do_reset = self.do_reset
        self.bot.do_resetalgo = self.do_resetalgo

    async def do_reset(self, channel, author, limit: int = 100):
        await channel.purge(limit=limit)

        await channel.send(config.welcome_header)
        rules = [
            "**{}**. {}".format(i, cleandoc(r))
            for i, r in enumerate(config.welcome_rules, 1)
        ]
        rule_choice = random.randint(2, len(rules))
        hash_choice_str = self.hash_choice.upper()
        if hash_choice_str == "BLAKE2B":
            hash_choice_str += "-512"
        elif hash_choice_str == "BLAKE2S":
            hash_choice_str += "-256"
        rules[rule_choice - 1] += "\n" + config.hidden_term_line.format(hash_choice_str)
        msg = (
            f"🗑 **Reset**: {author} cleared {limit} messages " f" in {channel.mention}"
        )
        msg += f"\n💬 __Current challenge location__: under rule {rule_choice}"
        log_channel = self.bot.get_channel(config.log_channel)
        await log_channel.send(msg)

        # find rule that puts us over 2,000 characters, if any
        total = 0
        messages = []
        current_message = ""
        for item in rules:
            total += len(item) + 2  # \n\n
            if total < 2000:
                current_message += item + "\n\n"
            else:
                # we've hit the limit; split!
                messages += [current_message]
                current_message = "\n\u200b\n" + item + "\n\u200b\n"
                total = 0
        messages += [current_message]

        for item in messages:
            await channel.send(item)
            await asyncio.sleep(1)

        for x in config.welcome_footer:
            await channel.send(cleandoc(x))
            await asyncio.sleep(1)

    async def do_resetalgo(self, channel, author, limit: int = 100):
        # randomize hash_choice on reset
        self.hash_choice = random.choice(tuple(config.welcome_hashes))

        msg = (
            f"📘 **Reset Algorithm**: {author} reset " f"algorithm in {channel.mention}"
        )
        msg += f"\n💬 __Current algorithm__: {self.hash_choice.upper()}"
        log_channel = self.bot.get_channel(config.log_channel)
        await log_channel.send(msg)

        await self.do_reset(channel, author)

    @commands.check(check_if_staff)
    @commands.hybrid_command()
    async def reset(self, ctx, limit: int = 100, force: bool = False):
        """Wipes messages and pastes the welcome message again. Staff only."""
        if ctx.channel.id != config.welcome_channel and not force:
            await ctx.send(
                f"This command is limited to"
                f" <#{config.welcome_channel}>, unless forced."
            )
            return
        await self.do_reset(ctx.channel, ctx.author.mention, limit)

    @commands.check(check_if_staff)
    @commands.hybrid_command()
    async def resetalgo(self, ctx, limit: int = 100, force: bool = False):
        """Resets the verification algorithm and does what reset does. Staff only."""
        if ctx.channel.id != config.welcome_channel and not force:
            await ctx.send(
                f"This command is limited to"
                f" <#{config.welcome_channel}>, unless forced."
            )
            return

        await self.do_resetalgo(ctx.channel, ctx.author.mention, limit)

    @commands.hybrid_command()
    async def verify(self, ctx, hash: str):
        """Verify yourself by submitting a special string.

        Read the rules in the welcome channel to see what to submit."""
        if ctx.channel.id != config.welcome_channel:
            return await ctx.send(
                f"This command can only be used in <#{config.welcome_channel}>.",
                ephemeral=True,
            )

        member = ctx.author
        guild = ctx.guild

        # Normalize the submitted hash so trailing whitespace/casing don't matter
        submitted = hash.strip().lower()

        # Get the role we will give in case of success
        success_role = guild.get_role(config.named_roles["participant"])

        # The things we'll accept a hash of
        allowed_names = [f"@{member.name}", member.name, str(member.id)]

        # Hash each accepted name with the currently-chosen algorithm
        hash_allow = [
            hashlib.new(self.hash_choice, name.encode("utf-8")).hexdigest()
            for name in allowed_names
        ]

        if submitted in hash_allow:
            await member.add_roles(success_role)
            return await ctx.send(
                ":white_check_mark: You've been verified! You now have access to"
                " the other channels. Welcome!",
                ephemeral=True,
            )

        # Detect if the user used the wrong hash algorithm
        wrong_hash_algos = set(config.welcome_hashes) - {self.hash_choice}
        for algo in wrong_hash_algos:
            for name in allowed_names:
                if hashlib.new(algo, name.encode("utf-8")).hexdigest() == submitted:
                    log_channel = self.bot.get_channel(config.log_channel)
                    await log_channel.send(
                        f"User {member.mention} tried verification with algo"
                        f" {algo} instead of {self.hash_choice}."
                    )
                    return await ctx.send(
                        ":no_entry: Close, but not quite. Go back and re-read!",
                        ephemeral=True,
                    )

        await ctx.send(
            ":no_entry: Incorrect. Make sure you're submitting the correct hex"
            " digest of your username. Please re-read the rules carefully and look"
            " up any terms you are not familiar with.",
            ephemeral=True,
        )


async def setup(bot):
    await bot.add_cog(Verification(bot))
