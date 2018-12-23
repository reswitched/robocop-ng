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

        if self.dds_re.match(err):
            err_console = "3DS"

        elif self.wiiu_re.match(err):
            err_console = "Wii U"

        elif self.switch_re.match(err):
            err_console = "Switch"
            module = int(err[0:4]) - 2000
            desc = int(err[5:9])
            errcode = (desc << 9) + module
            
            if module in switch_modules:
                err_module = switch_modules[module]
            else:
                err_module = "Unknown"

            if errcode in switch_known_errcodes:
                err_description = switch_known_errcodes[errcode]
            elif errcode in switch_support_page:
                err_description = switch_support_page[errcode]
            elif module in switch_known_errcode_ranges:
                for errcode_range in switch_known_errcode_ranges[module]:
                    if desc >= errcode_range[0] and desc <= errcode_range[1]:
                        err_description = errcode_range[2]
            
            embed = discord.Embed(title='0x{:X} / {}'.format(errcode, err), description="*Console:* {} \n *Module:* {} \n *Error Description:* {} \n".format(err_console, err_module, err_description))
            await ctx.send(embed=embed)

        elif err in switch_game_err: # Special Case Handling because Nintendo feels like its required to break their format lol
            game,desc = switch_game_err[err].split(":")
            await ctx.send(embed=discord.Embed(title=err, description="*Console:* {} \n *Game:* {} \n *Error Description:* {}".format(err_console, game, desc)))
            return

        elif err.startswith("0x"):
            pass # Ladies and Gentleman, this will be a guessing game ;)
            # 1 Switch 2 3DS / Wii U

        else:
            pass

def setup(bot):
    bot.add_cog(Err(bot))
