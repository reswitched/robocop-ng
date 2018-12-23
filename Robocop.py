import os
import sys
import logging
import logging.handlers
import traceback
import configparser
from pathlib import Path
import aiohttp

import discord
from discord.ext import commands

script_name = os.path.basename(__file__).split('.')[0]

log_file_name = f"{script_name}.log"

# Limit of discord (non-nitro) is 8MB (not MiB)
max_file_size = 1000 * 1000 * 8
backup_count = 10000  # random big number
file_handler = logging.handlers.RotatingFileHandler(
    filename=log_file_name, maxBytes=max_file_size, backupCount=backup_count)
stdout_handler = logging.StreamHandler(sys.stdout)

log_format = logging.Formatter(
    '[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s')
file_handler.setFormatter(log_format)
stdout_handler.setFormatter(log_format)

log = logging.getLogger('discord')
log.setLevel(logging.INFO)
log.addHandler(file_handler)
log.addHandler(stdout_handler)

config = configparser.ConfigParser()
config.read(f"{script_name}.ini")


def get_prefix(bot, message):
    prefixes = [config['base']['prefix']]

    return commands.when_mentioned_or(*prefixes)(bot, message)


initial_extensions = ['cogs.common',
                      'cogs.admin',
                      'cogs.basic']

bot = commands.Bot(command_prefix=get_prefix,
                   description=config['base']['description'], pm_help=None)

bot.log = log
bot.config = config
bot.script_name = script_name

if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            log.error(f'Failed to load extension {extension}.', file=sys.stderr)
            log.error(traceback.print_exc())


@bot.event
async def on_ready():
    aioh = {"User-Agent": f"{script_name}/1.0'"}
    bot.aiosession = aiohttp.ClientSession(headers=aioh)
    bot.app_info = await bot.application_info()

    log.info(f'\nLogged in as: {bot.user.name} - '
             f'{bot.user.id}\ndpy version: {discord.__version__}\n')
    game_name = f"{config['base']['prefix']}help"
    await bot.change_presence(activity=discord.Game(name=game_name))


@bot.event
async def on_command(ctx):
    log_text = f"{ctx.message.author} ({ctx.message.author.id}): "\
               f"\"{ctx.message.content}\" "
    if ctx.guild:  # was too long for tertiary if
        log_text += f"on \"{ctx.channel.name}\" ({ctx.channel.id}) "\
                    f"at \"{ctx.guild.name}\" ({ctx.guild.id})"
    else:
        log_text += f"on DMs ({ctx.channel.id})"
    log.info(log_text)


@bot.event
async def on_error(event_method, *args, **kwargs):
    log.error(f"Error on {event_method}: {sys.exc_info()}")


@bot.event
async def on_command_error(ctx, error):
    log.error(f"Error with \"{ctx.message.content}\" from "
              f"\"{ctx.message.author}\ ({ctx.message.author.id}) "
              f"of type {type(error)}: {error}")

    if isinstance(error, commands.NoPrivateMessage):
        return await ctx.send("This command doesn't work on DMs.")
    elif isinstance(error, commands.MissingPermissions):
        roles_needed = '\n- '.join(error.missing_perms)
        return await ctx.send(f"{ctx.author.mention}: You don't have the right"
                              " permissions to run this command. You need: "
                              f"```- {roles_needed}```")
    elif isinstance(error, commands.BotMissingPermissions):
        roles_needed = '\n-'.join(error.missing_perms)
        return await ctx.send(f"{ctx.author.mention}: Bot doesn't have "
                              "the right permissions to run this command. "
                              "Please add the following roles: "
                              f"```- {roles_needed}```")
    elif isinstance(error, commands.CommandOnCooldown):
        return await ctx.send(f"{ctx.author.mention}: You're being "
                              "ratelimited. Try in "
                              f"{error.retry_after:.1f} seconds.")
    elif isinstance(error, commands.CheckFailure):
        return await ctx.send(f"{ctx.author.mention}: Check failed. "
                              "You might not have the right permissions "
                              "to run this command.")

    help_text = f"Usage of this command is: ```{ctx.prefix}"\
                f"{ctx.command.signature}```\nPlease see `{ctx.prefix}help "\
                f"{ctx.command.name}` for more info about this command."
    if isinstance(error, commands.BadArgument):
        return await ctx.send(f"{ctx.author.mention}: You gave incorrect "
                              f"arguments. {help_text}")
    elif isinstance(error, commands.MissingRequiredArgument):
        return await ctx.send(f"{ctx.author.mention}: You gave incomplete "
                              f"arguments. {help_text}")


@bot.event
async def on_guild_join(guild):
    bot.log.info(f"Joined guild \"{guild.name}\" ({guild.id}).")
    await guild.owner.send(f"Hello and welcome to {script_name}!\n"
                           "If you don't know why you're getting this message"
                           f", it's because someone added {script_name} to your"
                           " server\nDue to Discord API ToS, I am required to "
                           "inform you that **I log command usages and "
                           "errors**.\n**I don't log *anything* else**."
                           "\n\nIf you do not agree to be logged, stop"
                           f" using {script_name} and remove it from your "
                           "server as soon as possible.")


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    ctx = await bot.get_context(message)
    await bot.invoke(ctx)

if not Path(f"{script_name}.ini").is_file():
    log.warning(
        f"No config file ({script_name}.ini) found, "
        f"please create one from {script_name}.ini.example file.")
    exit(3)

bot.run(config['base']['token'], bot=True, reconnect=True)
