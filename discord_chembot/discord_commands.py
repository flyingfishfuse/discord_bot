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
  Pubchem_lookup.py
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
from variables_for_reality import greenprint,redprint, \
    blueprint,lookup_output_container,devs,list_to_string
from equation_balancer import EquationBalancer
from pubchem_test import Pubchem_lookup
import element_lookup_class
from element_lookup_class import Element_lookup

# setup the discord variables that need to be global
import discord
import discord_key
from discord_key import *
from discord.ext import commands, tasks
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

################################################################################
# Private functions
################################################################################

@lookup_bot.command()
async def element_lookup(ctx, arg1, arg2):
    element_lookup_class.Element_lookup.validate_user_input(arg1, arg2)
    await ctx.send(lookup_output_container[0])

@lookup_bot.command()
async def pubchem_lookup(ctx, arg1, arg2):
    Pubchem_lookup.validate_user_input(arg1, arg2)
    #lookup_output_container[0].cid
    #lookup_output_container[0].molecular_formula
    #lookup_output_container[0].molecular_weight
    #lookup_output_container[0].charge
    #lookup_output_container[0].iupac_name
    pubchem_embed       = discord.Embed()
    pubchem_embed.title =  lookup_output_container[0].iupac_name
    pubchem_embed.add_field(name = "CID"           , value = lookup_output_container[0].cid)
    pubchem_embed.add_field(name = "Formula"       , value = lookup_output_container[0].molecular_formula)
    pubchem_embed.add_field(name = "Mol weight"    , value = lookup_output_container[0].molecular_weight)
    pubchem_embed.add_field(name = "Charge"        , value = lookup_output_container[0].charge)
    pubchem_embed.add_field(name = "Visualization" , value = lookup_output_container[0].image_data)
    #await ctx.send(str(lookup_output_container[0]))
    await ctx.send(content="lol", embed=pubchem_embed)

@lookup_bot.command()
async def balance_equation(ctx, arg1):
    EquationBalancer.validate_formula_input(arg1)
    await ctx.send(lookup_output_container)

################################################################################
# AND NOW WE RUN THE BOT!!! YAY!!! I HAVE MORE DEBUGGING TO DO!!########
lookup_bot.run(discord_key.discord_bot_token, bot=True)
################################################################################





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


