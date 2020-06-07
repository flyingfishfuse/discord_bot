from variables_for_reality import greenprint,redprint, \
    blueprint,lookup_output_container,devs,list_to_string
from calc import EquationBalancer
from pubchem_test import Pubchem_lookup
import element_lookup_class
from element_lookup_class import Element_lookup

# setup the discord variables that need to be global
import discord
import discord_key
from discord_key import *
from discord.ext import commands, tasks
from variables_for_reality import COMMAND_PREFIX,lookup_input_container
lookup_bot = commands.Bot(command_prefix=(COMMAND_PREFIX))
bot_help_message = "I am a beta bot, right now all you can do is \"lookup\" \
    \"element\" \"type_of_data\"."

def dev_check(ctx):
    return str(ctx.author.id) in devs

#LOAD EXTENSION
#@lookup_bot.command()
#@commands.check(dev_check)
#async def load(ctx, extension):
#    lookup_bot.load_extension("cogs.{}".format(extension))
#    await ctx.send(f"'{}'".format(extension) + " Loaded !")

#UNLOAD EXTENSION
#@lookup_bot.command()
@commands.check(dev_check)
async def unload(ctx, extension):
    lookup_bot.unload_extension(f"cogs.{extension}")
    await ctx.send(f"`{extension}`" + " Unloaded !")

#RELOAD EXTENSION
#@lookup_bot.command()
@commands.check(dev_check)
async def reload(ctx, extension):
    lookup_bot.unload_extension(f"cogs.{extension}")
    lookup_bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"`{extension}`" + " Reloaded !")
lookup_bot = commands.Bot(command_prefix=(COMMAND_PREFIX))
bot_help_message = "I am a beta bot, right now all you can do is \"lookup\" \
    \"element\" \"type_of_data\"."

# check if the person sending the command is a developer
def dev_check(ctx):
    return str(ctx.author.id) in str(devs)

# WHEN STARTED, APPLY DIRECTLY TO FOREHEAD
@lookup_bot.event
async def on_ready():
    print("Science_bot ALPHA")
    await lookup_bot.change_presence(activity=discord.Game(name="Chembot - type .help"))
    #await lookup_bot.connect()

#HELP COMMAND
@lookup_bot.command()
async def element_lookup_usage(ctx):
    await ctx.send(Element_lookup.help_message())

@lookup_bot.command()
async def pubchem_lookup_usage(ctx):
    await ctx.send(Pubchem_lookup.help_message())

@lookup_bot.command()
async def balancer_usage(ctx):
    await ctx.send(Pubchem_lookup.balancer_help_message())

@lookup_bot.command()
async def bot_usage(ctx):
    await ctx.send(bot_help_message)

#even though you a dev, why should I trust you?
# give a password!
#@lookup_bot.command()
#@commands.check(dev_check)
#async def restart_bot(secret_code):
    #Restart_bot(secret_code)

@lookup_bot.command()
async def element_lookup(ctx, arg1, arg2):
    await element_lookup_class.Element_lookup.validate_user_input(ctx, arg1, arg2)
    #print( list_to_string(lookup_output_container))
    #string_to_send = list_to_string(lookup_output_container)
    await ctx.send(lookup_output_container)

@lookup_bot.command()
async def pubchem_lookup(ctx, arg1, arg2):
    await Pubchem_lookup.validate_user_input(ctx, arg1, arg2)
    #string_to_send = list_to_string(lookup_output_container)
    await ctx.send(content="lol", embed=lookup_output_container)

@lookup_bot.command()
async def composition_lookup(ctx, arg1, arg2):
    await Pubchem_lookup.validate_user_input(ctx, arg1, arg2)
    #string_to_send = list_to_string(lookup_output_container)
    await ctx.send(content="lol", embed=lookup_output_container)

@lookup_bot.command()
@commands.check(dev_check)
async def composition_to_db(ctx, arg1, arg2):
    await Pubchem_lookup.validate_user_input(ctx, arg1, arg2)
    #string_to_send = list_to_string(lookup_output_container)
    await ctx.send(content="lol", embed=lookup_output_container)

@lookup_bot.command()
async def balance_equation(ctx, arg1):
    await EquationBalancer.validate_formula_input(ctx, arg1)
    string_to_send = list_to_string(lookup_output_container)
    #await ctx.send(content="lol", embed=lookup_output_container[0])
    await ctx.send(string_to_send)

@lookup_bot.command()
async def LC_circuit(ctx, inductance, capacitance, voltage, current_bool,series_bool, parallel_bool):
    await LC_circuit(ctx, inductance, capacitance, voltage, current_bool,series_bool, parallel_bool)
    #string_to_send = list_to_string(lookup_output_container)
    await ctx.send(content="lol", embed=lookup_output_container[0])
################################################################################

######## AND NOW WE RUN THE BOT!!! YAY!!! I HAVE MORE DEBUGGING TO DO!!########
lookup_bot.run(discord_key.discord_bot_token, bot=True)
