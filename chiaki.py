import discord
import asyncio
import random
import sys
import threading
from time import time

async def reminder(author, the_list):
    sentence = ' '.join(the_list)
    print("It worked till here")
    await client.send_message(author, sentence)

async def prune(message):
    splitted = message.content.split()
    num = 0
    for x in splitted[1:]:
        try:
            num = int(x)
            break
        except:
            pass
    to_delete = []
    if message.mentions:
        for x in message.mentions:
            count = 0
            for y in reversed(client.messages):
                if message.server == y.server and y.author == x:
                    to_delete.append(y)
                    count += 1
                if count == num:
                    break
    else:
        count = 0
        for x in reversed(client.messages):
            if message.server == x.server:
                to_delete.append(x)
                count += 1
            if count == num:
                break

    await client.delete_messages(to_delete)

def getTime():
    return time()

def checkForAuth(message, perm):
    auth = False
    if message.author == message.server.owner or message.author.id == "94374744576512000":
        auth = True

    else:
        if perm == "manage_messages":
            for x in message.author.roles:
                if x.permissions.manage_messages:
                    auth = True
                    break
        if perm == "kick_members":
            for x in message.author.roles:
                if x.permissions.kick_members:
                    auth = True
                    break
        elif perm == "ban_members":
            for x in message.author.roles:
                if x.permissions.ban_members:
                    auth = True
                    break
        elif perm == "manage_roles":
            for x in message.author.roles:
                if x.permissions.manage_roles:
                    auth = True
                    break
    return auth

client = discord.Client()

global bot_startup

async def mute(member):
    if not "Muted" in [x.name for x in member.server.roles]:
        await client.create_role(member.server, name="Muted", permissions=discord.Permissions.none())
        await client.send_message(member.server.owner, "The `Muted` role has been created for moderation purposes. Please push it up the list for more effective usage")
    await client.add_roles(member, [x for x in member.server.roles if x.name == "Muted"][0])
    #silences[member.id] = [member.server.id, time()]

async def unmute(member):
    if not "Muted" in [x.name for x in member.roles]:
        await client.send_message(message.channel, "This user is not Muted, so not unmuted")
    await client.remove_roles(member, [x for x in member.roles if x.name == "Muted"][0])

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
    global bot_startup
    bot_startup = getTime()
    game = ['Send Help']
    client.change_presence(game = game[0])
@client.event
async def on_message(message):
    if message.content.startswith('!test'):
        await client.send_message(message.channel, 'This is a test response')

        #FUN STUFF +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    elif message.content.startswith('!lenny'):
        await client.send_message(message.channel, '( ͡° ͜ʖ ͡°)')

    elif message.content.startswith('!shrug'):
        await client.send_message(message.channel, '¯\_(ツ)_/¯')

    elif message.content.startswith('!fiteme'):
        await client.send_message(message.channel, '(ง ͠° ͟ل͜ ͡°)ง')

    elif message.content.startswith('!hug'):
        await client.send_message(message.channel, '༼ つ ◕_◕ ༽つ')

    elif message.content.startswith('!flip'):
        await client.send_message(message.channel, '(╯°□°）╯︵ ┻━┻')

    elif message.content.startswith('!unflip'):
        await client.send_message(message.channel, '┬──┬ ノ( ゜-゜ノ)')

    elif message.content.startswith('!8ball'):
        magicball = ['It is certain', 'It is decidedly so', 'Without a doubt',
        'Yes, definitely', 'You may rely on it', 'As I see it, yes', 'Most likely',
        'Outlook good', 'Yes', 'Signs point to yes', 'Reply hazy try again',
        'Ask again later', 'Better not tell you now', 'Cannot predict now',
        'Concentrate and ask again', 'Don\'t count on it', 'My reply is no',
        'My sources say no', 'Outlook not so good', 'Very doubtful']
        await client.send_message(message.channel, random.choice(magicball))

    elif message.content.startswith('!mal'):
        tmp = message.content.split()
        if len(tmp) >= 2:
            await client.send_message(message.channel, 'Here\'s your Myanimelist, http://myanimelist.net/animelist/%s' % tmp[1])
        else:
            await client.send_message(message.channel, 'Please enter a username')

    elif message.content.startswith('!hb'):
        tmp = message.content.split()
        if len(tmp) >= 2:
            await client.send_message(message.channel, 'Here\'s your Hummingbird library, https://hummingbird.me/users/%s/library' % tmp[1])
        else:
            await client.send_message(message.channel, 'Please enter a username')

    elif message.content.startswith('!anilist'):
        tmp = message.content.split()
        if len(tmp) >= 2:
            await client.send_message(message.channel, 'Here\'s your anilist animelist, https://anilist.co/user/%s/animelist' % tmp[1])
        else:
            await client.send_message(message.channel, 'Please enter a username')

    elif message.content.startswith('!urban'):
        tmp = message.content.split()
        if len(tmp) >= 2:
            await client.send_message(message.channel, 'http://www.urbandictionary.com/define.php?term=%s' % tmp[1])
        else:
            await client.send_message(message.channel, 'Please enter an argument.')

            #FUN END ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

            #MODERATION++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    elif message.content.startswith('!ban'):
        authorized = checkForAuth(message, "ban_members")
        await client.delete_message(message)
        if authorized:
            for member in message.mentions:
                await ban(member)
            await client.send_message(message.channel, "%s has been banned" % member)
        else:
            await client.send_message(message.channel, "You are not authorized to use the ban command.")

    elif message.content.startswith('!kick'):

        authorized = checkForAuth(message, "kick_members")
        await client.delete_message(message)
        if authorized:
            for member in message.mentions:
                await kick(member)
            await client.send_message(message.channel, "%s has been kicked" % member)

        else:
            await client.send_message(message.channel, "You are not authorized to use the kick command")
    elif message.content.startswith('!mute'):
        authorized = checkForAuth(message, "manage_roles")
        if authorized:
            for member in message.mentions:
                await mute(member)
            await client.send_message(message.channel, "%s has been Muted" % member)

    elif message.content.startswith('!unmute'):
        authorized = checkForAuth(message, "manage_roles")
        if authorized:
            for member in message.mentions:
                await unmute(member)
            await client.send_message(message.channel, "%s has been unmuted" % member)

            #MODERATION END +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

            #UTILITY ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    elif message.content.startswith('!prune'):
        authorized = checkForAuth(message, "manage_messages")
        if authorized:
            await prune(message)

    elif message.content.startswith('!uptime'):
        currentTime = getTime()
        seconds = int(currentTime - bot_startup)
        minutes = seconds / 60
        hours = minutes / 60
        days = hours / 24
        if seconds < 60:
            await client.send_message(message.channel, 'I have been up for **%d** seconds! Let\'s go to the arcade!' % seconds)
        elif seconds <= 3600:
            division = divide(seconds, 60)
            await client.send_message(message.channel, 'I have been up for **%d** minutes and **%d** seconds. I\'m bored.' % (division[0], division[1]))
        elif seconds <= 3600 * 24:
            division_h = divide(minutes, 60)
            seconds = division_h[1] * 60
            division = divide(seconds, 60)
            await client.send_message(message.channel, 'I have been up for **%d** hours, **%d** minutes and **%d** seconds. Im sleepy....' % (division_h[0], division[0], division[1]))
        else:
            time = calculateTime(seconds)
            await client.send_message(message.channel, 'Chiaki has been up for **%d** days, **%d** hours, **%d** minutes and **%d** seconds. Oh, it seems she\'s sleeping while standing.' % (time[0], time[1], time[2], time[3]))

    elif message.content.startswith('!sleep'):
        if message.author.id == "94374744576512000":
            await client.send_message(message.channel, 'Era-kun, carry me to bed')
            sys.exit()
        else:
            await client.send_message(message.channel, "Mou! You're not Era-kun.")

    elif message.content.startswith('!ping'):
        if message.author.id == "94374744576512000":
            ping = await client.send_message(message.channel, 'Your net is working, Era-kun')
            tmptime = getTime()
            await client.get_message(message.channel, ping.id)
            tmptime1 = getTime()
            pingtime = tmptime1 - tmptime
            pingtime *= 1000
            await client.edit_message(ping, new_content="Your net is working, Era-kun. `%dms`" % pingtime)
        else:
            ping = await client.send_message(message.channel, 'Pong!')
            tmptime = getTime()
            await client.get_message(message.channel, ping.id)
            tmptime1 = getTime()
            pingtime = tmptime1 - tmptime
            pingtime *= 1000
            await client.edit_message(ping, new_content="Pong! `%dms`" % pingtime)

    elif message.content.startswith('!remindme'):
        splitted = message.content.split()
        try:
            tmptime = int(splitted[1])
        except:
            await client.send_message(message.channel, "Please try again. It should be in the form of `!remindme (a number) (hours/minutes/seconds) (a message)`")
        if str(splitted[2]) == "seconds":
            threading.Timer(tmptime, reminder, message.author, splitted[3:])
            await client.send_message(message.channel, "You will be send a reminder through DM in %s seconds!" % splitted[1])
        elif str(splitted[2]) == "minutes":
            tmptime *= 60
            threading.Timer(tmptime, reminder, message.author, splitted[3:])
            await client.send_message(message.channel, "You will be send a reminder through DM in %s minutes!" % splitted[1])
        elif str(splitted[3]) == "hours":
            tmptime = tmptime * 60 * 60
            threading.Timer(tmptime, reminder, message.author, splitted[3:])
            await client.send_message(message.channel, "You will be send a reminder through DM in %s hours!" % splitted[1])
        else:
            await client.send_message(message.channel, "Please try again. It should be in the form of `!remindme (a number) (hours/minutes/seconds) (a message)`")

    elif message.content.startswith('!help'):
        helptext = "There are a few commands you can use.\n`!ping` to check if your net is working ;)\n`!uptime` to check how long the bot has been up\n`!8ball` the magic 8ball will reply with either an affirmative, negative or a non-commital response\n`!urban` to check urbandictionary for the definition of a term\n`!mal`, `!hb`, `!anilist` to get your animelist from myanimelist, hummingbird and anilist, respectively.\n`!lenny`, `!fiteme`, `!flip`, `!unflip`, `!hug`, and `!shrug` reply with their respective  \n\nCommands for Moderators\n`!prune`, `!ban`, `!kick`, `!mute`, and `!unmute`, do exactly what they say.\n\nCommand for Era-kun only\n`!sleep`\nHere's my source code: https://github.com/09eragera09/chiaki/blob/master/chiaki.py\nTo invite me to your server, click this link: https://discordapp.com/oauth2/authorize?&client_id=241587632948248586&scope=bot"
        await client.send_message(message.author, helptext)

    elif message.content.startswith("!source"):
        await client.send_message(message.channel, "Here's my source code https://github.com/09eragera09/chiaki/blob/master/chiaki.py")

    elif message.content.startswith("!invite"):
        await client.send_message(message.channel, "Here's my invite link https://discordapp.com/oauth2/authorize?&client_id=241587632948248586&scope=bot")

token = open('token', 'r').read()
token = token.rstrip('\n')
client.run(token)
