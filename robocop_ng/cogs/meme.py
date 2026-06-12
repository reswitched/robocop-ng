import random
import discord
from discord.ext import commands
from discord.ext.commands import Cog
import math
import platform
from helpers.checks import check_if_staff_or_ot
import datetime


class Meme(Cog):
    """
    Meme commands.
    """

    def __init__(self, bot):
        self.bot = bot

    def c_to_f(self, c):
        """this is where we take memes too far"""
        return math.floor(9.0 / 5.0 * c + 32)

    def c_to_k(self, c):
        """this is where we take memes REALLY far"""
        return math.floor(c + 273.15)

    @commands.check(check_if_staff_or_ot)
    @commands.hybrid_command(hidden=True, name="warm")
    async def warm_member(self, ctx, user: discord.Member):
        """Warms a user :3"""
        celsius = random.randint(15, 100)
        fahrenheit = self.c_to_f(celsius)
        kelvin = self.c_to_k(celsius)
        await ctx.send(
            f"{user.mention} warmed."
            f" User is now {celsius}°C "
            f"({fahrenheit}°F, {kelvin}K)."
        )

    @commands.check(check_if_staff_or_ot)
    @commands.hybrid_command(hidden=True, name="chill", aliases=["cold"])
    async def chill_member(self, ctx, user: discord.Member):
        """Chills a user >:3"""
        celsius = random.randint(-50, 15)
        fahrenheit = self.c_to_f(celsius)
        kelvin = self.c_to_k(celsius)
        await ctx.send(
            f"{user.mention} chilled."
            f" User is now {celsius}°C "
            f"({fahrenheit}°F, {kelvin}K)."
        )

    @commands.check(check_if_staff_or_ot)
    @commands.hybrid_command(hidden=True, aliases=["thank", "reswitchedgold"])
    async def gild(self, ctx, user: discord.Member):
        """Gives a star to a user"""
        await ctx.send(f"{user.mention} gets a :star:, yay!")

    @commands.check(check_if_staff_or_ot)
    @commands.hybrid_command(
        hidden=True, aliases=["reswitchedsilver", "silv3r", "reswitchedsilv3r"]
    )
    async def silver(self, ctx, user: discord.Member):
        """Gives a user ReSwitched Silver™"""
        embed = discord.Embed(
            title="ReSwitched Silver™!",
            description=f"Here's your ReSwitched Silver™," f"{user.mention}!",
        )
        embed.set_image(
            url="https://cdn.discordapp.com/emojis/548623626916724747.png?v=1"
        )
        await ctx.send(embed=embed)

    @commands.check(check_if_staff_or_ot)
    @commands.hybrid_command(hidden=True)
    async def btwiuse(self, ctx):
        """btw i use arch"""
        uname = platform.uname()
        await ctx.send(
            f"BTW I use {platform.python_implementation()} "
            f"{platform.python_version()} on {uname.system} "
            f"{uname.release}"
        )

    @commands.check(check_if_staff_or_ot)
    @commands.hybrid_command(hidden=True)
    async def yahaha(self, ctx):
        """secret command"""
        await ctx.send(f"🍂 you found me 🍂")

    @commands.check(check_if_staff_or_ot)
    @commands.hybrid_command(hidden=True)
    async def bones(self, ctx):
        """Posts the bones meme."""
        await ctx.send("https://cdn.discordapp.com/emojis/443501365843591169.png?v=1")

    @commands.check(check_if_staff_or_ot)
    @commands.hybrid_command(hidden=True)
    async def headpat(self, ctx):
        """Posts a headpat."""
        await ctx.send("https://cdn.discordapp.com/emojis/465650811909701642.png?v=1")

    @commands.check(check_if_staff_or_ot)
    @commands.hybrid_command(
        hidden=True, aliases=["when", "etawhen", "emunand", "emummc", "thermosphere"]
    )
    async def eta(self, ctx):
        """Responds to ETA questions."""
        await ctx.send("June 15.")

    @commands.check(check_if_staff_or_ot)
    @commands.hybrid_command(hidden=True, name="bam")
    async def bam_member(self, ctx, target: discord.Member):
        """Bams a user owo"""
        if target == ctx.author:
            if target.id == 181627658520625152:
                return await ctx.send(
                    "https://cdn.discordapp.com/attachments/286612533757083648/403080855402315796/rehedge.PNG"
                )
            return await ctx.send("hedgeberg#7337 is ̶n͢ow b̕&̡.̷ 👍̡")
        elif target == self.bot.user:
            return await ctx.send(
                f"I'm sorry {ctx.author.mention}, I'm afraid I can't do that."
            )

        safe_name = await commands.clean_content(escape_markdown=True).convert(
            ctx, str(target)
        )
        await ctx.send(f"{safe_name} is ̶n͢ow b̕&̡.̷ 👍̡")

    @commands.hybrid_command(
        hidden=True,
        aliases=[
            "yotld",
            "yold",
            "yoltd",
            "yearoflinuxondesktop",
            "yearoflinuxonthedesktop",
        ],
    )
    async def yearoflinux(self, ctx):
        """Shows the year of Linux on the desktop"""
        await ctx.send(
            f"{datetime.datetime.now().year} is the year of Linux on the Desktop"
        )


async def setup(bot):
    await bot.add_cog(Meme(bot))
