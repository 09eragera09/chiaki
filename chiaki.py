import discord
import asyncio
import random
from time import time

client = discord.Client()

global bot_startup
bot_startup = 0

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
        if tmp.length >= 2:
            await client.send_message(message.channel, 'Here\'s your MAL ID, http://myanimelist.net/animelist/%s' % tmp[1])
        else:
            await client.send_message(message.channel, 'Please enter the right number of arguments and try again')

token = open('token', 'r').read()
client.run('token')
