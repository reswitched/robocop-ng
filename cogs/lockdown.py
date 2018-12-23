import discord
import asyncio
from discord.ext import commands
from config import modlog_channel, staff_role_ids, participant_role, community_channels, general_channels, hacker_role, community_role

class Lockdown:
    "Lockdown Commands"

    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(manage_messages=True)
    @commands.command(pass_context=True)
    async def lock(self, ctx):
        "Locks the channel"
        if ctx.message.channel in community_channels:
            roles = (hacker_role, community_role)
        else:
            roles = participant_role
        overwrites = ctx.message.channel.overwrites_for(roles[0])
        if overwrites.send_message == False:
            await ctx.send("The Channel is already locked!")
            return
        overwrites.send_message = False
        overwrites.add_reactions = False
        await asyncio.gather(*(self.bot.edit_channel_permissions(ctx.message.channel, role, overwrites) for role in roles))
        await ctx.send("🔒 Channel locked down. Only staff members may speak. Do not bring the topic to other channels or risk disciplinary actions.")
        ctx.send_message(modlog_channel, "Channel Lockdown for {channel} by {user}".format(ctx.message.channel.mention, ctx.message.author.mention))
        
def setup(bot):
    bot.add_cog(Lockdown(bot))