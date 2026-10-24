import discord


async def fetch_member_or_none(bot, guild, user_id):
    """Fetches a guild member by ID or returns None instead of erroring.

    When members priv intent is available, uses get_member (member cache, not a thing without events).
    When it is not, uses fetch_member, which goes to discord each time.
    """
    if bot.intents.members and guild.chunked:
        return guild.get_member(user_id)
    try:
        return await guild.fetch_member(user_id)
    except discord.NotFound:
        return None
