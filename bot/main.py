import discord
from discord.ext import commands
from discord.ext import tasks
import os
from dotenv import load_dotenv
import random
import youtube_dl
import asyncio
import requests
import datetime
import pytz
import csv

load_dotenv()

#intents were enabled through the developer portal
intents = discord.Intents().all()
client = commands.Bot(command_prefix="atta ", intents=intents)
token = os.getenv("DISCORD_BOT_TOKEN")


#vars
last_played = None
ist = pytz.timezone("Asia/Calcutta")


#output on ready
@client.event
async def on_ready() :
    await client.change_presence(status = discord.Status.online, activity = discord.Game("VALOLANT"))
    print("oowwee im up")
    budday.start()


#birthday crap
@tasks.loop(hours=24)
async def budday():
    global ist
    with open('./res/buddays.csv', 'r') as file:
        buddays = csv.reader(file)
        next(buddays)
        for row in buddays:
            if int(row[1][0:2]) == datetime.datetime.now(ist).month and int(row[1][3:6])==datetime.datetime.now(ist).day:
                for guild in client.guilds:
                    if guild.id == 542723128137351178 : #835037637789483018 for bt
                        for member in guild.members:
                            if member.name+'#'+member.discriminator == row[2]:
                                for channel in guild.channels:
                                    if channel.id == 689052830463688754 : #835419932865986590 for test
                                        await channel.send('Happy birthday ' + member.mention + ' :partying_face:')


#say nice
@client.event
async def on_message(message):
    check = ['69','420']
    if any(x in message.content for x in check) and client.user.id != message.author.id:
        raw_mentions = ['<@{0}>'.format(each) for each in message.raw_mentions]
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
@client.command(aliases=['kolaveridi','geography','whythis']) #fill this
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
            await asyncio.sleep(900)
            if last_played == id(obj):
                await voice.disconnect()
                await ctx.message.channel.send('I\'ll leave bro')
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
                await ctx.voice_client.move_to(ctx.author.voice.channel)
                voice = ctx.voice_client
        num = ctx.message.content.split()[-1]
        try:
            num = int(num)
            if num>10:
                await ctx.message.channel.send('That\'s too many man')
                return
        except:
            num = 1
        
        for _ in range(num):
            source = discord.FFmpegPCMAudio('./res/noises/'+random.choice(os.listdir('./res/noises')))
            obj = object()
            last_played = id(obj)
            ctx.voice_client.play(source)
            while voice.is_playing(): 
                await asyncio.sleep(1) 
        while voice.is_playing(): 
            await asyncio.sleep(1) 
        else:
            await asyncio.sleep(900)
            if last_played == id(obj):
                await voice.disconnect()
                await ctx.message.channel.send('I\'ll leave bro')
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
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount=1) :
    await ctx.channel.purge(limit=amount+1)


#put people in detention
@client.command(aliases=['jail','shut','shoo'])
@commands.has_guild_permissions(move_members = True)
async def detain(ctx):  #figure out permissions
    det_channel = None
    for channel in ctx.message.guild.channels:
        if "detention" in channel.name:
            det_channel = channel
            break           
    members = ctx.message.mentions
    if len(members)==0:
        tt = ctx.guild.get_member(454966507902992404)
        members.append(tt)
    for member in members:
        if member.voice is None:
            await ctx.message.channel.send(member.name + ' is not on a voice channel :person_facepalming:')
        else:
            await member.move_to(det_channel)


#create quiz text channel
@client.command(aliases=['createquiz'])
async def quiztime(ctx):
    guild = ctx.message.guild
    categories = guild.categories
    for channel in ctx.message.guild.channels:
        if "answers-yes" in channel.name:
            await ctx.message.channel.send('Its already there no :eyes:')
            return
    await guild.create_text_channel('answers-yes',category=categories[0])


#purge quiz text channel
@client.command(aliases=['destroy'])
async def purge(ctx):
    for channel in ctx.message.guild.channels:
        if "answers-yes" in channel.name:
            await channel.delete()
            await ctx.message.channel.send('Its gone bro')
            return
    await ctx.message.channel.send('Huh theres nothing to delete')


#covid updates
@client.command(aliases=['update'])
async def covid(ctx):
    api_data = requests.get("https://api.covid19india.org/data.json").json()
    blore_data = requests.get('https://api.covid19india.org/state_district_wise.json').json()

    i_d_con = 'no info yet' if api_data['statewise'][0]['deltaconfirmed']=='0' else '{:,d}'.format(int(api_data['statewise'][0]['deltaconfirmed']))
    i_act = int(api_data['statewise'][0]['active'])

    k_idx = next((i for i,d in enumerate(api_data['statewise']) if d['statecode']=='KA'),None)
    k_d_con = 'no info yet' if api_data['statewise'][k_idx]['deltaconfirmed']=='0' else '{:,d}'.format(int(api_data['statewise'][k_idx]['deltaconfirmed']))
    k_act = int(api_data['statewise'][k_idx]['active'])

    temp = blore_data['Karnataka']['districtData']['Bengaluru Urban']['delta']['confirmed']
    b_d_con = 'no info yet' if temp==0 else '{:,d}'.format(temp)
    b_act = blore_data['Karnataka']['districtData']['Bengaluru Urban']['active']

    embed = discord.Embed(title = 'Covid Update Time', colour = discord.Colour.blurple(), url = 'https://www.covid19india.org/')
    embed.add_field(name='India', value=f'> Today: {i_d_con}\n> Active: {i_act:,d}', inline=False)
    embed.add_field(name='Karnataka', value=f'> Today: {k_d_con}\n> Active: {k_act:,d}', inline=False)
    embed.add_field(name='Bangalore', value=f'> Today: {b_d_con}\n> Active: {b_act:,d}', inline=False)
    await ctx.message.channel.send(embed = embed)


#COMMENT THIS TO DEBUG 
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('no')
    if isinstance(error, commands.CommandInvokeError):
       await ctx.send('Aye you wait da')

client.run(token)
