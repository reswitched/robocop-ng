import config


async def log_member_update(
    bot,
    member,
    roles_before,
    roles_after,
    nick_before=None,
    nick_after=None,
    member_before=None,
):
    """Posts a member update (roles, username, nickname) to the log channel."""
    if member.guild.id not in config.guild_whitelist:
        return

    msg = ""
    role_removal = [role for role in roles_before if role not in roles_after]
    role_addition = [role for role in roles_after if role not in roles_before]
    if role_addition or role_removal:
        msg += "\n👑 __Role change__: "
        roles = []
        for role in role_removal:
            roles.append("_~~" + role.name + "~~_")
        for role in role_addition:
            roles.append("__**" + role.name + "**__")
        for role in roles_after:
            if role.is_default():
                continue
            if role not in role_removal and role not in role_addition:
                roles.append(role.name)
        msg += ", ".join(roles)

    if member_before is not None and member_before.name != member.name:
        msg += (
            "\n📝 __Username change__: "
            f"{bot.escape_message(member_before)} → "
            f"{bot.escape_message(member)}"
        )
    if nick_before != nick_after:
        if not nick_before:
            msg += "\n🏷 __Nickname addition__"
        elif not nick_after:
            msg += "\n🏷 __Nickname removal__"
        else:
            msg += "\n🏷 __Nickname change__"
        msg += (
            f": {bot.escape_message(nick_before)} → "
            f"{bot.escape_message(nick_after)}"
        )

    if msg:
        msg = (
            f"ℹ️ **Member update**: {member.mention} | "
            f"{bot.escape_message(member)}{msg}"
        )
        log_channel = bot.get_channel(config.log_channel)
        await log_channel.send(msg)


_unchanged = object()


async def log_own_member_update(
    bot, member, add_roles=(), remove_roles=(), nick=_unchanged
):
    """Logs a member update the bot itself just made.

    We rely on on_member_update when members privileged intent is on.
    Without it, we don't get it, so this is for manual bot events to log
    their own actions.
    """
    if bot.intents.members:
        return

    roles_after = [role for role in member.roles if role not in remove_roles]
    roles_after += [role for role in add_roles if role not in roles_after]
    nick_after = member.nick if nick is _unchanged else nick
    await log_member_update(
        bot, member, member.roles, roles_after, member.nick, nick_after
    )
