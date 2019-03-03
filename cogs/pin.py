import config
from discord.ext.commands import Cog
from discord.enums import MessageType
from discord import Embed
import aiohttp
import gidgethub.aiohttp
from helpers.checks import check_if_collaborator
from helpers.checks import check_if_pin_channel

class Pin(Cog):
    """
    Allow users to pin things
    """

    def __init__(self, bot):
        self.bot = bot

    async def get_pinboard(self, gh, channel):
        # Find pinboard pin
        pinboard_msg = None
        for msg in reversed(await channel.pins()):
            if msg.author == self.bot.user and len(msg.embeds) > 0 and msg.embeds[0].title == "Pinboard":
                # Found pinboard, return content and gist id
                id = msg.embeds[0].url.split("/")[-1]
                data = await gh.getitem(f"/gists/{id}")
                return (id, data["files"]["pinboard.md"]["content"])

        # Create pinboard pin if it does not exist
        data = await gh.post("/gists", data={"files": {"pinboard.md": {"content": "Old pins are available here:\n\n"}}, "description": f"Pinboard for SwitchRoot #{channel.name}", "public": True})
        msg = await channel.send(embed=Embed(title="Pinboard", description="Old pins are moved to the pinboard to make space for new ones. Check it out!", url=data["html_url"]))
        await msg.pin()
        return (data["id"], data["files"]["pinboard.md"]["content"])

    async def add_pin_to_pinboard(self, channel, data):
        if config.github_oauth_token == "":
            # Don't add to gist pinboard if we don't have an oauth token
            return

        async with aiohttp.ClientSession() as session:
            gh = gidgethub.aiohttp.GitHubAPI(session, "RoboCop-NG", oauth_token=config.github_oauth_token)
            (id, content) = await self.get_pinboard(gh, channel)
            content += "- " + data + "\n"

            await gh.patch(f"/gists/{id}", data={"files": {"pinboard.md": {"content": content}}})

    # Use raw_reaction to allow pinning old messages.
    @Cog.listener()
    async def on_raw_reaction_add(self, payload):
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
                        else:
                            break

                # Add pin to pinboard, create one if none is found
                await self.add_pin_to_pinboard(target_chan, target_msg.jump_url)

                # Avoid staying "stuck" waiting for the pin message if message
                # was already manually pinned
                if not target_msg.pinned:
                    # Wait for the automated "Pinned" message so we can delete it
                    waitable = self.bot.wait_for('message', check=check)

                    # Pin the message
                    await target_msg.pin()

                    # Delete the automated Pinned message
                    msg = await waitable
                    await msg.delete()

                # Add a Pin reaction so we remember that the message is pinned
                await target_msg.add_reaction("📌")


def check(msg):
    return msg.type is MessageType.pins_add


def setup(bot):
    bot.add_cog(Pin(bot))
