#!/usr/bin/python3
import os
#import re
import chempy
import asyncio
import discord
import datetime
import itertools
import mendeleev
#import threading
#import wikipedia
import math, cmath
from ionize import *
from pprint import pprint
import pubchempy as pubchem
#from bs4 import BeautifulSoup
from chempy import mass_fractions
import discord_chembot.database_setup
from discord.ext import commands, tasks
from chempy import balance_stoichiometry
from discord_chembot.discord_key import *
from discord_chembot.database_setup import *
from discord_chembot.variables_for_reality import *

lookup_bot = commands.Bot(command_prefix=(COMMAND_PREFIX))
bot_help_message = "I am a beta bot, right now all you can do is \"lookup\" \
    \"element\" \"type_of_data\"."

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
async def pubchem_lookup(ctx, arg1):
    await Pubchem_lookup.validate_user_input(ctx, arg1)
    list_to_string = lambda list_to_convert: ''.join(list_to_convert)
    string_to_send = list_to_string(lookup_output_container)
    await ctx.send(string_to_send)

@lookup_bot.command()
#async def pubsearch(ctx, arg1, arg2, arg3):
#    user_input = self.validate_user_input( arg1, arg2, arg3 )
#    lookup = self.pubchem_lookup_by_name_or_CID(user_input)

# now we can just start copying code and changing it slightly to implement
# new functionality, then import the class and good to go!
###############################################################################
from discord_chembot.element_lookup_class import Element_lookup
##############################################################################
#figure out WHY this is doing and make it less ugly
def size_check_256(thing_to_check):
    if len(thing_to_check) != None and 150 < len(thing_to_check) < 256:
        return (str(txt[:100]) + "... sliced ...")
    else:
        function_failure_message(thing_to_check, "red")
##############################################################################

class Pubchem_lookup(commands.Cog):
    '''
Class to perform lookups on CID's and IUPAC names
Also does chempy translation to feed data to the calculation engine
    '''
    def __init__(self):
        self.asdf                 = ["test_init : self.asdf"]
        self,lookup_result        = ["test_init : self.lookup_result"]
        self.name_lookup_result   = None
        name_lookup_results_list  = ["test_init : self.name_lookup_results_list"] 
        greenprint("loaded pubchem_commands")
    
    def balancer_help_message():
        return " Reactants and Products are Comma Seperated Values using"+\
        "symbolic names for elements e.g. \n user input for "+\
        "reactants => NH4ClO4,Al \n user input for products "+\
        " => Al2O3,HCl,H2O,N2 "

    def lookup_help_message():
        return "input CID or IUPAC name"

    def validate_user_input(self, user_input: str):
        # haha I made a joke!
        # maybe we can feed the formula CSV to chempy directly and use the 
        # error and validation functions of chempy to determine if the 
        # user supplied good information? We can strongly reduce our own checks
        # EVERYWHERE if we validate on the input function. Don't write more 
        # code than necessary!

        # SO! Here we have fed the input to a chempy.Substance!
        try:
            test_entity1 = chempy.Substance.from_formula(user_input)
        # if it doesn't work, lets see why!
        except Exception:
            function_failure_message(Exception, "red")
        lambda hard = True : hard ; pass  

    #remove async and ctx to make non-discord
    async def send_reply(self, ctx, formatted_reply):
        reply = format_message_discord(self, ctx, formatted_reply)
        #await ctx.send(content="lol", embed=formatted_reply)
        await ctx.send(content="lol", embed=reply)

    def parse_lookup_to_chempy(pubchem_lookup : list):
        '''
        creates a chempy something or other based on what you feed it
        like cookie monster
        '''
        #lookup_cid       = pubchem_lookup[0].get('cid')
        lookup_formula   = pubchem_lookup[1].get('formula')
        #lookup_name      = pubchem_lookup[2].get('name')
        return chempy.Substance.from_formula(lookup_formula)
    
    def pubchem_lookup_by_name_or_CID(self, compound_id:str or int):
        '''
        wakka wakka wakka
        outputs in the following order:
        CID, Formula, Name
        '''
        #make a thing
        return_relationships = list
        
        #if the user supplied a name
        if isinstance(compound_id, str):
            lookup_results = pubchem.get_compounds(compound_id,'name',)
            
            #if there were multiple results
            if isinstance(lookup_results, list):
                for each in lookup_results:
                    return_relationships.append([                      \
                    {'cid'     : each.cid                        },\
                    {'formula' : each.molecular_formula          },\
                    {'name'    : each.iupac_name                 }])
                    compound_to_database(return_relationships)
            
            # if there was only one result
            elif isinstance(lookup_results, pubchem.Compound):
                return_relationships.append([                          \
                    {'cid'     : lookup_results.cid              },\
                    {'formula' : lookup_results.molecular_formula},\
                    {'name'    : lookup_results.iupac_name       }])
                compound_to_database(return_relationships)

        #if the user supplied a CID
        elif isinstance(compound_id, int):
            lookup_results = pubchem.Compound.from_cid(compound_id)
            
            #if there were multiple results
            if isinstance(lookup_results, list):
                return_relationships.append([                            \
                    {'cid'     : lookup_results.cid}                    ,\
                    {'formula' : lookup_results.molecular_formula}      ,\
                    {'name'    : lookup_results.iupac_name}             ])
                compound_to_database(return_relationships)
            #if there was only one result
            elif isinstance(lookup_results, pubchem.Compound):
                return_relationships.append([                          \
                    {'cid'     : lookup_results.cid              },\
                    {'formula' : lookup_results.molecular_formula},\
                    {'name'    : lookup_results.iupac_name       }])
                compound_to_database(return_relationships)


    def compound_to_database(lookup_list: list):
        """
        Puts a pubchem lookup to the database
        ["CID", "Formula", "Name"]
        """
        lookup_cid                 = lookup_list[0].get('cid')
        lookup_formula             = lookup_list[1].get('formula')
        lookup_name                = lookup_list[2].get('name')
        add_to_db(Compound(cid     = lookup_cid,          \
                           formula = lookup_formula,      \
                           name    = lookup_name         ))

    def composition_to_database(comp_name: str, units_used :str, \
                                formula_list : list , info : str):
        """
        The composition is a relation between multiple Compounds
        Each Composition entry will have required a pubchem_lookup on each
        Compound in the Formula field. 
        the formula is a CSV LIST WHERE: 
        ...str_compound,int_amount,.. REPEATING (floats allowed)

        """
        # query local database for records before performing pubchem
        # lookups
        for each in formula_list:
            internal_local_database_lookup(each, "formula")
            pass

        new_comp = Composition(name       = comp_name,               \
                               units      = units_used,              \
                               compounds  = formula_list,            \
                               notes      = info                     )
        add_to_db(new_comp)



    async def format_mesage_arbitrary(self, arg1, arg2, arg3):
        pass

    async def format_message_discord(self, ctx, lookup_results_object):
        formatted_message = discord.Embed( \
            title=lookup_results_object.synonyms[0],
            #change color option
            colour=discord.Colour(discord_color),  \
            url="",
            description=size_check_256(lookup_results_object.iupac_name),
            timestamp=datetime.datetime.utcfromtimestamp(1580842764))
        #formatted_message.set_image(url="https://cdn.discordapp.com/embed/avatars/0.png")
        formatted_message.set_thumbnail(    \
            url="https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{}" + \
                "/PNG?record_type=3d&image_size=small" + \
                "".format(lookup_results_object.cid))
        formatted_message.set_author(
            name="{} ({})".format(lookup_results_object.name,\
                                    lookup_results_object.cid),\
            url="https://pubchem.ncbi.nlm.nih.gov/compound/{}" + \
                "".format(lookup_results_object.cid), 
            icon_url="https://pubchem.ncbi.nlm.nih.gov/pcfe/logo/" + \
                "PubChem_logo_splash.png")
        formatted_message.add_field(
            name="Molecular Formula",
            value=lookup_results_object.molecular_formula)
        formatted_message.add_field(
            name="Molecular Weight",
            value=lookup_results_object.molecular_weight)
        formatted_message.add_field(
            name="Charge",
            value=lookup_results_object.charge)
        formatted_message.set_footer(
            text="",
            icon_url="")
        return formatted_message

################################################################################

#example from docs    
def balance_simple_equation(react, prod):
    """
    Reactants and Products are Comma Seperated Values
    using symbolic names for elements e.g. 
    user input for reactants => NH4ClO4,Al
    user input for products  => Al2O3,HCl,H2O,N2
    """
    reactants, products = chempy.balance_stoichiometry(react,prod)
    #pprint(dict(reac))
    #{'Al': 10, 'NH4ClO4': 6}
    #pprint(dict(prod))
    #{'Al2O3': 5, 'H2O': 9, 'HCl': 6, 'N2': 3}
    react =  {'NH4ClO4', 'Al'}
    prod  =  {'Al2O3', 'HCl', 'H2O', 'N2'}

    #iterates over reactants and products with the function 
    # mass_fractions(reactants)
    # mass_fractions(products)
    for fractions in map(mass_fractions, [react, prod]):
        pprint({k: '{0:.3g} wt%'.format(v*100) for k, v in fractions.items()})
    pprint([dict(_) for _ in balance_stoichiometry({'C', 'O2'}, {'CO2', 'CO'})])  # doctest: +SKIP
    #[{'C': x1 + 2, 'O2': x1 + 1}, {'CO': 2, 'CO2': x1}]
    #user input 
    user_input_reactants = "NH4ClO4,Al"
    user_input_products  = "Al2O3,HCl,H2O,N2"

    #check the DB for the reactants
    for each in user_input_reactants:
        local_db_query = internal_local_database_lookup(each, "formula")
        #it was in the database
        if local_db_query == True:
            return local_db_query
        #it was not in the database
        elif local_db_query ==False:
            function_failure_message("local db query returned NEGATIVE", "red")
            Pubchem_lookup.pubchem_lookup_by_name_or_CID(each)