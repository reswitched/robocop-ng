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

        # Removing any chance of hex having to go to the awful guessing game we wil have to do soon
        elif err in switch_known_errcodes:
            err_description = switch_known_errcodes[err]
            err = err[2:]
            errcode = int(err, 16)
            module = errcode & 0x1FF
            desc = (errcode >> 9) & 0x3FFF

            if module in switch_modules:
                err_module = switch_modules[module]
            else:
                err_module = "Unknown"

            # Make a nice Embed out of it
            embed = discord.Embed(title="{} / {}".format(errcode, err), url="https://www.youtube.com/watch?v=x3yXlomPCmU", description=err_description)
            embed.set_footer(text="Console: Switch")
            embed.add_field(name="Module", value="{} ({})".format(err_module, module), inline=True)
            embed.add_field(name="Description", value=desc, inline=True)

            # Send message, crazy
            await ctx.send(embed=embed)

        elif self.switch_re.match(err): # Switch
            # Transforming into Hex
            module = int(err[0:4]) - 2000
            desc = int(err[5:9])
            errcode = (desc << 9) + module
            
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
            embed = discord.Embed(title="{} / {}".format(errcode, err), url="https://www.youtube.com/watch?v=x3yXlomPCmU", description=err_description)
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

        # The Guessing Game of Hex (Could be both 3DS or Switch so we have to constantly assume :P)
        elif err.startswith("0x"):
            err = err[2:] # Both work without the 0x
            # Most Switch Hex error should be detected by now so the chance that it's 3DS is much higher
            derr = err.strip()
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

            # Now lets just search for the last remaining switch errors to make sure
            errcode = int(err, 16)
            module = errcode & 0x1FF
            desc = (errcode >> 9) & 0x3FFF
            errcode = '{:04}-{:04}'.format(module + 2000, desc)

            # Searching for error codes related to the Switch (Doesn't include Special Cases)
            if errcode in switch_support_page:
                err_description = switch_support_page[errcode]
            elif module in switch_known_errcode_ranges:
                for errcode_range in switch_known_errcode_ranges[module]:
                    if desc >= errcode_range[0] and desc <= errcode_range[1]:
                        err_description = errcode_range[2]
            else:
                err_description = "It seems like your error code is unknown. You should report relevant details to <@141532589725974528> so it can be added to the bot."
            
            if module in switch_modules:
                err_module = switch_modules[module]
            else:
                err_module = "Unknown"

            # Make a nice Embed out of it
            embed = discord.Embed(title="{} / {}".format(errcode, err), url="https://www.youtube.com/watch?v=x3yXlomPCmU", description=err_description)
            embed.set_footer(text="Console: Switch")
            embed.add_field(name="Module", value="{} ({})".format(err_module, module), inline=True)
            embed.add_field(name="Description", value=desc, inline=True)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Unknown Format - This is either no error code or you made some mistake!")

def setup(bot):
    bot.add_cog(Err(bot))
