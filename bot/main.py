import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import youtube_dl

load_dotenv()

client = commands.Bot(command_prefix="atta ")
token = os.getenv("DISCORD_BOT_TOKEN")

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
        else: await message.channel.send('Oh lord thats very nice :fire::fire:')
    await client.process_commands(message)
    #if client.user.id != message.author.id:

#sing
@client.command(aliases=[]) #fill this
async def sing(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = discord.FFmpegPCMAudio('./res/atta_song.mp3')
        voice.play(source)
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.souce.volume = 0.5
    else:
        await ctx.message.channel.send('Ayeeee\njoin voice channel')

#stop singing and leave vc
@client.command(aliases=['stfu','my ears hurt','stop'])
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


client.run(token)
