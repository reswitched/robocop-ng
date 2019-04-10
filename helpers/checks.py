import config


def check_if_staff(ctx):
    if not ctx.guild:
        return False
    return any(r.id in config.staff_role_ids for r in ctx.author.roles)


def check_if_bot_manager(ctx):
    if not ctx.guild:
        return False
    return any(r.id == config.bot_manager_role_id for r in ctx.author.roles)


def check_if_staff_or_ot(ctx):
    return True