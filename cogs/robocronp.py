import asyncio
import config
import time
import discord
from discord.ext import commands
from helpers.robocronp import get_crontab, delete_job
from helpers.restrictions import remove_restriction
from helpers.checks import check_if_staff


class Robocronp:
    def __init__(self, bot):
        self.bot = bot
        bot.loop.create_task(self.minutely())
        bot.loop.create_task(self.hourly())

    async def send_data(self):
        data_files = [discord.File(fpath) for fpath in self.bot.wanted_jsons]
        log_channel = self.bot.get_channel(config.log_channel)
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
                    embed.add_field(name=f"{jobtype} for {job_name}",
                                    value=f"Timestamp: {jobtimestamp}, "
                                    f"Details: {job_details}",
                                    inline=False)
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.check(check_if_staff)
    @commands.command(aliases=["removejob"])
    async def deletejob(self, ctx, timestamp: str,
                        job_type: str, job_name: str):
        """Removes a timed robocronp job, staff only.

        You'll need to supply:
        - timestamp (like 1545981602)
        - job type (like "unban")
        - job name (userid, like 420332322307571713)

        You can get all 3 from listjobs command."""
        delete_job(timestamp, job_type, job_name)
        await ctx.send(f"{ctx.author.mention}: Deleted!")

    async def do_jobs(self, ctab, jobtype, timestamp):
        for job_name in ctab[jobtype][timestamp]:
            job_details = ctab[jobtype][timestamp][job_name]
            if jobtype == "unban":
                target_user = await self.bot.get_user_info(job_name)
                target_guild = self.bot.get_guild(job_details["guild"])
                await target_guild.unban(target_user,
                                         reason="Robocronp: Timed ban expired.")
                delete_job(timestamp, jobtype, job_name)
            elif jobtype == "unmute":
                remove_restriction(job_name, config.mute_role)
                target_guild = self.bot.get_guild(job_details["guild"])
                target_member = target_guild.get_member(int(job_name))
                target_role = target_guild.get_role(config.mute_role)
                await target_member.remove_roles(target_role,
                                                 reason="Robocronp: Timed "
                                                        "mute expired.")
                delete_job(timestamp, jobtype, job_name)

    async def minutely(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            try:
                ctab = get_crontab()
                timestamp = time.time()
                for jobtype in ctab:
                    for jobtimestamp in ctab[jobtype]:
                        if timestamp > int(jobtimestamp):
                            await self.do_jobs(ctab, jobtype, jobtimestamp)
            except:
                # Don't kill cronjobs if something goes wrong.
                pass
            await asyncio.sleep(60)

    async def hourly(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            # Your stuff that should run at boot
            # and after that every hour goes here
            await asyncio.sleep(3600)
            try:
                await self.send_data()
            except:
                # Don't kill cronjobs if something goes wrong.
                pass
            # Your stuff that should run an hour after boot
            # and after that every hour goes here


def setup(bot):
    bot.add_cog(Robocronp(bot))
