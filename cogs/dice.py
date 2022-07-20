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

import discord
import re
import random
from discord.ext import commands

matchString = r"^[1-9][0-9]{0,8}[d|D](2|3|4|6|8|10|12|20|100)((\+|\-)[1-9][0-9]{0,8})?$|^([2-9]|10|12|20|100)((" \
              r"\+|\-)[1-9][0-9]{0,8})?$ "


# Return: a list representation of a parsed input string for rolling a die
# in the form of [number of dice, type of die, modifier] all integers
# or a string with usage instructions
def parse_string(input_string: str):
    # check for match on result of input
    result = re.search(matchString, input_string)
    # if result exists we can parse it
    if result:
        # turn everything lowercase to potentially change a D to d
        lower_case = input_string.lower()
        # check for the case where there is a d in the string
        if lower_case.find('d') != -1:
            # check for + or -
            # split on the d either way
            values = lower_case.split('d')
            if values[1].find('+') != -1 or values[1].find('-') != -1:
                # check which it is
                if values[1].find('+') != -1:
                    die_mod = values[1].split('+')
                    return [int(values[0]), int(die_mod[0]), int(die_mod[1])]
                else:
                    # do subtraction
                    die_mod = values[1].split('-')
                    return [int(values[0]), int(die_mod[0]), int(die_mod[1]) * -1]
            else:
                # no + or - here
                return [int(values[0]), int(values[1]), 0]
        else:
            # no d here
            if input_string.find('+') != -1 or input_string.find('-') != -1:
                if input_string.find('+') != -1:
                    die_mod = input_string.split('+')
                    return [1, int(die_mod[0]), int(die_mod[1])]
                else:
                    die_mod = input_string.split('-')
                    return [1, int(die_mod[0]), int(die_mod[1]) * -1]
            else:
                # only a digit
                return [1, int(input_string), 0]
    else:
        # result doesn't exist so return error message
        return 'Usage: .r ndn e.g. `.r 1d20` or `.r 3d6+5`\nUse .help for more information.'


def roll_die(arg):
    num = arg[0]
    die = arg[1]
    mod = arg[2]
    result = 0
    list_of_rolls = ''
    for i in range(0, num):
        current_roll = random.randint(1, die)
        list_of_rolls += (str(current_roll) + '+')
        result += current_roll
    if mod == 0:
        list_of_rolls2 = list_of_rolls[:-1]
    else:
        if mod < 0:
            list_of_rolls2 = list_of_rolls[:-1] + str(mod)
        else:
            list_of_rolls2 = list_of_rolls + str(mod)
    result += mod
    string_res = '`' + list_of_rolls2 + '`'

    return result, string_res


class Dice(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True, name='r')
    async def roll(self, ctx, *args: str):
        if len(args) != 1:
            return await ctx.channel.send('Usage: .r ndn e.g. `.r 1d20` or `.r 3d6+5`\nUse .help for more information.')
        result = parse_string(args[0])
        if isinstance(result, str):
            return await ctx.channel.send(result)
        else:
            num_result, str_result = roll_die(result)
            return await ctx.channel.send(
                str(ctx.message.author).split('#')[0] + ' got: `' + str(
                    max(0, num_result)) + '`\nRolled: ' + str_result)

    @commands.command(pass_context=True, name='add')
    async def add(self, ctx, *args: str):
        message = 'Usage: .a ndn ndn e.g. `.add 1d20+6 3d6 2d4-2`\nAdds all rolls together. Use .help for more ' \
                  'information '
        if len(args) <= 1:
            return await ctx.channel.send(message)
        num_result = []
        str_result = []
        for i in range(0, len(args)):
            temp = parse_string(args[i])
            if isinstance(temp, str):
                return await ctx.channel.send(message)
            result = roll_die(temp)
            num_result.append(result[0])
            str_result.append(result[1][1:-1])
        final_string = '`'
        for x in range(0, len(str_result)):
            final_string = final_string + '+' + str_result[x]
        final_string += '`'
        if final_string.find('+') == 1:
            final_string = '`' + final_string[2:]
        return await ctx.channel.send(
            str(ctx.message.author).split('#')[0] + ' got: `' + str(
                max(0, sum(num_result))) + '`\nRolled: ' + final_string)


def setup(client):
    client.add_cog(Dice(client))
