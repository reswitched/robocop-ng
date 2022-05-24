import config
import time
import discord
import traceback
from discord.ext import commands, tasks
from discord.ext.commands import Cog
from helpers.robocronp import get_crontab, delete_job
from helpers.restrictions import remove_restriction
from helpers.checks import check_if_staff


class Robocronp(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.minutely.start()
        self.hourly.start()
        self.daily.start()

    def cog_unload(self):
        self.minutely.cancel()
        self.hourly.cancel()
        self.daily.cancel()

    async def send_data(self):
        data_files = [discord.File(fpath) for fpath in self.bot.wanted_jsons]
        log_channel = self.bot.get_channel(config.botlog_channel)
        await log_channel.send("Hourly data backups:", files=data_files)

    @commands.guild_only()
    @commands.check(check_if_staff)
    @commands.command()
    async def listjobs(self, ctx):
        """Lists timed robocronp jobs, staff only."""
        ctab = get_crontab()
        embed = discord.Embed(title=f"Active robocronp jobs")
        for jobtype in ctab:
            for jobtimestamp in ctab[jobtype]:
                for job_name in ctab[jobtype][jobtimestamp]:
                    job_details = repr(ctab[jobtype][jobtimestamp][job_name])
                    embed.add_field(
                        name=f"{jobtype} for {job_name}",
                        value=f"Timestamp: {jobtimestamp}, Details: {job_details}",
                        inline=False,
                    )
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.check(check_if_staff)
    @commands.command(aliases=["removejob"])
    async def deletejob(self, ctx, timestamp: str, job_type: str, job_name: str):
        """Removes a timed robocronp job, staff only.

        You'll need to supply:
        - timestamp (like 1545981602)
        - job type (like "unban")
        - job name (userid, like 420332322307571713)

        You can get all 3 from listjobs command."""
        delete_job(timestamp, job_type, job_name)
        await ctx.send(f"{ctx.author.mention}: Deleted!")

    async def do_jobs(self, ctab, jobtype, timestamp):
        log_channel = self.bot.get_channel(config.botlog_channel)
        for job_name in ctab[jobtype][timestamp]:
            try:
                job_details = ctab[jobtype][timestamp][job_name]
                if jobtype == "unban":
                    target_user = await self.bot.fetch_user(job_name)
                    target_guild = self.bot.get_guild(job_details["guild"])
                    delete_job(timestamp, jobtype, job_name)
                    await target_guild.unban(
                        target_user, reason="Robocronp: Timed ban expired."
                    )
                elif jobtype == "unmute":
                    remove_restriction(job_name, config.mute_role)
                    target_guild = self.bot.get_guild(job_details["guild"])
                    target_member = target_guild.get_member(int(job_name))
                    target_role = target_guild.get_role(config.mute_role)
                    await target_member.remove_roles(
                        target_role, reason="Robocronp: Timed mute expired."
                    )
                    delete_job(timestamp, jobtype, job_name)
                elif jobtype == "remind":
                    text = job_details["text"]
                    added_on = job_details["added"]
                    target = await self.bot.fetch_user(int(job_name))
                    if target:
                        await target.send(
                            f"You asked to be reminded about `{text}` on {added_on}."
                        )
                    delete_job(timestamp, jobtype, job_name)
            except:
                # Don't kill cronjobs if something goes wrong.
                delete_job(timestamp, jobtype, job_name)
                await log_channel.send(
                    "Crondo has errored, job deleted: ```"
                    f"{traceback.format_exc()}```"
                )

    async def clean_channel(self, channel_id):
        log_channel = self.bot.get_channel(config.botlog_channel)
        channel = self.bot.get_channel(channel_id)
        try:
            done_cleaning = False
            count = 0
            while not done_cleaning:
                purge_res = await channel.purge(limit=100)
                count += len(purge_res)
                if len(purge_res) != 100:
                    done_cleaning = True
            await log_channel.send(
                f"Wiped {count} messages from <#{channel.id}> automatically."
            )
        except:
            # Don't kill cronjobs if something goes wrong.
            await log_channel.send(
                f"Cronclean has errored: ```{traceback.format_exc()}```"
            )

    @tasks.loop(minutes=1)
    async def minutely(self):
        await self.bot.wait_until_ready()
        log_channel = self.bot.get_channel(config.botlog_channel)
        try:
            ctab = get_crontab()
            timestamp = time.time()
            for jobtype in ctab:
                for jobtimestamp in ctab[jobtype]:
                    if timestamp > int(jobtimestamp):
                        await self.do_jobs(ctab, jobtype, jobtimestamp)

            # Handle clean channels
            for clean_channel in config.minutely_clean_channels:
                await self.clean_channel(clean_channel)
        except:
            # Don't kill cronjobs if something goes wrong.
            await log_channel.send(
                f"Cron-minutely has errored: ```{traceback.format_exc()}```"
            )

    @tasks.loop(hours=1)
    async def hourly(self):
        await self.bot.wait_until_ready()
        log_channel = self.bot.get_channel(config.botlog_channel)
        try:
            await self.send_data()
            # Handle clean channels
            for clean_channel in config.hourly_clean_channels:
                await self.clean_channel(clean_channel)
        except:
            # Don't kill cronjobs if something goes wrong.
            await log_channel.send(
                f"Cron-hourly has errored: ```{traceback.format_exc()}```"
            )

    @tasks.loop(hours=24)
    async def daily(self):
        await self.bot.wait_until_ready()
        log_channel = self.bot.get_channel(config.botlog_channel)
        try:
            # Reset verification and algorithm
            if "cogs.verification" in config.initial_cogs:
                verif_channel = self.bot.get_channel(config.welcome_channel)
                await self.bot.do_resetalgo(verif_channel, "daily robocronp")
        except:
            # Don't kill cronjobs if something goes wrong.
            await log_channel.send(
                f"Cron-daily has errored: ```{traceback.format_exc()}```"
            )


async def setup(bot):
    await bot.add_cog(Robocronp(bot))
