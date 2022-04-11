# bot.py
import os
import random
#from emojis import EMOJI_DATA
from discord.ext import commands
from dotenv import load_dotenv
import emoji

import asyncio

emojis=list(emoji.unicode_codes.EMOJI_DATA.keys())

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='_')

@bot.command(name='respond', help='Responds with a random response.')
async def bot_response(ctx):
    bot_response_list = [
        'Ok, here is a response.',
        'Hi...You',
        'This is the reponse you have been waiting for'
    ]

    response = random.choice(bot_response_list)
    await ctx.send(response)

@bot.command(pass_context=True, name='emoji', help='Responds with a random emoji.')
async def bot_emoji(ctx):
    response = random.choice(emojis)
    await ctx.send(response)

@bot.command(pass_context=True, name='random', help='Returns a random number between x and y\n Example:\n_random 0 100 \nReturns a random number between 0 and 100')
async def bot_random(ctx, *args):
    nums = [int(args[0]), int(args[1])]
    random_number = random.randint(min(nums), max(nums))
    await ctx.send("Here is your random number between {min} and {max}:\t {rand}".format(min=min(nums), max=max(nums), rand=random_number))

@bot.command(pass_context=True, name='randomgame', help='Extended version of random where you can guess a number between x and y')
async def bot_random_game(ctx, *args):
    def is_correct(m):
        return m.author == ctx.author and m.content.isdigit()
    await ctx.channel.send('Minimum Value: ')
    try:
        min_val = await bot.wait_for('message', check=is_correct, timeout=10.0)
    except asyncio.TimeoutError:
        return await ctx.channel.send('Sorry, you took too long')
    await ctx.channel.send('Maximum Value: ')
    try:
        max_val = await bot.wait_for('message', check=is_correct, timeout=10.0)
    except asyncio.TimeoutError:
        return await ctx.channel.send('Sorry, you took too long')
    nums = [int(min_val.content), int(max_val.content)]
    random_number = random.randint(min(nums), max(nums))
    await ctx.channel.send('Number of tries: ')
    try:
        tries = await bot.wait_for('message', check=is_correct, timeout=10.0)
        tries = int(tries.content)
    except asyncio.TimeoutError:
        tries = 1
        await ctx.channel.send('Number of tries set to 1.')
    await ctx.channel.send('Guess a number between {} and {}.'.format(min(nums), max(nums)))
    while tries != 0:
        try:
            guess = await bot.wait_for('message', check=is_correct, timeout=10.0)
        except asyncio.TimeoutError:
            await ctx.channel.send('Sorry, you took too long')

        if int(guess.content) == random_number:
            return await ctx.channel.send('You are right!')
        elif tries >1:
            await ctx.channel.send('Oops. Try again')
        
        tries = tries -1
    
    await ctx.channel.send('You lost. the number was {}'.format(random_number))

bot.run(TOKEN)