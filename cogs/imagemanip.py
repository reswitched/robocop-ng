import discord
from discord.ext import commands
from discord.ext.commands import Cog
from helpers.checks import check_if_staff_or_ot
import textwrap
import PIL.Image
import PIL.ImageFilter
import PIL.ImageOps
import PIL.ImageFont
import PIL.ImageDraw


class ImageManip(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.check(check_if_staff_or_ot)
    @commands.command(hidden=True)
    async def cox(self, ctx, *, headline: str):
        """Gives a cox headline"""
        mention = ctx.author.mention

        in_vice = "assets/motherboardlogo.png"
        in_byjcox = "assets/byjcox.png"
        font_path = "assets/neue-haas-grotesk-display-bold-regular.otf"

        # Settings for image generation, don't touch anything
        horipos = 18
        vertpos = 75
        line_spacing = 10
        font_size = 50
        image_width = 750
        font_wrap_count = 30
        sig_height = 15

        # Wrap into lines
        lines = textwrap.wrap(headline, width=font_wrap_count)
        # not great, 4am be like
        image_height = (len(lines) + 2) * (vertpos + line_spacing)

        # Load font
        f = PIL.ImageFont.truetype(font_path, font_size)

        # Create image base, paste mobo logo
        im = PIL.Image.new("RGB", (image_width, image_height), color="#FFFFFF")
        moboim = PIL.Image.open(in_vice)
        im.paste(moboim, (horipos, 17))

        # Go through all the wrapped text lines
        for line in lines:
            # Get size of the text by font, create a new image of that size
            size = f.getsize(line)
            txt = PIL.Image.new('L', size)

            # Draw the text
            d = PIL.ImageDraw.Draw(txt)
            d.text((0, 0), line, font=f, fill=255)

            # Paste the text into the base image
            w = txt.rotate(0, expand=1)
            im.paste(PIL.ImageOps.colorize(w, (0, 0, 0),
                                           (0, 0, 0)), (horipos, vertpos), w)

            # Calculate position on next line
            vertpos += size[1] + line_spacing

        # Add jcox signature
        jcoxim = PIL.Image.open(in_byjcox)
        im.paste(jcoxim, (horipos, vertpos + sig_height))

        # Crop the image to the actual resulting size
        im = im.crop((0, 0, image_width, vertpos + (sig_height * 3)))

        # Save image
        out_filename = f"/tmp/{ctx.message.id}-out.png"
        im.save(out_filename, quality=100, optimize=True)
        await ctx.send(content=f"{mention}: Enjoy.",
                       file=discord.File(out_filename))

    @commands.check(check_if_staff_or_ot)
    @commands.command(hidden=True)
    async def trump(self, ctx, *, headline: str):
        """Gives a trump tweet"""
        mention = ctx.author.mention

        in_header = "assets/trumpheader.png"
        in_footer = "assets/trumpfooter.png"
        font_path = "assets/Segoe UI.ttf"

        # Settings for image generation, don't touch anything
        horipos = 10
        vertpos = 70
        font_size = 27
        image_width = 590
        font_wrap_count = 45
        sig_height = 49

        # Wrap into lines
        lines = textwrap.wrap(headline, width=font_wrap_count)
        # not great, 4am be like
        image_height = (len(lines) + 2) * vertpos

        # Load font
        f = PIL.ImageFont.truetype(font_path, font_size)

        # Create image base, paste mobo logo
        im = PIL.Image.new("RGB", (image_width, image_height), color="#15202B")
        headerim = PIL.Image.open(in_header)
        im.paste(headerim, (horipos, 15))

        # Go through all the wrapped text lines
        for line in lines:
            # Get size of the text by font, create a new image of that size
            size = f.getsize(line)
            txt = PIL.Image.new('L', size)

            # Draw the text
            d = PIL.ImageDraw.Draw(txt)
            d.text((0, 0), line, font=f, fill=255)

            # Paste the text into the base image
            w = txt.rotate(0, expand=1)
            im.paste(PIL.ImageOps.colorize(w, (0, 0, 0),
                                           (255, 255, 255)), (horipos, vertpos),
                     w)

            # Calculate position on next line
            vertpos += size[1]

        # Add jcox signature
        jcoxim = PIL.Image.open(in_footer)
        im.paste(jcoxim, (horipos, vertpos + int(sig_height / 3)))

        # Crop the image to the actual resulting size
        im = im.crop((0, 0, image_width, vertpos + int(sig_height * 2.5)))

        # Save image
        out_filename = f"/tmp/{ctx.message.id}-out.png"
        im.save(out_filename, quality=100, optimize=True)
        await ctx.send(content=f"{mention}: Enjoy.",
                       file=discord.File(out_filename))


def setup(bot):
    bot.add_cog(ImageManip(bot))
