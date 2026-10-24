from discord.ext import commands


def get_jump(ctx):
    """Returns the modlog jump-link line for prefix invocations.

    Slash invocations have no triggering message, so this returns an empty
    string and the jump line is simply omitted.
    """
    if ctx.interaction is not None or ctx.message is None:
        return ""
    return f"\n🔗 __Jump__: <{ctx.message.jump_url}>"


async def get_reason_line(ctx, reason):
    if not reason:
        return ""
    safe_reason = await commands.clean_content(escape_markdown=True).convert(
        ctx, reason
    )
    return f'\n✏️ Reason: "{safe_reason}"'
