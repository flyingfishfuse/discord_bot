# -*- coding: utf-8 -*-
################################################################################
## Chemical element resource database from wikipedia/mendeleev python library ##
##                             for discord bot                                ##
################################################################################
# Copyright (c) 2020 Adam Galindo                                             ##
#                                                                             ##
# Permission is hereby granted, free of charge, to any person obtaining a copy##
# of this software and associated documentation files (the "Software"),to deal##
# in the Software without restriction, including without limitation the rights##
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell   ##
# copies of the Software, and to permit persons to whom the Software is       ##
# furnished to do so, subject to the following conditions:                    ##
#                                                                             ##
# Licenced under GPLv3                                                        ##
# https://www.gnu.org/licenses/gpl-3.0.en.html                                ##
#                                                                             ##
# The above copyright notice and this permission notice shall be included in  ##
# all copies or substantial portions of the Software.                         ##
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
################################################################################
"""
Discord bot for utilizing the functions found in
  Pubchem_test.py
  database_setup.py
  element_lookup.py
  equation_balancer.py
  add_composition.py

This is a Top level file, It can be run singly as the App.

Running this file by itself will start a discord bot.


"""
################################################################################
# Imports
################################################################################
import os
import discord
import discord_key
from discord_key import *
import element_lookup_class
from element_lookup_class import Element_lookup
import pubchem_test
from pubchem_test import Pubchem_lookup
from discord.ext import commands, tasks
from equation_balancer import EquationBalancer
from variables_for_reality import lookup_output_container
from variables_for_reality import redprint,greenprint,blueprint,devs
from variables_for_reality import COMMAND_PREFIX,lookup_input_container

################################################################################
# Variables
################################################################################

lookup_bot = commands.Bot(command_prefix=(COMMAND_PREFIX))
bot_help_message = "I am a beta bot, right now all you can do is \"lookup\" \
    \"element\" \"type_of_data\"."

################################################################################
# Private functions
################################################################################

# check if the person sending the command is a developer
def dev_check(ctx):
    return str(ctx.author.id) in str(devs)

@commands.check(dev_check)
async def unload(ctx, extension):
    lookup_bot.unload_extension(f"cogs.{extension}")
    await ctx.send(f"`{extension}`" + " Unloaded !")

# WHEN STARTED, APPLY DIRECTLY TO FOREHEAD
@lookup_bot.event
async def on_ready():
    print("Science_bot ALPHA")
    await lookup_bot.change_presence(activity=discord.Game(name="Chembot - type .help"))
    #await lookup_bot.connect()

################################################################################
# Public functions
################################################################################
#HELP COMMAND
@lookup_bot.command()
async def element_lookup_usage(ctx):
    help = Element_lookup.help_message()
    await ctx.send(help)

@lookup_bot.command()
async def pubchem_lookup_usage(ctx):
    help = Pubchem_lookup.help_message()
    await ctx.send(help)

@lookup_bot.command()
async def balancer_usage(ctx):
    await ctx.send(EquationBalancer.balancer_help_message())

@lookup_bot.command()
async def bot_usage(ctx):
    await ctx.send(bot_help_message)

#even though you a dev, why should I trust you?
# give a password!
#@lookup_bot.command()
#@commands.check(dev_check)
#async def restart_bot(secret_code):
    #Restart_bot(secret_code)

#@lookup_bot.command()
#async def composition_lookup(ctx, arg1, arg2):
    # this does the thing and places the output in lookup_output_container
#   Pubchem_lookup.validate_user_input(ctx, arg1, arg2)
    #string_to_send = list_to_string(lookup_output_container)
#    await ctx.send(content="lol", embed=lookup_output_container)

#@lookup_bot.command()
#@commands.check(dev_check)
#async def composition_to_db(ctx, arg1, arg2):
    # this does the thing and places the output in lookup_output_container
#    await Pubchem_lookup.validate_user_input(ctx, arg1, arg2)
    #string_to_send = list_to_string(lookup_output_container)
#    await ctx.send(content="lol", embed=lookup_output_container)

################################################################################
# Private functions
################################################################################

@lookup_bot.command()
async def element_lookup(ctx, arg1, arg2):
    element_lookup_class.Element_lookup.validate_user_input(arg1, arg2)
    await ctx.send(lookup_output_container[0])

@lookup_bot.command()
async def pubchem_lookup(ctx, arg1, arg2):
    new_lookup = pubchem_test.Pubchem_lookup(arg1,arg2)
    pubchem_embed       =  discord.Embed()
    print(new_lookup.local_output_container)
    pubchem_embed.title =  new_lookup.local_output_container.get('iupac_name')
    pubchem_embed.add_field(name = "CID: " , value = new_lookup.local_output_container.get('cid'))
    pubchem_embed.add_field(name = "Formula"       , value = new_lookup.local_output_container.get('molecular_formula'))
    pubchem_embed.add_field(name = "Mol weight"    , value = new_lookup.local_output_container.get('molecular_weight'))
    pubchem_embed.add_field(name = "Charge"        , value = new_lookup.local_output_container.get('charge'))

    ###########################################################################
    # How to set a local file image source:
    #
    # embed = discord.Embed(title="Title", description="Desc", color=0x00ff00) #creates embed
    # file = discord.File("path/to/image/file.png", filename="image.png")
    # embed.set_image(url="attachment://image.png")
    # await ctx.send(file=file, embed=embed)
    pubchem_embed.set_image(url='data:image/png;base64,{}'.format(new_lookup.image_data))    
    await ctx.send(content="lol", embed=pubchem_embed)

@lookup_bot.command()
async def balance_equation(ctx, arg1):
    EquationBalancer.validate_formula_input(arg1)
    await ctx.send(lookup_output_container)


greenprint("[+] Loaded Discord commands")

################################################################################
# AND NOW WE RUN THE BOT!!! YAY!!! I HAVE MORE DEBUGGING TO DO!!########
from variables_for_reality import TESTING
if TESTING == True:
    lookup_bot.run(discord_key.discord_bot_token, bot=True)
else:
    try:
        if __name__ == '__main__':
            os.environ['DISCORDAPP'] = "True"
            lookup_bot.run(discord_key.discord_bot_token, bot=True)
        else:
            print("wat")
    except:
        redprint("[-] Error starting program")
################################################################################