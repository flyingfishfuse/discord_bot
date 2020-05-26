#!/usr/bin/python3
import os
#import re
import chempy
import asyncio
import discord
import datetime
import itertools
import mendeleev
import threading
import wikipedia
import math, cmath
from ionize import *
from discord_chembot.discord_key import *
import pubchempy as pubchem
#from bs4 import BeautifulSoup
from discord.ext import commands, tasks
from discord.ext import commands
from discord_chembot.database_setup import *
from discord_chembot.variables_for_reality import *

lookup_bot = commands.Bot(command_prefix=(COMMAND_PREFIX))
bot_help_message = "I am a beta bot, right now all you can do is \"lookup\" \
    \"element\" \"type_of_data\"."

def function_failure_message(exception_message):
        import inspect
        return "something wierd happened in: " + inspect.currentframe().f_code.co_name + \
            "\n" + exception_message

# GLOBAL OUTPUT CONTAINER FOR FINAL CHECKS
global global_output_container 
global_output_container = []

global lookup_output_container
lookup_output_container = []

#load the cogs into the bot
if load_cogs == True:
    for filename in cog_directory_files:
        if filename.endswith(".py"):
            lookup_bot.load_extension(f"cogs.{filename[:-3]}")

# check if the person sending the command is a developer
def dev_check(ctx):
    return str(ctx.author.id) in str(devs)

#LOAD EXTENSION
@lookup_bot.command()
@commands.check(dev_check)
async def load(ctx, extension):
    lookup_bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"`{extension}`" + " Loaded !")

#UNLOAD EXTENSION
@lookup_bot.command()
@commands.check(dev_check)
async def unload(ctx, extension):
    lookup_bot.unload_extension(f"cogs.{extension}")
    await ctx.send(f"`{extension}`" + " Unloaded !")

#RELOAD EXTENSION
@lookup_bot.command()
@commands.check(dev_check)
async def reload(ctx, extension):
    lookup_bot.unload_extension(f"cogs.{extension}")
    lookup_bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"`{extension}`" + " Reloaded !")

# WHEN STARTED, APPLY DIRECTLY TO FOREHEAD
@lookup_bot.event
async def on_ready():
    print("Element_properties_lookup_tool")
    await lookup_bot.change_presence(activity=discord.Game(name="THIS IS BETA !"))

#HELP COMMAND
@lookup_bot.command()
async def lookup_usage(ctx):
    await ctx.send(await Element_lookup.help_message())

@lookup_bot.command()
async def bot_usage(ctx):
    await ctx.send(bot_help_message)

@lookup_bot.command()
async def mendel_lookup(ctx, arg1, arg2):
    await Element_lookup.validate_user_input(ctx, arg1, arg2)
    #await Element_lookup.format_and_print_output(lookup_output_container)
    #await ctx.send(lookup_output_container)
    list_to_string = lambda list_to_convert: ''.join(list_to_convert)
    string_to_send = list_to_string(lookup_output_container)
    await ctx.send(string_to_send)

@lookup_bot.command()
async def pubchem_lookup(ctx, arg1, arg2):
    await Pubchem_lookup.validate_user_input(ctx, arg1)
    #await Element_lookup.format_and_print_output(lookup_output_container)
    #await ctx.send(lookup_output_container)
    list_to_string = lambda list_to_convert: ''.join(list_to_convert)
    string_to_send = list_to_string(lookup_output_container)
    await ctx.send(string_to_send)

# now we can just start copying code and changing it slightly to implement
# new functionality, then import the class and good to go!
###############################################################################
from discord_chembot.element_lookup_class import Element_lookup
##############################################################################
#figure out WHY this is doing and make it less ugly
def size_check_256(txt):
    if txt == None:
        return "iupac name Not Found"
    # print(len(txt))
    elif len(txt) < 255:
        return txt
    else:
        short = (str(txt[:100])+ " .....")
        return short
##############################################################################

class Pubchem_lookup(commands.Cog):

    def __init__(self):
        self.asdf = []
        self.name_lookup_result = None
        print("loaded pubchem_commands")
        name_lookup_results_list = [] 

    def pubchem_lookup_by_name_or_CID(compound_id:str or int):
        if isinstance(compound_id, str):
            name_lookup_results_list = pubchem.get_compounds(compound_id,\
                                        'name' , \
                                        list_return='flat')
        elif isinstance(compound_id, int):
            self.name_lookup_result = pubchem.Compound.from_cid(compound_id)

##############################################################################

def parse_lookup_to_chempy(pubchem_lookup : list):
    lookup_cid = chempy.Substance.from_formula(pubchem_lookup[1].get('cid'))
    lookup_formula = chempy.Substance.from_formula(pubchem_lookup[1].get('formula'))
    lookup_name = chempy.Substance.from_formula(pubchem_lookup[1].get('name'))
    return chempy.Substance.from_formula(lookup_formula)

def pubchem_lookup_by_name_or_CID(compound_id:str or int):
    '''
    
    lookup_cid = chempy.Substance.from_formula(asdf[1].get('cid')
    lookup_formula = chempy.Substance.from_formula(asdf[1].get('formula')
    lookup_name = chempy.Substance.from_formula(asdf[1].get('name')
    '''
    return_relationships = list
    if isinstance(compound_id, str):
        lookup_results = pubchem.get_compounds(compound_id,'name',\
                                                list_return='flat')
        if isinstance(lookup_results, list):
            for each in lookup_results:
                return_relationships.append([                \
                    {'cid'     : each.cid}                  ,\
                    {'formula' : each.molecular_formula}    ,\
                    {'name'    : each.iupac_name}           ])
        else:
            return_relationships.append(lookup_results)

        return return_relationships
    elif isinstance(compound_id, int):
        lookup_results = pubchem.Compound.from_cid(compound_id)
        return_relationships.append([                       \
            {'cid'     : lookup_results.cid}               ,\
            {'formula' : lookup_results.molecular_formula} ,\
            {'name'    : lookup_results.iupac_name}        ])
        return return_relationships
##############################################################################

    def validate_user_input(user_input: str):
        lambda hard: hard ; pass  
##############################################################################

    async def send_reply(self, ctx, formatted_reply):
        await message.edit(content="lol", embed=formatted_reply)
##############################################################################

    
    async def format_message(self, ctx, lookup_results_object):
        formatted_message = discord.Embed( \
            title=lookup_results_object.synonyms[0],
            #change color option
            colour=discord.Colour(discord_color),  \
            url="",
            description=size_check_256(lookup_results_object.iupac_name),
            timestamp=datetime.datetime.utcfromtimestamp(1580842764))
        #formatted_message.set_image(url="https://cdn.discordapp.com/embed/avatars/0.png")
        formatted_message.set_thumbnail(url="https://pubchem.ncbi.nlm.nih.gov/" + \
                "rest/pug/compound/cid/{1}/PNG?record_type=3d&image_size=small" + \
                "".format(lookup_results_object.cid))
        formatted_message.set_author(
            name="{1} ({2})".format(lookup_results_object.name, lookup_results_object.cid),
            url=f"https://pubchem.ncbi.nlm.nih.gov/compound/{lookup_results_object.cid}", 
            icon_url="https://pubchem.ncbi.nlm.nih.gov/pcfe/logo/PubChem_logo_splash.png"
            )
        formatted_message.add_field(
            name="Molecular Formula",
            value=lookup_results_object.molecular_formula
            )
        formatted_message.add_field(
            name="Molecular Weight",
            value=lookup_results_object.molecular_weight
            )
        formatted_message.add_field(
            name="Charge",
            value=lookup_results_object.charge
            )
        formatted_message.set_footer(
            text="",
            icon_url=""
            )
##############################################################################

    @commands.command()
    async def pubsearch(self, ctx, arg1, arg2, arg3):
        user_input = self.validate_user_input( arg1, arg2, arg3 )
        lookup = self.pubchem_lookup_by_name_or_CID(user_input)
        #if len(lookup) >= 25:
        #    await message.edit(content="")
        #    return
        results =[pubchem.Compound.from_cid(cid) for cid in cidsRes]
        if len(results) >= 9:
            await ctx.message.edit(content=f"Your result is >9 ({len(results)}), trimming...")
            results = results[:9]
        else:
            if len(results) >= 25:
                pass
            await ctx.message.edit(content=f"Processing your {len(results)} results...")
        #results = pcp.get_compounds(cmp, 'name')
 
        #if there are no results, print text below
        if not results: 
            await ctx.message.edit(content=f"0 results for {cmp}")
            return

        #makes one big string, if there are too many results say that aswell
        results_str = ""
        results_ammount = 0
        for i in results:
            results_ammount += 1
            name = "Synonym not found"
            if len(i.synonyms) > 0:
                name = i.synonyms[0]
            results_str = results_str + f"{discord_numbers.get(results_ammount)} {name} \n"
            if len(results_str) >= 1900:
                await ctx.message.edit(content="Cannot show list, reply longer than 1900 characters")
            return
        # edit the message and show results
        await message.edit(content=results_str)
            # cmpdataz = pcp.get_compounds(record_type='3d')
            #lookup_results.name = "Synonym not found"




