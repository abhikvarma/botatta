import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import random
import youtube_dl
import asyncio


load_dotenv()

client = commands.Bot(command_prefix="atta ")
token = os.getenv("DISCORD_BOT_TOKEN")

#vars
last_played = None

#output on ready
@client.event
async def on_ready() :
    await client.change_presence(status = discord.Status.idle, activity = discord.Game("VALOLANT"))
    print("oowwee im up")

#say nice
@client.event
async def on_message(message):
    check = ['69','420']
    if any(x in message.content for x in check):
        raw_mentions = ['<@!{0}>'.format(each) for each in message.raw_mentions]
        words = list(filter(lambda word: word not in raw_mentions,message.content.split()))
        words = ''.join(words)
        count = 0
        for each in check:
            count+= words.count(each)
        if(count and count<=2): await message.channel.send('Nice :ok_hand:')
        elif count>=3: await message.channel.send('Oh lord thats very nice :fire::fire:')
    await client.process_commands(message)
    #if client.user.id != message.author.id:

#sing
@client.command(aliases=[]) #fill this
async def sing(ctx):
    if (ctx.author.voice):
        global last_played
        channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            voice = await channel.connect()
        else: 
            if ctx.author.voice.channel == ctx.voice_client.channel:
                voice = ctx.voice_client 
            else:
                voice = await ctx.voice_client.move_to(ctx.author.voice.channel)
        source = discord.FFmpegPCMAudio('./res/atta_song_low.mp3')
        obj = object()
        last_played = id(obj)
        ctx.voice_client.play(source)
        while voice.is_playing(): 
            await asyncio.sleep(1) 
        else:
            await asyncio.sleep(60)
            if last_played == id(obj):
                await voice.disconnect()
    else:
        await ctx.message.channel.send('Ayeeee\njoin voice channel')

#noises
@client.command(aliases=['random','moo'])
async def noises(ctx):
    if (ctx.author.voice):
        global last_played
        channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            voice = await channel.connect()
        else: 
            if ctx.author.voice.channel == ctx.voice_client.channel:
                voice = ctx.voice_client 
            else:
                voice = await ctx.voice_client.move_to(ctx.author.voice.channel)
        source = discord.FFmpegPCMAudio('./res/noises/'+random.choice(os.listdir('./res/noises')))
        obj = object()
        last_played = id(obj)
        ctx.voice_client.play(source)
        while voice.is_playing(): 
            await asyncio.sleep(1) 
        else:
            await asyncio.sleep(60)
            if last_played == id(obj):
                await voice.disconnect()
    else:
        await ctx.message.channel.send('Ayeeee\njoin voice channel')

#stop singing and leave vc
@client.command(aliases=['stfu','myearshurt','stop'])
async def leave(ctx):
    if(ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.message.channel.send('Ok :slight_frown:')
    else:
        await ctx.message.channel.send('Huh im not on a voice channel')


#clear messages
@client.command()
@commands.has_permissions(manage_messages = True) #handle errors here
async def clear(ctx, amount=3) :
    await ctx.channel.purge(limit=amount+1)


#put people in detention
@client.command(aliases=['jail','shut','shoo'])
@commands.has_guild_permissions(move_members = True) #handle errors here
async def detain(ctx):  #figure out permissions
    det_channel = None
    for channel in ctx.message.guild.channels:
        if "detention" in channel.name:
            det_channel = channel
            break           
    members = ctx.message.mentions
    for member in members:
        await member.move_to(det_channel)


@client.command(aliases=['createquiz'])
async def quiz(ctx):
    guild = ctx.message.guild
    categories = guild.categories
    for channel in ctx.message.guild.channels:
        if "answers-yes" in channel.name:
            await ctx.message.channel.send('Its already there no :eyes:')
            return
    await guild.create_text_channel('answers-yes',category=categories[0])

@client.command(aliases=['selfdestruct'])
async def purge(ctx):
    for channel in ctx.message.guild.channels:
        if "answers-yes" in channel.name:
            await channel.delete()
            await ctx.message.channel.send('Its gone bro')
            return
    await ctx.message.channel.send('Huh theres nothing to delete')

#COMMENT THIS TO DEBUG 
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('no')
    if isinstance(error, commands.CommandInvokeError):
       await ctx.send('Aye you wait da')


client.run(token)
