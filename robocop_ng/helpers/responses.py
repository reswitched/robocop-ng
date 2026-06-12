def get_jump(ctx):
    """Returns the modlog jump-link line for prefix invocations.

    Slash invocations have no triggering message, so this returns an empty
    string and the jump line is simply omitted.
    """
    if ctx.interaction is not None or ctx.message is None:
        return ""
    return f"\n🔗 __Jump__: <{ctx.message.jump_url}>"
