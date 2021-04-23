import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

client = commands.Bot(command_prefix="atta ")
token = os.getenv("DISCORD_BOT_TOKEN")

@client.event
async def on_ready() :
    await client.change_presence(status = discord.Status.idle, activity = discord.Game("VALORANT"))
    print("oowwee im up")

@client.event
async def on_message(message):
    if client.user.id == message.author.id:
        return
    if '69' in message.content:
        await message.reply('nice!', mention_author=False)

@client.command()
async def clear(ctx, amount=3) :
    await ctx.channel.purge(limit=amount)


client.run(token)
