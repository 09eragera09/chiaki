import discord
import logging
import asyncio
import random
import sys
import threading
import subprocess
from pybooru import Danbooru
from wand.drawing import Drawing
from wand.image import Image
from wand.color import Color
from time import time, strftime

async def game_check(member):
    if not(member.game):
        return "Unknown"
    else:
        return str(member.game.name)

async def role_name_grabber(member):
    role_list = []
    for role in member.roles:
        role_list.append(role.name)
    return role_list

async def userinfo(name, message):
    member = message.server.get_member_named(name)
    role_list = await role_name_grabber(member)
    role_list_joined = ", ".join(role_list[1:])
    game = await game_check(member)
    embed = discord.Embed(title="❯ Member Details", description="• Nickname: %s\n• Roles: %s\n• Joined at: %s" % (member.nick, role_list_joined, member.joined_at.strftime("%A, %B %d, %Y, %I:%M %p")), color=0x9A32CD)
    embed.add_field(name="❯ User Details", value="• Created at: %s\n• Status: %s\n• Game: %s" % (member.created_at.strftime("%A, %B %d, %Y, %I:%M %p"), member.status, game), inline=True)
    embed.set_author(name="%s#%s" %(member.name, member.discriminator), icon_url=member.avatar_url)
    embed.set_footer(text="Userinfo, a method on the shitty python bot Chiaki", icon_url=client.user.avatar_url)
    embed.set_thumbnail(url=member.avatar_url)
    await client.send_message(message.channel, embed=embed)

def imageGen(member):
    if len(member.name) > 15 and len(member.name) < 22:
        with Drawing() as draw:
            draw.font_size = 35
            draw.fill_color = Color('white')
            draw.font = 'assets/Whitney_Medium.ttf'
            draw.text(x=510, y=350, body="User: %s#%s" % (member.name, member.discriminator))
            with Image(filename='assets/KUD_3.png') as image:
                draw(image)
                image.save(filename='assets/test.png')
                return None
    if len(member.name) >= 22:
        with Drawing() as draw:
            draw.font_size = 30
            draw.fill_color = Color('white')
            draw.font = 'assets/Whitney_Medium.ttf'
            draw.text(x=510, y=350, body="User: %s#%s" % (member.name, member.discriminator))
            with Image(filename='assets/KUD_3.png') as image:
                draw(image)
                image.save(filename='assets/test.png')
                return None
    else:
        with Drawing() as draw:
            draw.font_size = 40
            draw.fill_color = Color('white')
            draw.font = 'assets/Whitney_Medium.ttf'
            draw.text(x=510, y=350, body="User: %s#%s" % (member.name, member.discriminator))
            with Image(filename='assets/KUD_3.png') as image:
                draw(image)
                image.save(filename='assets/test.png')
                return None

async def reminder(author, the_list, date):
    sentence = ' '.join(the_list)
    await client.send_message(author, "You had set a reminder on %s GMT for the following message: %s" % (date, sentence))

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
danbooru = Danbooru('danbooru', username='09eragera09', api_key='X6PIMs2DWAOyNmKBZ6HFzjGWqaLMB7ydvsaDJMrTgmI')


global bot_startup

async def mute(member):
    if not "Muted" in [x.name for x in member.server.roles]:
        await client.create_role(member.server, name="Muted", permissions=discord.Permissions.none())
        await client.send_message(member.server.owner, "The `Muted` role has been created for moderation purposes. Please push it up the list for more effective usage")
    await client.add_roles(member, [x for x in member.server.roles if x.name == "Muted"][0])

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
    print("Logged in as %s" % client.user.name)
    print("Chiaki will do her best!")
    print(client.user.id)
    print('-' * 20)
    global bot_startup
    bot_startup = getTime()
    #discord.Game.name = "Send Help"
    #client.change_presence(game=discord.Game.name)
@client.event
async def on_message(message):
    if message.content.startswith('!test'):
        await client.send_message(message.channel, 'This is a test response')

        #FUN STUFF +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    elif message.content.startswith('!rr'):
        luck = random.randint(1,7)
        if luck == 6:
            await client.send_message(message.channel, "You're in luck! You hit the blank!")
        else:
            await client.send_message(message.channel, "Too bad. You were unlucky. Nagato is disappointed.")


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

    elif message.content.startswith("!shitwaifu"):
        await client.send_message(message.channel, "http://azelf.net/mfw/shitwaifu.png")

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

    elif message.content.startswith('!enlarge'):
        splitted = message.content.split()
        emoji = splitted[1]
        emoji_id = emoji.split(":")[-1]
        emoji_id = emoji_id.rstrip('>')
        await client.send_message(message.channel, "Custom emote has been enlarged, https://discordapp.com/api/emojis/%s.png" % emoji_id)
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
            client.close()
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

    elif message.content.startswith('!remind'):
        splitted = message.content.split()
        try_again = "Please try again. It should be in the form of `!remind (a number) (hours/minutes/seconds) (a message)`"
        if len(splitted) >= 4:
            try:
                tmptime = int(splitted[1])
            except:
                await client.send_message(message.channel, try_again)
            date = strftime("%Y-%m-%d %H:%M")
            if splitted[2] in ["second", "seconds"]:
                await client.send_message(message.channel, "You will be send a reminder through DM in %s second(s)!" % splitted[1])
                await asyncio.sleep(tmptime)
                await reminder(message.author, splitted[3:], date)
            elif splitted[2] in ["minute", "minutes"]:
                tmptime *= 60
                await client.send_message(message.channel, "You will be send a reminder through DM in %s minute(s)!" % splitted[1])
                await asyncio.sleep(tmptime)
                await reminder(message.author, splitted[3:], date)
            elif splitted[2] in ["hour", "hours"]:
                tmptime = tmptime * 60 * 60
                await client.send_message(message.channel, "You will be send a reminder through DM in %s hour(s)!" % splitted[1])
                await asyncio.sleep(tmptime)
                await reminder(message.author, splitted[3:], date)
            else:
                await client.send_message(message.channel, try_again)
        else:
            await client.send_message(message.channel, try_again)

    elif message.content.startswith('!help'):
        userhelp = ["There are a few commands you can use.",
        "• `!ping` to check if your net is working ;)",
        "• `!uptime` to check how long the bot has been up",
        "• `!userinfo` to check your or someone else's basic account info",
        "• `!avatar` to get someone's avatar",
        "• `!status` Prints the bot's status",
        "• `!remind` will let you set a reminder.",
        "• `!booru` searches Danbooru, accepts tags, use an underscore, for example, `!booru competition_swimsuit`",
        "• `!sfw` same as above, but with safe images forced",
        "• `!nsfw` same as above, but with explicit images forced",
        "• `!enlarge` enlarges custom emojis such as ones from NGNL",
        "• `!invite` lets you get the bot invite link",
        "• `!8ball` the magic 8ball will reply with either an affirmative, negative or a non-commital response",
        "• `!urban` to check urbandictionary for the definition of a term",
        "• `!mal`, `!hb`, `!anilist` to get your animelist from myanimelist, hummingbird and anilist, respectively.",
        "• `!welcome` to test the welcome card",
        "• `!lenny`, `!fiteme`, `!flip`, `!unflip`, `!hug`, and `!shrug` reply with their respective emojis ",
        "Here's my source code: https://github.com/09eragera09/chiaki/blob/master/chiaki.py",
        "To invite me to your server, click this link: https://discordapp.com/oauth2/authorize?&client_id=241587632948248586&scope=bot"]

        modhelp = ["• `!prune`, `!ban`, `!kick`, `!mute`, and `!unmute`, do exactly what they say."]

        ownerhelp = ["Command for Era-kun only",
        "• `!sleep` makes the bot go offline",
        "• `!restart` makes the bot restart",
        "• `subprocess` makes the bot execute commands in shell"]
        userhelp = '\n'.join(userhelp)
        embed = discord.Embed(title="❯ User Commands", description=userhelp, color=0x9A32CD)
        embed.set_author(name="Command List", icon_url=message.author.avatar_url)
        embed.set_footer(text="Chiaki is a shitty bot written in python", icon_url=client.user.avatar_url)
        if message.author.id == "94374744576512000":
            modhelp = '\n'.join(modhelp)
            embed.add_field(name="❯ Mod Commands", value=modhelp)
            ownerhelp = '\n'.join(ownerhelp)
            embed.add_field(name="❯ Owner Commands", value=ownerhelp)
            await client.send_message(message.author, embed=embed)
        elif [x for x in message.server.roles if x.name == "Staff"][0] in message.author.roles:
            modhelp = '\n'.join(modhelp)
            embed.add_field(name="❯ Mod Commands", value=modhelp)
            await client.send_message(message.author, embed=embed)
        else:
            await client.send_message(message.author, embed=embed)

    elif message.content.startswith("!source"):
        await client.send_message(message.channel, "Here's my source code https://github.com/09eragera09/chiaki/blob/master/chiaki.py")

    elif message.content.startswith("!invite"):
        await client.send_message(message.channel, "Here's my invite link https://discordapp.com/oauth2/authorize?&client_id=241587632948248586&scope=bot")

    elif message.content.startswith("!welcome"):
        imagegen = imageGen(message.author)
        await client.send_file(message.author.server, 'assets/test.png', content="Welcome to Kindly United Dreams, %s, Please read the rules over at <#%s>" % (message.author.mention, [x.id for x in message.author.server.channels if x.name == "readme"][0]))

    elif message.content.startswith("!embed"):
        embed = discord.Embed(title="This is test", description="Lorem Ipsum", color=0x9A32CD)
        embed.add_field(name="Test", value="Lorem Ipsum")
        embed.set_thumbnail(url=message.author.avatar_url)
        await client.send_message(message.channel, embed=embed)

    elif message.content.startswith("!status"):
        embed = discord.Embed(title="%s#%s" %(client.user.name, client.user.discriminator), description="A shitty python bot", color=0x9A32CD)
        embed.add_field(name="Owner", value="Era#4669", inline=False)
        currentTime = getTime()
        seconds = int(currentTime - bot_startup)
        uptime = calculateTime(seconds)
        embed.add_field(name="Uptime", value="%sd%sh%sm%ss" % (uptime[0], uptime[1], uptime[2], uptime[3]), inline=False)
        embed.set_thumbnail(url=client.user.avatar_url)
        await client.send_message(message.channel, embed=embed)

    elif message.content.startswith("!userinfo"):
        splitted = message.content.split()
        if len(splitted) == 1:
            await userinfo(message.author.name, message)
        elif message.mentions and not message.mention_everyone:
            user = message.mentions[0]
            await userinfo(user.name, message)
        elif len(splitted) > 1:
            await userinfo(" ".join(splitted[1:]), message)
        else:
            await client.send_message(message.channel, "Unknown User")
    elif message.content.startswith("!eval"):
        splitted = message.content.split()
        if message.author.id == "94374744576512000":
            await client.send_message(message.channel, eval(splitted[1]))
        else:
            await client.send_message(message.channel, "Oh hey Era-ku-- Wait, You're not Era-kun!")
    elif message.content.startswith("!restart"):
        if message.author.id == "94374744576512000":
            subprocess.call(["./chiaki.sh"], shell=True)
        else:
            await client.send_message(message.channel, "Oh hey Era-ku-- Wait, You're not Era-kun!")

    elif message.content.startswith("!avatar"):
        splitted = message.content.split()
        if len(splitted) == 1:
            await client.send_message(message.channel, message.author.avatar_url)
        elif message.mentions and not message.mention_everyone:
            user = message.mentions[0]
            await client.send_message(message.channel, user.avatar_url)
        elif len(splitted) > 1:
            name = " ".join(splitted[1:])
            member = message.server.get_member_named(name)
            await client.send_message(message.channel, member.avatar_url)
        else:
            await client.send_message(message.channel, "Unknown User")

    elif message.content.startswith("!say"):
        splitted = message.content.split()
        if message.author.id == "94374744576512000":
            await client.send_message(message.channel, " ".join(splitted[1:]))

    elif message.content.startswith("!subprocess"):
        if message.author.id == "94374744576512000":
            #wip
            pass

    elif message.content.startswith("!booru"):
        splitted = message.content.split()
        splitted = ' '.join(splitted[1:])
        nsfw = [x for x in message.server.channels if x.name == "nsfw"][0]
        images = [x for x in message.server.channels if x.name == "images"][0]
        if message.channel in [nsfw, images]:
            hentai_list = danbooru.post_list(limit=50, tags=splitted)
            hentai = random.choice(hentai_list)
            hentai_url = "http://danbooru.donmai.us" + hentai['file_url']
            artist = hentai['tag_string_artist']
            artist = artist.split("_")
            artist = ' '.join(artist)
            artist = artist.title()
            embed = discord.Embed(title="Post drawn by %s" % artist, color=0x9A32CD)
            embed.set_image(url=hentai_url)
            rating = hentai['rating']
            if message.channel == images:
                if rating != 's':
                    await client.send_message(message.channel, "This image is too lewd for this channel, try again.")
                else:
                    await client.send_message(message.channel, embed=embed)
            else:
                await client.send_message(message.channel, embed=embed)
        else:
            await client.send_message(message.channel, "Please try again in an image channel such as <#%s> or <#%s>" % (images.id, nsfw.id))

    elif message.content.startswith("!nsfw"):
        splitted = message.content.split()
        splitted.append('rating:e')
        splitted = ' '.join(splitted[1:])
        nsfw = [x for x in message.server.channels if x.name == "nsfw"][0]
        if message.channel == nsfw:
            hentai_list = danbooru.post_list(limit=50, tags=splitted)
            hentai = random.choice(hentai_list)
            hentai_url = "http://danbooru.donmai.us" + hentai['file_url']
            artist = hentai['tag_string_artist']
            artist = artist.split("_")
            artist = ' '.join(artist)
            artist = artist.title()
            embed = discord.Embed(title="Post drawn by %s" % artist, color=0x9A32CD)
            embed.set_image(url=hentai_url)
            await client.send_message(message.channel, embed=embed)
        else:
            await client.send_message(message.channel, "Please try again in <#%s>" % nsfw.id)

    elif message.content.startswith("!sfw"):
        splitted = message.content.split()
        splitted.append('rating:s')
        splitted = ' '.join(splitted[1:])
        nsfw = [x for x in message.server.channels if x.name == "nsfw"][0]
        images = [x for x in message.server.channels if x.name == "images"][0]
        if message.channel in [nsfw, images]:
            hentai_list = danbooru.post_list(limit=50, tags=splitted)
            hentai = random.choice(hentai_list)
            hentai_url = "http://danbooru.donmai.us" + hentai['file_url']
            artist = hentai['tag_string_artist']
            artist = artist.split("_")
            artist = ' '.join(artist)
            artist = artist.title()
            embed = discord.Embed(title="Post drawn by %s" % artist, color=0x9A32CD)
            embed.set_image(url=hentai_url)
            await client.send_message(message.channel, embed=embed)
        else:
            await client.send_message(message.channel, "Please try again in an image channel such as <#%s> or <#%s>" % (images.id, nsfw.id))

@client.event
async def on_member_join(member):
    imagegen = imageGen(member)
    await client.send_file(member.server, 'assets/test.png', content="Welcome to Kindly United Dreams, %s, Please read the rules over at <#%s>" % (member.mention, [x.id for x in member.server.channels if x.name == "readme"][0]))
    music_role = [x for x in member.server.roles if x.name == "Music"][0]
    image_role = [x for x in member.server.roles if x.name == "Image"][0]
    suggestion_role = [x for x in member.server.roles if x.name == "Suggestion"][0]
    role_list = [music_role, image_role, suggestion_role]
    await client.add_roles(member, role_list[0], role_list[1], role_list[2])
    await asyncio.sleep(300)
    await client.add_roles(member, [x for x in member.server.roles if x.name == "People"][0])

@client.event
async def on_voice_state_update(before, after):
    if not(after.voice.voice_channel):
        await client.remove_roles(after, [x for x in after.server.roles if x.name == "Voice-Chat"][0])
    elif (after.voice.voice_channel):
        await client.add_roles(after, [x for x in after.server.roles if x.name == "Voice-Chat"][0])

token = open('token', 'r').read()
token = token.rstrip('\n')
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
try:
    client.run(token)
except:
    subprocess.call(["./chiaki.sh"], shell=True)
