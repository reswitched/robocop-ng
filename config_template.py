import datetime

# Basic bot config
prefixes = [".", "!"]
token = "token-goes-here"
bot_description = "Robocop-NG, the moderation bot of ReSwitched."

source_url = "https://github.com/aveao/robocop-ng"
rules_url = "https://reswitched.team/discord/"

# The bot description to be used in .robocop embed
embed_desc = "Robocop-NG is developed by [Ave](https://github.com/aveao)"\
             " and [tomGER](https://github.com/tumGER), and is a rewrite "\
             "of Robocop.\nRobocop is based on Kurisu by 916253 and ihaveamac."


# Minimum account age required to join the discord
min_age = datetime.timedelta(minutes=15)

guild_whitelist = [
    526372255052201993,  # NotSwitched discord
    269333940928512010  # ReSwitched discord
]

# Named roles to be used with .approve and .revoke
# The defaults are for NotSwitched
named_roles = {
    "community": 526378381839695872,
    "hacker": 526471781184176139,
    "participant": 526378358129557506
}

bot_manager_role_id = 526372554081042462  # Bot management role in NotSwitched
staff_role_ids = [526384077679624192,  # Team role in NotSwitched
                  526372582455508992,  # Mod role in NotSwitched
                  526372554081042462,  # Bot management role in NotSwitched
                  526383985430102016]  # Wizard role in NotSwitched

log_channel = 526377735908491284  # Log channel in NotSwitched
botlog_channel = 529070401704296460  # Botlog channel in NotSwitched
welcome_channel = 526372470752673792  # rules-info channel in NotSwitched

community_channels = [526378423468425236]  # Channels requiring community role
general_channels = [526372255052201995]  # Channels everyone can access

mute_role = 526500080879140874  # Mute role in NotSwitched
