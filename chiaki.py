import discord
import asyncio
import random
import sys
from time import time

client = discord.Client()

global bot_startup
bot_startup = 0

def calculateTime(totalseconds):
    totalminutes = int(totalseconds/60)
    seconds = int(totalseconds % 60)
    totalhours = int(totalminutes / 60)
    minutes = int(totalminutes % 60)
    totaldays = int(totalhours / 24)
    hours = int(totalhours % 24)

    return [totaldays, hours, minutes, seconds]

def divide(a, b):
    result = a // b
    remainder = a % b
    return [result, remainder]

async def kick(member):
    await client.kick(member);

async def ban(member):
    await client.ban(member);

async def unban(member):
    await client.unban(member)

@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print('-' * 20)
    bot_startup = time()
@client.event
async def on_message(message):
    if message.content.startswith('!test'):
        await client.send_message(message.channel, 'This is a test response')

    elif message.content.startswith('!8ball'):
        magicball = ['It is certain', 'It is decidedly so', 'Without a doubt',
        'Yes, definitely', 'You may rely on it', 'As I see it, yes', 'Most likely',
        'Outlook good', 'Yes', 'Signs point to yes', 'Reply hazy try again',
        'Ask again later', 'Better not tell you now', 'Cannot predict now',
        'Concentrate and ask again', 'Don\'t count on it', 'My reply is no',
        'My sources say no', 'Outlook not so good', 'Very doubtful']
        await client.send_message(message.channel, random.choice(magicball))
    elif message.content.startswith('!ping'):
        await client.send_message(message.channel, 'Your net is working, %s-kun' % message.author.name)
    elif message.content.startswith('!malid'):
        tmp = message.content.split()
        if len(tmp) >= 2:
            await client.send_message(message.channel, 'Here\'s your MAL ID, http://myanimelist.net/animelist/%s' % tmp[1])
        else:
            await client.send_message(message.channel, 'Please enter the right number of arguments and try again')
    elif message.content.startswith('!kill'):
        await client.send_message(message.channel, 'Chiaki will now exit.')
        sys.exit()
    elif message.content.startswith('!urban'):
        tmp = message.content.split()
        if len(tmp) >= 2:
            await client.send_message(message.channel, 'http://www.urbandictionary.com/define.php?term=%s' % tmp[1])
        else:
            await client.send_message(message.channel, 'Please enter an argument.')
    elif message.content.startswith('!help'):
        await client.send_message(message.channel, 'This doesnt contain anything. _yet_')
    elif message.content.startswith('!uptime'):
        seconds = int(time() - bot_startup)
        minutes = seconds / 60
        hours = minutes / 60
        days = hours / 24
        if seconds < 60:
            await client.send_message(message.channel, 'Chiaki has been up for **%d** seconds.' % seconds)
        elif seconds >= 60:
            division = divide(seconds, 60)
            await client.send_message(message.channel, 'Chiaki has been up for **%d** minutes and **%d** seconds' % (division[0], division[1]))
        elif minutes >= 60:
            division_h = divide(minutes, 60)
            seconds = division_h[2] * 60
            division = divide(seconds, 60)
            await client.send_message(message.channel, 'Chiaki has been up for **%d** hours, **%d** minutes and **%d** seconds.' % (division_h[0], division[0], division[1]))
        else:
            time = calculateTime(seconds)
            await client.send_message(message.channel, 'Chiaki has been up for **%d** days, **%d** hours, **%d** minutes and **%d** seconds.' % (time[0], time[1], time[2], time[3]))
token = open('token', 'r').read()
token = token.rstrip('\n')
client.run(token)
