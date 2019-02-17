import discord
from discord.ext import commands
import asyncio
import config
import random
from inspect import cleandoc
import hashlib
from helpers.checks import check_if_staff


welcome_header = """
<:ReSwitched:326421448543567872> __**Welcome to ReSwitched!**__

__**Be sure you read the following rules and information before participating. If you came here to ask about "backups", this is NOT the place.**__

__**Got questions about Nintendo Switch hacking? Before asking in the server, please see our FAQ at <https://reswitched.team/faq/> to see if your question has already been answered.**__

​:bookmark_tabs:__Rules:__
"""

welcome_rules = (
    # 1
    """
    Read all the rules before participating in chat. Not reading the rules is *not* an excuse for breaking them.
     • It's suggested that you read channel topics and pins before asking questions as well, as some questions may have already been answered in those.
    """,

    # 2
    """
    Be nice to each other. It's fine to disagree, it's not fine to insult or attack other people.
     • You may disagree with anyone or anything you like, but you should try to keep it to opinions, and not people. Avoid vitriol.
     • Constant antagonistic behavior is considered uncivil and appropriate action will be taken.
     • The use of derogatory slurs -- sexist, racist, homophobic, transphobic, or otherwise -- is unacceptable and may be grounds for an immediate ban.
    """,

    # 3
    'If you have concerns about another user, please take up your concerns with a staff member (someone with the "mod" role in the sidebar) in private. Don\'t publicly call other users out.',

    # 4
    """
    From time to time, we may mention everyone in the server. We do this when we feel something important is going on that requires attention. Complaining about these pings may result in a ban.
     • To disable notifications for these pings, suppress them in "ReSwitched → Notification Settings".
    """,

    # 5
    """
    Don't spam.
     • For excessively long text, use a service like <https://0bin.net/>.
    """,

    # 6
    "Don't brigade, raid, or otherwise attack other people or communities. Don't discuss participation in these attacks. This may warrant an immediate permanent ban.",

    # 7
    'Off-topic content goes to #off-topic. Keep low-quality content like memes out.',

    # 8
    'Trying to evade, look for loopholes, or stay borderline within the rules will be treated as breaking them.',

    # 9
    """
    Absolutely no piracy. Discussion of "backups" or other pirated materials is not permitted, even if you legally own a copy of the game. This is a zero-tolerance, non-negotiable policy, and will be enforced strictly and swiftly.'
     • Absolutely **NO** support will be provided for SX OS or other Team Xecuter ("TX") devices and software.
    """, 
    
    # 10
    'Installable homebrew NSPs are not supported here. If you are confused about how to set up homebrew properly (via hbl.nsp), it is fine to ask for assistance.',

    # 11
    'The first character of your server nickname should be alphanumeric if you wish to talk in chat.'
)

welcome_footer = (
    """
    :hash: __Channel Breakdown:__
    #news - Used exclusively for updates on ReSwitched progress and community information. Most major announcements are passed through this channel and whenever something is posted there it's usually something you'll want to look at.

    #switch-hacking-meta - For "meta-discussion" related to hacking the switch. This is where we talk *about* the switch hacking that's going on, and where you can get clarification about the hacks that exist and the work that's being done.

    #user-support - End-user focused support, mainly between users. Ask your questions about using switch homebrew here.

    #tool-support - Developer focused support. Ask your questions about using PegaSwitch, libtransistor, Mephisto, and other tools here.

    #hack-n-all - General hacking, hardware and software development channel for hacking on things *other* than the switch. This is a great place to ask about hacking other systems-- and for the community to have technical discussions.
    """,

    """
    #switch-hacking-general - Channel for everyone working on hacking the switch-- both in an exploit and a low-level hardware sense. This is where a lot of our in-the-open development goes on. Note that this isn't the place for developing homebrew-- we have #homebrew-development for that!

    #homebrew-development - Discussion about the development of homebrew goes there. Feel free to show off your latest creation here.

    #off-topic - Channel for discussion of anything that doesn't belong in #general. Anything goes, so long as you make sure to follow the rules and be on your best behavior.

    #toolchain-development - Discussion about the development of libtransistor itself goes there.

    #cfw-development - Development discussion regarding custom firmware (CFW) projects, such as Atmosphère. This channel is meant for the discussion accompanying active development.
    
    #bot-cmds - Channel for excessive/random use of Robocop's various commands.
    
    **If you are still not sure how to get access to the other channels, please read the rules again.**
    **If you have questions about the rules, feel free to ask here!**

    **Note: This channel is completely automated (aside from responding to questions about the rules). If your message didn't give you access to the other channels, you failed the test. Feel free to try again.**
    """,
)

hidden_term_line = ' • When you have finished reading all of the rules, send a message in this channel that includes the SHA1 hash of your discord "name#discriminator" (for example, User#1234), and we\'ll grant you access to the other channels. You can find your "name#discriminator" (your username followed by a ‘#’ and four numbers) under the discord channel list.'


class Verification:
    def __init__(self, bot):
        self.bot = bot

    @commands.check(check_if_staff)
    @commands.command()
    async def reset(self, ctx, limit: int = 100, force: bool = False):
        """Wipes messages and pastes the welcome message again. Staff only."""
        if ctx.message.channel.id != config.welcome_channel and not force:
            await ctx.send(f"This command is limited to"
                           f" <#{config.welcome_channel}>, unless forced.")
            return

        await ctx.channel.purge(limit=limit)

        await ctx.send(welcome_header)
        rules = ['**{}**. {}'.format(i, cleandoc(r)) for i, r in
                 enumerate(welcome_rules, 1)]
        rule_choice = random.randint(2, len(rules))
        rules[rule_choice - 1] += '\n' + hidden_term_line
        msg = f"🗑 **Reset**: {ctx.author.mention} cleared {limit} messages "\
              f" in {ctx.channel.mention}"
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
                current_message = "\n\u200B\n" + item + "\n\u200B\n"
                total = 0
        messages += [current_message]

        for item in messages:
            await ctx.send(item)
            await asyncio.sleep(1)

        for x in welcome_footer:
            await ctx.send(cleandoc(x))
            await asyncio.sleep(1)

    async def process_message(self, message):
        """Big code that makes me want to shoot myself
        Not really a rewrite but more of a port

        Git blame tells me that I should blame/credit Robin Lambertz"""
        if message.channel.id == config.welcome_channel:
            # Assign common stuff into variables to make stuff less of a mess
            member = message.author
            full_name = str(member)
            discrim = str(member.discriminator)
            guild = message.guild
            chan = message.channel
            mcl = message.content.lower()

            # Get the role we will give in case of success
            success_role = guild.get_role(config.participant_role)

            # Get a list of stuff we'll allow and will consider close
            allowed_names = [f"@{full_name}", full_name, str(member.id)]
            close_names = [f"@{member.name}", member.name, discrim,
                           f"#{discrim}"]
            # Now add the same things but with newlines at the end of them
            allowed_names += [(an + '\n') for an in allowed_names]
            close_names += [(cn + '\n') for cn in close_names]

            # Finally, hash the stuff so that we can access them later :)
            sha1_allow = [hashlib.sha1(name.encode('utf-8')).hexdigest()
                          for name in allowed_names]
            md5_allow = [hashlib.md5(name.encode('utf-8')).hexdigest()
                         for name in allowed_names]
            sha1_close = [hashlib.sha1(name.encode('utf-8')).hexdigest()
                          for name in close_names]

            # I'm not even going to attempt to break those into lines jfc
            if any(allow in mcl for allow in sha1_allow):
                await member.add_roles(success_role)
                await chan.purge(limit=100, check=lambda m: m.author == message.author or (m.author == self.bot.user and message.author.mention in m.content))
            elif any(close in mcl for close in sha1_close):
                await chan.send(f"{message.author.mention} :no_entry: Close, but incorrect. You got the process right, but you're not doing it on your name and discriminator properly. Please re-read the rules carefully and look up any terms you are not familiar with.")
            elif any(allow in mcl for allow in md5_allow):
                await chan.send(f"{message.author.mention} :no_entry: Close, but incorrect. You're processing your name and discriminator properly, but you're not using the right process. Please re-read the rules carefully and look up any terms you are not familiar with.")
            elif full_name in message.content or str(member.id) in message.content or member.name in message.content or discrim in message.content:
                await chan.send(f"{message.author.mention} :no_entry: Incorrect. You need to do something *specific* with your name and discriminator instead of just posting it. Please re-read the rules carefully and look up any terms you are not familiar with.")

    async def on_message(self, message):
        if message.author.bot:
            return

        try:
            await self.process_message(message)
        except discord.errors.Forbidden:
            chan = self.bot.get_channel(message.channel)
            await chan.send("💢 I don't have permission to do this.")

    async def on_message_edit(self, before, after):
        if message.author.bot:
            return

        try:
            await self.process_message(after)
        except discord.errors.Forbidden:
            chan = self.bot.get_channel(after.channel)
            await chan.send("💢 I don't have permission to do this.")

    # @commands.guild_only()
    # @commands.command()
    # async def verify(self, ctx, *, verification_string: str):
    #     """Does verification.

    #     See text on top of #verification for more info."""

    #     await ctx.message.delete()

    #     veriflogs_channel = ctx.guild.get_channel(config.veriflogs_chanid)
    #     verification_role = ctx.guild.get_role(config.read_rules_roleid)
    #     verification_wanted = config.verification_code\
    #         .replace("[discrim]", ctx.author.discriminator)

    #     # Do checks on if the user can even attempt to verify
    #     if ctx.channel.id != config.verification_chanid:
    #         resp = await ctx.send("This command can only be used "
    #                               f"on <#{config.verification_chanid}>.")
    #         await asyncio.sleep(config.sleep_secs)
    #         return await resp.delete()

    #     if verification_role in ctx.author.roles:
    #         resp = await ctx.send("This command can only by those without "
    #                               f"<@&{config.read_rules_roleid}> role.")
    #         await asyncio.sleep(config.sleep_secs)
    #         return await resp.delete()

    #     # Log verification attempt
    #     await self.bot.update_logs("Verification Attempt",
    #                                ctx.author.id,
    #                                veriflogs_channel,
    #                                log_text=verification_string,
    #                                digdepth=50, result=-1)

    #     # Check verification code
    #     if verification_string.lower().strip() == verification_wanted:
    #         resp = await ctx.send("Success! Welcome to the "
    #                               f"club, {str(ctx.author)}.")
    #         await self.bot.update_logs("Verification Attempt",
    #                                    ctx.author.id,
    #                                    veriflogs_channel,
    #                                    digdepth=50, result=0)
    #         await asyncio.sleep(config.sleep_secs)
    #         await ctx.author.add_roles(verification_role)
    #         await resp.delete()
    #     else:
    #         resp = await ctx.send(f"Incorrect password, {str(ctx.author)}.")
    #         await asyncio.sleep(config.sleep_secs)
    #         await resp.delete()


def setup(bot):
    bot.add_cog(Verification(bot))
