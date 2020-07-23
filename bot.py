####IDEAS##############
# DONE randomize every action - 1/4 chance that Amy ignores you or goes "Grrrrr" -> random_cat_behaviour
# DONE >friends - show cat photos
# DONE >futter - daily check in
# DONE list of commands
# kotz_behaviour ->  -> try to kotz in a random channel -> prevent it by typing >scream/take her away/push her -> goes back into main channel -> /clean
# activities -> add long sleeping inbetween
# goes to scratch pad -> cat emotional release
# change bot avatar picture -> loop
# hunting game -> throw an item to another channel -> cat tries to catch it / show where with #channel
# somehow represent her strawberry obsession
# randomly starts meowing, sometimes holding mouse in her mouth
####IDEAS##############


import re

import requests
from discord.ext import commands, tasks
import discord
import random
from itertools import cycle

rulesFile = open("rules.txt", encoding="UTF-8")
rules = rulesFile.readlines()

current_prefix = 'Amy '

current_channel = {}

def get_prefix(client, message):
    return commands.when_mentioned_or(current_prefix)(client, message)

client = commands.Bot(command_prefix=get_prefix)

cat_activities = cycle(
    ['with your underwear', 'the laserpointer game', 'with her mice', 'hide no seek', 'sleep world record',
     'kitchen climbing simulator', 'shadow hunters', 'singstar - meow at a corner edition'])


@client.event
async def on_ready():
    print("discord version: " + discord.__version__)
    change_activity.start()
    walk_around.start()
    print("Amy wakes up")

    global current_channel
    current_channel = client.get_channel(734552235131797590)  # 'the-amish-people'

########################
# Random Cat Behaviour #
########################
# you could use checks instead : https://www.youtube.com/watch?v=9KOJgfaUPmQ
class CatInterrupt(Exception):
    pass

@client.before_invoke
async def random_cat_behaviour(ctx):
    possibleMessages = ["Grrr...", "Meow.", "Meow?", "*Turns and walks away.*", '*Sleeping.*']
    chance = 0
    if random.randrange(1, 100) <= chance:
        possible_behaviour = [1, 2]
        behaviour = random.choice(possible_behaviour)
        # 1 : do nothing
        # 2 : random message
        if behaviour == 2:
            await ctx.send(random.choice(possibleMessages))
        raise CatInterrupt
    else:
        return

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CatInterrupt):
        print("cat error3")
        return  # Ignore Cat Related Errors
    else:
        print(error)
########################
# Random Cat Behaviour #
########################

@client.check
async def is_amy_here(ctx):
    return ctx.channel == current_channel


@tasks.loop(seconds=10)
async def change_activity():
    await client.change_presence(activity=discord.Game(next(cat_activities)))


@client.command(aliases=['meow', 'greetings', 'hello'])
async def hey(ctx):
    """Greet the cat and hope she greets you back"""
    await ctx.send(f'*Meows at you, {ctx.author.name}.*')


@client.command()
@commands.cooldown(1, 60 * 60 * 24, commands.BucketType.user)
async def food(ctx):
    """Feed the cat once per day"""
    await ctx.send('*nom, nom, nom*')


@food.error
async def food_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        seconds = int(error.retry_after) % (24 * 3600)
        hours = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        await ctx.send(f"That's too much! Please wait {hours} hours, {minutes} minutes and {seconds} seconds.")


@client.command()
async def rule(ctx, *, number):
    """Show cat rule number X"""
    await ctx.send(rules[int(number) - 1])


@client.command()
async def friends(ctx):
    """Show a random cat image from https://random.cat"""
    await ctx.send(random_cat_image())


def random_cat_image():
    r = requests.get('https://random.cat')
    img = re.search('(?<=<meta property="og:image" content=")(.*?)(?=" />)', r.text)
    return img.group()


@client.command()
async def goto(ctx, channel: discord.TextChannel):
    """Tell Amy to go to another channel"""
    change_channel(channel)
    await ctx.send('*Walks to ' + channel.mention + '.*')


def change_channel(channel):
    global current_channel
    current_channel = channel


@client.command()
async def prefix(ctx, prefix):
    """Change prefix"""
    global current_prefix
    current_prefix = prefix
    await ctx.send('prefix changed to ' + prefix)

@client.command()
async def true_name(ctx):
    """You can only control a demon if you know their true name"""
    await ctx.send('Aimée')

@tasks.loop(minutes=30)
async def walk_around():
    global current_channel
    for guild in client.guilds:
        channel = random.choice(guild.text_channels)
        await current_channel.send(f'*Wanders to {channel.mention}.*')
        change_channel(channel)


client.load_extension('cogs.testcog')
client.load_extension('cogs.debugger')


client.run("NzM0NTQyMTQ4NTg1NjUyMjM2.XxTQtw.exOljvI5KTN35CVG1FPWDAmW2y4")
