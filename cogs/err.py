import re
import discord

from discord.ext import commands
from data.errcodes import *

class Err:
    "Everything related to Nintendo 3DS, Wii U and Switch error codes"

    def __init__(self, bot):
        self.bot = bot
        self.dds_re = re.compile(r'0\d{2}\-\d{4}')
        self.wiiu_re = re.compile(r'1\d{2}\-\d{4}')
        self.switch_re = re.compile(r'2\d{3}\-\d{4}')
        print("Err has been loaded!")

    @commands.command(aliases=["nxerr", "serr", "nin_err"])
    async def err(self, ctx, err: str):
        """Searches for Nintendo 3DS, Switch and Wii U error codes!
            Usage: .serr/.nxerr/.nin_err/.err <Error Code>"""

        if self.dds_re.match(err): # 3DS - dds -> Drei DS -> Three DS
            if err in dds_errcodes:
                err_description = dds_errcodes[err]
            else:
                err_description = "It seems like your error code is unknown. You should report relevant details to <@141532589725974528> so it can be added to the bot."
            # Make a nice Embed out of it
            embed = discord.Embed(title=err, url="https://www.youtube.com/watch?v=x3yXlomPCmU", description=err_description)
            embed.set_footer(text="Console: 3DS")

            # Send message, crazy
            await ctx.send(embed=embed)

        elif err.startswith("0x"): # These are not similar to the other errors apperently ... ?
            derr = err[2:]
            derr = derr.strip()
            rc = int(derr, 16)
            desc = rc & 0x3FF
            mod = (rc >> 10) & 0xFF
            summ = (rc >> 21) & 0x3F
            level = (rc >> 27) & 0x1F
            if mod in dds_modules and summ in dds_summaries and desc in dds_descriptions and level in dds_levels:
                # ^ Lets just make extra sure that everything is right :P
                embed = discord.Embed(title="0x{:X}".format(rc))
                embed.add_field(name="Module", value=dds_modules[mod], inline=False)
                embed.add_field(name="Description", value=dds_descriptions[desc], inline=False)
                embed.add_field(name="Summary", value=dds_summaries[summ], inline=False)
                embed.add_field(name="Level", value=dds_levels[level], inline=False)
                embed.set_footer(text="Console: 3DS")

                await ctx.send(embed=embed)
                return

        elif self.wiiu_re.match(err): # Wii U
            module = err[2:3] # Is that even true, idk just guessing
            desc = err[5:8]
            if err in wii_u_errors:
                err_description = wii_u_errors[err]
            else:
                err_description = "It seems like your error code is unknown. You should report relevant details to <@141532589725974528> so it can be added to the bot."

            # Make a nice Embed out of it
            embed = discord.Embed(title=err, url="https://www.youtube.com/watch?v=x3yXlomPCmU", description=err_description)
            embed.set_footer(text="Console: Wii U")
            embed.add_field(name="Module", value=module, inline=True)
            embed.add_field(name="Description", value=desc, inline=True)

            # Send message, crazy
            await ctx.send(embed=embed)            

        if self.switch_re.match(err) or err.startswith("0x"): # Switch
            
            if err.startswith("0x"):
                err = err[2:]
                errcode = int(err, 16)
                module = errcode & 0x1FF
                desc = (errcode >> 9) & 0x3FFF
            else:
                module = int(err[0:4]) - 2000
                desc = int(err[5:9])
                errcode = (desc << 9) + module
            
            str_errcode = '{:04}-{:04}'.format(module + 2000, desc)

            # Searching for Modules in list
            if module in switch_modules:
                err_module = switch_modules[module]
            else:
                err_module = "Unknown"

            # Searching for error codes related to the Switch (Doesn't include Special Cases)
            if errcode in switch_known_errcodes:
                err_description = switch_known_errcodes[errcode]
            elif errcode in switch_support_page:
                err_description = switch_support_page[errcode]
            elif module in switch_known_errcode_ranges:
                for errcode_range in switch_known_errcode_ranges[module]:
                    if desc >= errcode_range[0] and desc <= errcode_range[1]:
                        err_description = errcode_range[2]
            else:
                err_description = "It seems like your error code is unknown. You should report relevant details to <@141532589725974528> so it can be added to the bot."

            # Make a nice Embed out of it
            embed = discord.Embed(title="{} / {}".format(str_errcode, hex(errcode)), url="https://www.youtube.com/watch?v=x3yXlomPCmU", description=err_description)
            embed.set_footer(text="Console: Switch")
            embed.add_field(name="Module", value="{} ({})".format(err_module, module), inline=True)
            embed.add_field(name="Description", value=desc, inline=True)

            # Send message, crazy
            await ctx.send(embed=embed)

        elif err in switch_game_err: # Special Case Handling because Nintendo feels like its required to break their format lol
            game,desc = switch_game_err[err].split(":")

            embed = discord.Embed(title=err, url="https://www.youtube.com/watch?v=x3yXlomPCmU", description=desc)
            embed.set_footer(text="Console: Switch")
            embed.add_field(name="Game", value=game, inline=True)

            await ctx.send(embed=embed)

        else:
            await ctx.send("Unknown Format - This is either no error code or you made some mistake!")

    @commands.command(aliases=["e2h"])
    async def err2hex(self, ctx, err: str):
        """Converts Nintendo Switch errors to hex
            Usage: .err2hex <Error Code>"""
        if self.switch_re.match(err):
            module = int(err[0:4]) - 2000
            desc = int(err[5:9])
            errcode = (desc << 9) + module
            await ctx.send(hex(errcode))
        else:
            await ctx.send("This doesn't follow the typical Nintendo Switch 2XXX-XXXX format!")
    
    @commands.command(aliases=["h2e"])
    async def hex2err(self, ctx, err: str):
        """Converts Nintendo Switch errors to hex
            Usage: .hex2err <Hex>"""
        if err.startswith("0x"):
            err = err[2:]
            err = int(err, 16)
            module = err & 0x1FF
            desc = (err >> 9) & 0x3FFF
            errcode = '{:04}-{:04}'.format(module + 2000, desc)
            await ctx.send(errcode) 
        else:
            await ctx.send("This doesn't look like typical hex!")  


def setup(bot):
    bot.add_cog(Err(bot))
