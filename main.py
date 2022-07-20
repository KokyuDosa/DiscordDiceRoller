#     A dice rolling bot for discord.
#     Copyright (C) 2022  Nikolas Kanetomi
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>

import random
import re
import os

from discord.ext import commands

from private import token

description = '''D&D Dice rolling bot.'''

bot = commands.Bot(command_prefix='.', description=description)


@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')


@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')

if __name__ == '__main__':
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')


# # Usage: attack roll (1d20+mod) (crit threshold) (crit multiplier) (damage roll(s))
# @bot.command(pass_context=True, name='a')
# async def attack(ctx, *args):
#     message = 'Usage: attack roll (1d20+mod) (crit threshold) (damage roll(s))'
#     if len(args) < 3:
#         return await ctx.channel.send(message)
#     if int(args[1]) < 1 and int(args[1]) > 20:
#         return await ctx.channel.send(message)
#     arg0 = parse_string(args[0])
#     arg1 = int(args[1])

@bot.event
async def on_ready():
    print('Logged in as:')
    print(bot.user.name)
    print('Bot is ready!')


bot.run(token)
