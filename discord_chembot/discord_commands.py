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
lookup_bot = commands.Bot(command_prefix=(COMMAND_PREFIX))
bot_help_message = "I am a beta bot, right now all you can do is \"lookup\" \
    \"element\" \"type_of_data\"."

# check if the person sending the command is a developer
def dev_check(ctx):
    return str(ctx.author.id) in str(devs)

@commands.check(dev_check)
async def unload(ctx, extension):
    lookup_bot.unload_extension(f"cogs.{extension}")
    await ctx.send(f"`{extension}`" + " Unloaded !")

lookup_bot = commands.Bot(command_prefix=(COMMAND_PREFIX))
bot_help_message = "I am a beta bot, right now all you can do is \"lookup\" \
    \"element\" \"type_of_data\"."

# WHEN STARTED, APPLY DIRECTLY TO FOREHEAD
@lookup_bot.event
async def on_ready():
    print("Science_bot ALPHA")
    await lookup_bot.change_presence(activity=discord.Game(name="Chembot - type .help"))
    #await lookup_bot.connect()

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
    # this does the thing and places the output in lookup_output_container
    Pubchem_lookup.validate_user_input(arg1, arg2)
    #string_to_send = list_to_string(lookup_output_container)
    ##########################################################################
    # DO STUFF HERE TO create the discord.Embed object
    # lookup_output_container is holding the local lookup from the DB
    # it's already done the remote lookup and stored the result
    ##########################################################################


    await ctx.send(content="lol", embed=lookup_output_container)

@lookup_bot.command()
async def balance_equation(ctx, arg1):
    # this does the thing and places the output in lookup_output_container
    EquationBalancer.validate_formula_input(ctx, arg1)
    #string_to_send = list_to_string(lookup_output_container)
    ##########################################################################
    # DO STUFF HERE TO create the discord.Embed object
    ##########################################################################
    
    await ctx.send(content="lol", embed=lookup_output_container[0])
    #await ctx.send(string_to_send)


######## AND NOW WE RUN THE BOT!!! YAY!!! I HAVE MORE DEBUGGING TO DO!!########
lookup_bot.run(discord_key.discord_bot_token, bot=True)





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


