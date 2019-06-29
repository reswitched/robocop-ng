import datetime

# Basic bot config, insert your token here, update description if you want
prefixes = [".", "!"]
token = "token-goes-here"
bot_description = "Robocop-NG, the moderation bot of ReSwitched."

# If you forked robocop-ng, put your repo here
source_url = "https://github.com/reswitched/robocop-ng"
rules_url = "https://reswitched.team/discord/#rules"

# The bot description to be used in .robocop embed
embed_desc = "Robocop-NG is developed by [Ave](https://github.com/aveao)"\
             " and [tomGER](https://github.com/tumGER), and is a rewrite "\
             "of Robocop.\nRobocop is based on Kurisu by 916253 and ihaveamac."


# Minimum account age required to join the guild
# If user's account creation is shorter than the time delta given here
# then user will be kicked and informed
min_age = datetime.timedelta(minutes=15)

# The bot will only work in these guilds
guild_whitelist = [
    269333940928512010  # ReSwitched discord
]

# Role that gets chosen by default by .approve and .revoke if none was specified
default_named_role = "community"

# Named roles to be used with .approve and .revoke
# Example: .approve User hacker
named_roles = {
    "community": 420010997877833731,
    "hacker": 364508795038072833,
    "participant": 434353085926866946
}

# The bot manager and staff roles
# Bot manager can run eval, exit and other destructive commands
# Staff can run administrative commands
bot_manager_role_id = 466447265863696394  # Bot management role in ReSwitched
staff_role_ids = [364647829248933888,  # Team role in ReSwitched
                  360138431524765707,  # Mod role in ReSwitched
                  466447265863696394,  # Bot management role in ReSwitched
                  360138163156549632,  # Admin role in ReSwitched
                  287289529986187266]  # Wizard role in ReSwitched

kek_role_ids = [578239919542239243,  # Kekdad role in AtlasNX
                574670558910742531,  # Kekmon role in AtlasNX
                594592298763943977]  # Kekreport role in AtlasNX

# Various log channels used to log bot and guild's activity
# You can use same channel for multiple log types
# Spylog channel logs suspicious messages or messages by members under watch
# Invites created with .invite will direct to the welcome channel.
log_channel = 290958160414375946  # server-logs in ReSwitched
botlog_channel = 529070282409771048  # bot-logs channel in ReSwitched
modlog_channel = 542114169244221452  # mod-logs channel in ReSwitched
spylog_channel = 548304839294189579  # spy channel in ReSwitched
welcome_channel = 326416669058662401  # newcomers channel in ReSwitched

# These channel entries are used to determine which roles will be given
# access when we unmute on them
general_channels = [420029476634886144,
                    414949821003202562,
                    383368936466546698,
                    343244421044633602,
                    491316901692178432,
                    539212260350885908]  # Channels everyone can access
community_channels = [269333940928512010,
                      438839875970662400,
                      404722395845361668,
                      435687501068501002,
                      286612533757083648]  # Channels requiring community role

# Controls which roles are blocked during lockdown
lockdown_configs = {
    # Used as a default value for channels without a config
    "default": {
        "channels": general_channels,
        "roles": [named_roles["participant"]]
    },
    "community": {
        "channels": community_channels,
        "roles": [named_roles["community"], named_roles["hacker"]]
    }
}

# Mute role is applied to users when they're muted
# As we no longer have mute role on ReSwitched, I set it to 0 here
mute_role = 0  # Mute role in ReSwitched

# Channels that will be cleaned every minute/hour
minutely_clean_channels = []
hourly_clean_channels = []

# Edited and deletes messages in these channels will be logged
spy_channels = general_channels

# Channels and roles where users can pin messages
allowed_pin_channels = []
allowed_pin_roles = []

# Used for the pinboard. Leave empty if you don't wish for a gist pinboard.
github_oauth_token = ""
