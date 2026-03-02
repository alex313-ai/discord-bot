import discord
import os
from discord.ext import commands

TOKEN = "MTQ3NzI3MDk1NzIwMTY4NjU4OQ.GtaFGM.8QThxLz7w_GGKkU6yRLsA1RpDnIpjWwDEzdTHo"

intents = discord.Intents.default()
intents.message_content = True  # Needed to read messages
intents.members = True  # Needed to read members and their roles

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print("Bot is ready!")

@bot.command()
async def check(ctx, message_id: int):
    """Checks reactions on a message and pings members with @Blue Youth who didn't react."""
    try:
        message = await ctx.channel.fetch_message(message_id)
    except discord.NotFound:
        await ctx.send("Message not found.")
        return
    except discord.Forbidden:
        await ctx.send("I don't have permission to read that message.")
        return
    except discord.HTTPException:
        await ctx.send("Something went wrong while fetching the message.")
        return

    # Get all users who reacted
    reacted_users = set()
    for reaction in message.reactions:
        async for user in reaction.users():
            if not user.bot:
                reacted_users.add(user)

    # Get all members with the role "Blue Youth"
    role = discord.utils.get(ctx.guild.roles, name="Blue Youth")
    if role is None:
        await ctx.send("Role @Blue Youth does not exist on this server!")
        return

    members_with_role = [member for member in ctx.guild.members if role in member.roles]

    # List those who haven't reacted
    not_reacted = [member for member in members_with_role if member not in reacted_users]

    if not not_reacted:
        await ctx.send("All members with @Blue Youth have reacted ✅")
    else:
        mentions = " ".join(member.mention for member in not_reacted)
        await ctx.send(f"The following @Blue Youth members have not reacted:\n{mentions}")

bot.run(os.getenv("MTQ3NzI3MDk1NzIwMTY4NjU4OQ.GtaFGM.8QThxLz7w_GGKkU6yRLsA1RpDnIpjWwDEzdTHo"))
