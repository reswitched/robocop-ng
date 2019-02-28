import config
import pprint
from discord.enums import MessageType

class Pin:
    """
    Allow users to pin things
    """
    def __init__(self, bot):
        self.bot = bot

    # Use raw_reaction to allow pinning old messages.
    async def on_raw_reaction_add(self, payload):
        # TODO: handle more than 50 pinned message
        # BODY: If there are more than 50 pinned messages,
        # BODY: we should move the oldest pin to a pinboard
        # BODY: channel to make room for the new pin.
        # BODY: This is why we use the pin reaction to remember
        # BODY: that a message is pinned.

        # Check that the user wants to pin this message
        if payload.emoji.name not in ["📌", "📍"]:
            return

        # Check that reaction pinning is allowd in this channel
        if payload.channel_id not in config.allowed_pin_channels:
            return

        target_guild = self.bot.get_guild(payload.guild_id)
        if target_guild is None:
            return

        # Check that the user is allowed to reaction-pin
        target_user = target_guild.get_member(payload.user_id)
        for role in config.staff_role_ids + config.allowed_pin_roles:
            if role in [role.id for role in target_user.roles]:
                target_chan = self.bot.get_channel(payload.channel_id)
                target_msg = await target_chan.get_message(payload.message_id)

                # Check that the message hasn't already been pinned
                for reaction in target_msg.reactions:
                    if reaction.emoji == "📌":
                        if reaction.me:
                            return
                        break

                # Wait for the automated "Pinned" message so we can delete it
                waitable = self.bot.wait_for('message', check=check)

                # Pin the message
                await target_msg.pin()

                # Delete the automated Pinned message
                msg = await waitable
                await msg.delete()

                # Add a Pin reaction so we remember that the message is pinned
                await target_msg.add_reaction("📌")

                # Send custom pinned message
                await target_chan.send("Pinned!")

def check(msg):
    return msg.type is MessageType.pins_add


def setup(bot):
    bot.add_cog(Pin(bot))
