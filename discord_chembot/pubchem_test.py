#!/usr/bin/python3
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
####
################################################################################
##    Search by element number, symbol,
##    list resources available
##    TODO: show basic info if no specificity in query
# created by : mr_hai on discord / flyingfishfuse on github
## Test/Personal Server : https://discord.gg/95V7Mn
#list_of_resources = "https://en.wikipedia.org/wiki/List_of_data_references_for_chemical_elements"
#data_pages_list   = "https://en.wikipedia.org/wiki/Category:Chemical_element_data_pages"
# https://chemspipy.readthedocs.io/en/latest/
import os
import re
import chempy
import ionize
import asyncio
import discord
import datetime
import itertools
import mendeleev
#import threading
#import wikipedia
import math, cmath
from pprint import pprint
import pubchempy as pubchem
#from bs4 import BeautifulSoup
from chempy import mass_fractions
#import discord_chembot.database_setup
from discord.ext import commands, tasks
#from chempy import balance_stoichiometry
#from discord_chembot.discord_key import *
#from discord_chembot.database_setup import *
#from discord_chembot.discord_commands import *
#from discord_chembot.element_lookup_class import Element_lookup
#from discord_chembot.variables_for_reality import greenprint,redprint,blueprint
#from discord_chembot.variables_for_reality import show_line_number,cas_regex
#pretend main file, move contents to properties_lookup.py
import database_setup
from chempy import balance_stoichiometry
from discord_key import *
from database_setup import *
from variables_for_reality import *
#from discord_chembot.discord_commands import *
#from element_lookup_class import Element_lookup
#from variables_for_reality import greenprint,redprint,blueprint
#from variables_for_reality import show_line_number,cas_regex
#make them global scope for testing purposes
show_line_number = lambda line: blueprint('line:' + inspect.getframeinfo(inspect.currentframe()).lineno)
blueprint = lambda text: print(Fore.BLUE + ' ' +  text + ' ' + Style.RESET_ALL)
greenprint = lambda text: print(Fore.GREEN + ' ' +  text + ' ' + Style.RESET_ALL)
redprint = lambda text: print(Fore.RED + ' ' +  text + ' ' + Style.RESET_ALL)


# setup the discord variables that need to be global
from discord.ext import commands
lookup_bot = commands.Bot(command_prefix=(COMMAND_PREFIX))
bot_help_message = "I am a beta bot, right now all you can do is \"lookup\" \
    \"element\" \"type_of_data\"."

# GLOBAL OUTPUT CONTAINER FOR FINAL CHECKS
global lookup_output_container 
lookup_output_container = []

# GLOBAL INPUT CONTAINER FOR USER INPUT VALIDATION
global lookup_input_container
lookup_input_container = []

#load the cogs into the bot
cog_directory_files = os.listdir("./")
if load_cogs == True:
    for filename in cog_directory_files:
        if filename.endswith(".py"):
            lookup_bot.load_extension("cogs.{}".format(filename[:-3]))
# check if the person sending the command is a developer
def dev_check(ctx):
    return str(ctx.author.id) in str(devs)

#LOAD EXTENSION
@lookup_bot.command()
#@commands.check(dev_check)
#async def load(ctx, extension):
#    lookup_bot.load_extension("cogs.{}".format(extension))
#    await ctx.send(f"'{}'".format(extension) + " Loaded !")

#UNLOAD EXTENSION
#@lookup_bot.command()
#@commands.check(dev_check)
#async def unload(ctx, extension):
#    lookup_bot.unload_extension(f"cogs.{extension}")
#    await ctx.send(f"`{extension}`" + " Unloaded !")

#RELOAD EXTENSION
#@lookup_bot.command()
#@commands.check(dev_check)
#async def reload(ctx, extension):
#    lookup_bot.unload_extension(f"cogs.{extension}")
#    lookup_bot.load_extension(f"cogs.{extension}")
#    await ctx.send(f"`{extension}`" + " Reloaded !")
    #LOAD EXTENSION

#@lookup_bot.command()
#@commands.check(dev_check)
#async def load(ctx, extension):
#    lookup_bot.load_extension("cogs.{}".format(extension))
#    await ctx.send("'{}'".format(extension) + " Loaded !")

#UNLOAD EXTENSION
#@lookup_bot.command()
#@commands.check(dev_check)
#async def unload(ctx, extension):
#    lookup_bot.unload_extension(f"cogs.{extension}")
#    await ctx.send(f"`{extension}`" + " Unloaded !")

#RELOAD EXTENSION
#@lookup_bot.command()
#@commands.check(dev_check)
#async def reload(ctx, extension):
#    lookup_bot.unload_extension(f"cogs.{extension}")
#    lookup_bot.load_extension(f"cogs.{extension}")
#    await ctx.send(f"`{extension}`" + " Reloaded !")

# WHEN STARTED, APPLY DIRECTLY TO FOREHEAD
@lookup_bot.event
async def on_ready():
    print("Element_properties_lookup_tool")
    await lookup_bot.change_presence(activity=discord.Game(name="Chembot - type .help"))

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
@lookup_bot.command()
async def restart_bot(secret_code):
    Restart_bot(secret_code)

@lookup_bot.command()
async def element_lookup(ctx, arg1, arg2):
    await Element_lookup.validate_user_input(ctx, arg1, arg2)
    #await Element_lookup.format_and_print_output(lookup_output_container)
    #await ctx.send(lookup_output_container)
    list_to_string = lambda list_to_convert: ''.join(list_to_convert)
    string_to_send = list_to_string(lookup_output_container)
    await ctx.send(string_to_send)

@lookup_bot.command()
async def pubchem_lookup(ctx, arg1, arg2):
    await Pubchem_lookup.validate_user_input(ctx, arg1, arg2)
    #list_to_string = lambda list_to_convert: ''.join(list_to_convert)
    #string_to_send = list_to_string(lookup_output_container)
    #await ctx.send(string_to_send)
    
    # The lookup_output_container can be used to store objects!    
    #await ctx.send(content="lol", embed=formatted_reply_object)
    #redprint(lookup_output_container[0])
    await ctx.send(content="lol", embed=lookup_output_container[0])

#@lookup_bot.command()
#async def pubsearch(ctx, arg1, arg2, arg3):
#    user_input = Pubchem_lookup.validate_user_input( arg1, arg2, arg3 )
#    lookup = Pubchem_lookup.pubchem_lookup_by_name_or_CID(user_input)

# now we can just start copying code and changing it slightly to implement
# new functionality

##############################################################################
##############################################################################
#figure out WHY this is doing and make it less ugly
def size_check_256(thing_to_check):
    if len(thing_to_check) != None and 150 < len(thing_to_check) < 256:
        return (str(thing_to_check[:100]) + "... sliced ...")
    else:
        function_message(thing_to_check, "red")
##############################################################################
class RestartBot():

    pass

class Pubchem_lookup():
    '''
Class to perform lookups on CID's and IUPAC names
Also does chempy translation to feed data to the calculation engine
    '''
    def __init__(self):
        self.asdf                 = ["test_init : self.asdf"]
        self.lookup_result        = ["test_init : self.lookup_result"]
        self.name_lookup_result   = None
        name_lookup_results_list  = ["test_init : self.name_lookup_results_list"] 
        greenprint("loaded pubchem_commands")
    
    def balancer_help_message():
        return " Reactants and Products are Comma Seperated Values using"+\
        "symbolic names for elements e.g. \n "        +\
        "user input for reactants => NH4ClO4,Al \n"   +\
        "user input for products  => Al2O3,HCl,H2O,N2 \n"

    def help_message():
        return """
input CID/CAS or IUPAC name or synonym
Provide a search term and "term type", term types are "cas" , "name" , "cid"
Example 1 : .pubchemlookup methanol name
Example 2 : .pubchemlookup 3520 cid
Example 3 : .pubchemlookup 113-00-8 cas
"""
###############################################################################
    def send_lookup_to_output(message):
        '''
    Takes a list or string, if list, joins the list to a string and assigns to 
    lookup_output_container.
        ''' 
        # yeah yeah yeah, we are swapping between array and string like a fool
        # but it serves a purpose. Need to keep the output as an iterable
        # until the very last second when we send it to the user.
        #We want to be able to allow the developer to just send a list
        # or string to the output when adding new functions instead of
        # having to pay attention to too much stuff!
        list_to_string = lambda list_to_convert: ''.join(list_to_convert)
        if isinstance(message,list):
            message = list_to_string(message) 
        temp_array = [message]
        #global lookup_output_container
        lookup_output_container = temp_array 

    #remove async and ctx to make non-discord
    #async def send_reply(self, formatted_reply_object):
    #    reply = format_message_discord(self, formatted_reply)
    #    await ctx.send(content="lol", embed=formatted_reply_object)
    #    await ctx.send(content="lol", embed=reply)

###############################################################################
    def parse_lookup_to_chempy(pubchem_lookup : list):
        '''
        creates a chempy something or other based on what you feed it
        like cookie monster
        '''
        #lookup_cid       = pubchem_lookup[0].get('cid')
        lookup_formula   = pubchem_lookup[1].get('formula')
        #lookup_name      = pubchem_lookup[2].get('name')
        try:
            greenprint(chempy.Substance.from_formula(lookup_formula))
        except Exception:
            function_message(asdf, "blue")
###############################################################################

    def user_input_was_wrong(type_of_pebkac_failure : str, bad_string = str):
        """
        You can put something funny here!
            This is something the creator of the bot needs to modify to suit
            Thier community.
        """
        greenprint(inspect.stack()[1][3])

        user_is_a_doofus_CID_message = \
            'Stop being a doofus! Accepted types are "name","cas" or "cid" '
        user_is_a_doofus_formula_message = \
            "Stop being a doofus and feed me a good formula!"
        user_is_a_doofus_form_react_message = \
            "the following input was invalid: " + bad_string 
        user_is_a_doofus_form_prod_message = \
            "the following input was invalid: " + bad_string
        user_is_a_doofus_form_gen_message = \
            "the following input was invalid: " + bad_string
        if type_of_pebkac_failure   == "pubchem_lookup_by_name_or_CID":
            Pubchem_lookup.reply_to_query(user_is_a_doofus_CID_message)
        elif type_of_pebkac_failure == "specifics":
            Pubchem_lookup.reply_to_query(user_is_a_doofus_formula_message)
        elif type_of_pebkac_failure == "formula_reactants":
            Pubchem_lookup.reply_to_query(user_is_a_doofus_form_react_message)
        elif type_of_pebkac_failure == "formula_products":
            Pubchem_lookup.reply_to_query(user_is_a_doofus_form_prod_message)
        else:
            #change this to sonething reasonable
            Element_lookup.reply_to_query(type_of_pebkac_failure)

    def lookup_failure(type_of_failure: str):
        """
        does what it says on the label, called when a lookup is failed
        """
        greenprint(inspect.stack()[1][3])

        #TODO: find sqlalchemy exception object
        # why cant I find the type of object I need fuck me
        if type_of_failure == "SQL":
            ##global lookup_output_container
            lookup_output_container = ["SQL QUERY FAILURE"]
        elif type_of_failure == pubchem.PubChemPyError:
            ##global lookup_output_container
            lookup_output_container = ["chempy failure"]
        pass
    
    async def validate_user_input(ctx, user_input: str, type_of_input:str):
        """
    User Input is expected to be the proper identifier.
        only one input, we are retrieving one record for one entity
    
    Remove self and async from the code to transition to non-discord
        """
        import re
        cas_regex = re.compile('[1-9]{1}[0-9]{1,5}-\d{2}-\d')
        temp_output_container = []
        input_types_requestable = ["name", "cid", "cas"]
        for each in input_types_requestable:
            if type_of_input == each:
                greenprint("user supplied a : " + type_of_input)
                try:
                    if type_of_input == "cas":
                        try:
                            greenprint("[+} trying to match regular expression for CAS")
                            if re.match(cas_regex,user_input):
                                greenprint("[+] Good CAS Number")
                                await Pubchem_lookup.lookup_from_inputs(ctx, user_input, type_of_input)
                            else:
                                database_setup.function_message("[-] Bad CAS Number ","validation CAS lookup checks", "red")                    
                        except Exception:
                            database_setup.function_message('[-] Something happened in the try/except block for cas numbers','', 'red')
                    else:
                        await Pubchem_lookup.lookup_from_inputs(ctx, user_input, type_of_input)
                except Exception:
                    database_setup.function_message(Exception, " reached the exception", "red") 
            else:
                user_input_was_wrong("user_input_identification")

    async def lookup_from_inputs(ctx, user_input: str, type_of_input: str):
        '''
        function to lookup and send to output after validation is performed on inputs
        '''
        temp_output_container = []
        blueprint("[+] attempting internal lookup")
        try:
            internal_lookup = database_setup.Database_functions.internal_local_database_lookup(user_input, type_of_input)
            if internal_lookup == None:
                redprint("[-] Internal Lookup returned false")
                blueprint("[+] Attempting pubchem search")
                lookup_object = Pubchem_lookup.pubchem_lookup_by_name_or_CID(user_input, type_of_input)
                #formatted_message = Pubchem_lookup.format_message_discord(ctx, lookup_object)
                await Pubchem_lookup.format_message_discord(ctx, lookup_object)
                #temp_output_container.append([formatted_message])
                #temp_output_container.append([Pubchem_lookup.format_message_discord(ctx, lookup_object)])
                #global lookup_output_container
                #lookup_output_container = temp_output_container
            elif internal_lookup == True:
                greenprint("============Internal Lookup returned TRUE===========")
                await Pubchem_lookup.format_message_discord(ctx, lookup_object)
                #formatted_message = Pubchem_lookup.format_message_discord(ctx, internal_lookup)
                #await temp_output_container.append(Pubchem_lookup.format_message_discord(ctx, internal_lookup))
                #global lookup_output_container
                #lookup_output_container = temp_output_container
                database_setup.dump_db()
            else:
                database_setup.function_message("[-] Something is wrong with the database", "red")
        except Exception:
            database_setup.function_message(Exception, "blue")

###############################################################################
    def validate_formula_input(equation_user_input : str):
        """
        :param formula_input: comma seperated values of element symbols
        :type formula_input: str     
    makes sure the formula supplied to the code is valid
    user input will be valid only in the form of:
    eq = "NH4ClO4,Al => Al2O3,HCl,H2O,N2"
    note the two spaces
        """
        #user_input_reactants = "NH4ClO4,Al"
        #user_input_products  = "Al2O3,HCl,H2O,N2"
        #equation_user_input  = "NH4ClO4,Al=>Al2O3,HCl,H2O,N2"

        # if it doesn't work, lets see why!
        try:
            # validate equation formatting
            parsed_equation = equation_user_input.split(" => ")
            try:
                #validate reactants formatting
                user_input_reactants = str.split(parsed_equation[0], sep =",")
            except Exception:
                function_message("reactants formatting",Exception , "red")
                Pubchem_lookup.user_input_was_wrong("formula_reactants", user_input_reactants)                
            try:
                #validate products formatting
                user_input_products  = str.split(parsed_equation[1], sep =",")
            except Exception:
                function_message("products formatting",Exception , "red")
                Pubchem_lookup.user_input_was_wrong("formula_products", user_input_products)  
                #validate reactants contents
            for each in user_input_reactants:
                try:
                    validation_check = chempy.Substance(each)
                except Exception:
                    function_message("reactants contents",Exception , "red")
                    Pubchem_lookup.user_input_was_wrong("formula_reactants", each)  
                #validate products contents
            for each in user_input_products:
                try:
                    validation_check = chempy.Substance(each)
                except Exception:
                    function_message("products contents",Exception , "red")
                    Pubchem_lookup.user_input_was_wrong("formula_products", each)
        # if the inputs passed all the checks
        # RETURN THE REACTANTS AND THE PRODUCTS AS A LIST
        # [ [reactants] , [products] ]
            return [user_input_reactants, user_input_products]
        except Exception:
            function_message("formula validation exception", Exception, "red")
            Pubchem_lookup.user_input_was_wrong("formula_general", equation_user_input)
        
###############################################################################    
    def pubchem_lookup_by_name_or_CID(compound_id, type_of_data:str):
        '''
        Provide a search term and record type
        requests can be CAS,CID,IUPAC NAME/SYNONYM

        outputs in the following order:
        CID, CAS, SMILES, Formula, Name

        Stores lookup in database if lookup is valid
        I know it looks like it can be refactored into a smaller block 
        but they actually require slightly different code for each lookup
        and making a special function to do that would be just as long probably
        I'll look at it
        TODO: SEARCH LOCAL BY CAS!!!!
        '''
        #make a thing
        return_relationships = []
        #TODO : this is so hackish , fix this shit
        # you get multiple records retirned from a pubchem search VERY often
        # so you have to choose the best one to store, This needs to be 
        # presented as an option to the user,and not programmatically 
        # applied as the limiting factor in accuracy here is pubchem's
        # humans performing the input. To overcome we must use our human's
        # ability to THINK... DEAR LORD WE ARE ALL DOOMED!
        return_index = 0
        ###################################
        #if the user supplied a name
        ###################################
        if type_of_data == "name":
            try:
                greenprint("[+] Performing Pubchem Query")
                lookup_results = pubchem.get_compounds(compound_id,'name')
            except Exception :# pubchem.PubChemPyError:
                function_message("lookup by NAME exception - name", Exception, "red")
                user_input_was_wrong("pubchem_lookup_by_name_or_CID")
            #if there were multiple results
            # TODO: we have to figure out a good way to store the extra results
                   #as possibly a side record
            if isinstance(lookup_results, list):
                greenprint("[+] Multiple results returned ")
                for each in lookup_results:
                    redprint(each.molecular_formula)
                    asdf = [{'cid'      : each.cid                ,\
                            #dis bitch dont have a CAS NUMBER!
                            #'cas'      : each.cas                 ,\
                            'smiles'    : each.isomeric_smiles     ,\
                            'formula'   : each.molecular_formula   ,\
                            'molweight' : each.molecular_weight    ,\
                            'charge'    : each.charge              ,\
                            'name'      : each.iupac_name          }]
                    return_relationships.append(asdf)
                    ####################################################
                    #Right here we need to find a way to store multiple records
                    # and determine the best record to store as the main entry
                    ####################################################
                    #compound_to_database() TAKES A LIST
                    # first element of first element
                    #[ [this thing here] , [not this one] ]
                    redprint("=========RETURN RELATIONSHIPS=======")
                    blueprint(str(return_relationships[return_index]))
                    redprint("=========RETURN RELATIONSHIPS=======")
                    Pubchem_lookup.compound_to_database(return_relationships[return_index])
            
            # if there was only one result
            elif isinstance(lookup_results, pubchem.Compound):
                asdf = [{'cid'      : each.cid                ,\
                            #dis bitch dont have a CAS NUMBER!
                            #'cas'      : each.cas                 ,\
                            'smiles'    : each.isomeric_smiles     ,\
                            'formula'   : each.molecular_formula   ,\
                            'molweight' : each.molecular_weight    ,\
                            'charge'    : each.charge              ,\
                            'name'      : each.iupac_name          }]
                return_relationships.append(asdf)
                redprint("=========RETURN RELATIONSHIPS=======")
                blueprint(str(return_relationships[return_index]))
                redprint("=========RETURN RELATIONSHIPS=======")
                Pubchem_lookup.Database_functions.compound_to_database(return_relationships[return_index])

        ###################################
        #if the user supplied a CID
        ###################################
        elif type_of_data == "cid":
        #elif isinstance(compound_id, int):
            try:
                greenprint("[+] Performing Pubchem Query")
                lookup_results = pubchem.Compound.from_cid(compound_id)
            except Exception :# pubchem.PubChemPyError:
                function_message("lookup by cid exception - cid", Exception, "red")
                #if there were multiple results
                # TODO: we have to figure out a good way to store the extra results
                   #as possibly a side record
            if isinstance(lookup_results, list):
                greenprint("[+] Multiple results returned ")
                for each in lookup_results:
                    redprint(each.molecular_formula)
                    asdf = [{'cid'      : each.cid                ,\
                            #dis bitch dont have a CAS NUMBER!
                            #'cas'      : each.cas                 ,\
                            'smiles'    : each.isomeric_smiles     ,\
                            'formula'   : each.molecular_formula   ,\
                            'molweight' : each.molecular_weight    ,\
                            'charge'    : each.charge              ,\
                            'name'      : each.iupac_name          }]
                    return_relationships.append(asdf)
            ####################################################
            #Right here we need to find a way to store multiple records
            # and determine the best record to store as the main entry
            ####################################################
                    #compound_to_database() TAKES A LIST
                    # first element of first element
                    #[ [this thing here] , [not this one] ]
                redprint("=========RETURN RELATIONSHIPS=======")
                blueprint(str(return_relationships[return_index]))
                redprint("=========RETURN RELATIONSHIPS=======")
                Pubchem_lookup.compound_to_database(return_relationships[return_index])

            #if there was only one result
            elif isinstance(lookup_results, pubchem.Compound):
                asdf = [{'cid'      : each.cid                ,\
                            #dis bitch dont have a CAS NUMBER!
                            #'cas'      : each.cas                 ,\
                            'smiles'    : each.isomeric_smiles     ,\
                            'formula'   : each.molecular_formula   ,\
                            'molweight' : each.molecular_weight    ,\
                            'charge'    : each.charge              ,\
                            'name'      : each.iupac_name          }]
                return_relationships.append(asdf)
                redprint("=========RETURN RELATIONSHIPS=======")
                blueprint(str(return_relationships[return_index]))
                redprint("=========RETURN RELATIONSHIPS=======")
                Pubchem_lookup.compound_to_database(return_relationships[return_index])

        ###################################
        #if the user supplied a CAS
        ###################################
        elif type_of_data == "cas":
        #elif isinstance(compound_id, int):
            try:
                greenprint("[+] Performing Pubchem Query")
                lookup_results = pubchem.get_compounds(compound_id,'name',)
            except Exception :# pubchem.PubChemPyError:
                function_message("lookup by cid exception - CAS", Exception, "red")            
            #if there were multiple results
            # TODO: we have to figure out a good way to store the extra results
            #as possibly a side record
            if isinstance(lookup_results, list):
                greenprint("[+] Multiple results returned ")
                for each in lookup_results:
                    asdf = [{'cid'      : each.cid                ,\
                            #dis bitch dont have a CAS NUMBER!
                            #'cas'      : each.cas                 ,\
                            'smiles'    : each.isomeric_smiles     ,\
                            'formula'   : each.molecular_formula   ,\
                            'molweight' : each.molecular_weight    ,\
                            'charge'    : each.charge              ,\
                            'name'      : each.iupac_name          }]
                    return_relationships.append(asdf)
            ####################################################
            #Right here we need to find a way to store multiple records
            # and determine the best record to store as the main entry
            ####################################################
                    #compound_to_database() TAKES A LIST
                    # first element of first element
                    #[ [this thing here] , [not this one] ]
                redprint("=========RETURN RELATIONSHIPS=======")
                blueprint(str(return_relationships[return_index]))
                redprint("=========RETURN RELATIONSHIPS=======")
                Pubchem_lookup.compound_to_database(return_relationships[return_index])

            #if there was only one result
            elif isinstance(lookup_results, pubchem.Compound):
                asdf = [{'cid'      : each.cid                ,\
                            #dis bitch dont have a CAS NUMBER!
                            #'cas'      : each.cas                 ,\
                            'smiles'    : each.isomeric_smiles     ,\
                            'formula'   : each.molecular_formula   ,\
                            'molweight' : each.molecular_weight    ,\
                            'charge'    : each.charge              ,\
                            'name'      : each.iupac_name          }]
                return_relationships.append(asdf)
                redprint("=========RETURN RELATIONSHIPS=======")
                blueprint(return_relationships)
                redprint("=========RETURN RELATIONSHIPS=======")
                Pubchem_lookup.compound_to_database(return_relationships)
            else:
                function_message("PUBCHEM LOOKUP BY CID","ELSE AT THE END", "red")
        #and then, once all that is done return the LOCAL database entry to
        # the calling function so this is just an API to the db code
        return_query = return_relationships[return_index]
        redprint("==BEGINNING==return query for pubchem/local lookup===========")
        blueprint(str(return_query[0]))
        redprint("=====END=====return query for pubchem/local lookup===========")

        return database_setup.Database_functions.Compound_by_id(return_query)

###############################################################################
    def compound_to_database(lookup_list: list):
        """
        Puts a pubchem lookup to the database
        ["CID", "cas" , "smiles" , "Formula", "Name"]
        """
        print(inspect.stack()[1][3])

        lookup_cid                 = lookup_list[0].get('cid')
        #lookup_cas                = lookup_list[1].get('cas')
        lookup_smiles              = lookup_list[0].get('smiles')
        lookup_formula             = lookup_list[0].get('formula')        
        lookup_molweight           = lookup_list[0].get('molweight')        
        lookup_charge              = lookup_list[0].get('charge')
        lookup_name                = lookup_list[0].get('name')
        database_setup.Database_functions.add_to_db(Compound(cid     = lookup_cid,\
                           #cas     = lookup_cas,                   \
                           smiles    = lookup_smiles,                 \
                           formula   = lookup_formula,                \
                           molweight = lookup_molweight,              \
                           charge    = lookup_charge,                 \
                           name      = lookup_name                    ))

###############################################################################
    def composition_to_database(comp_name: str, units_used :str, \
                                formula_list : list , info : str):
        """
        The composition is a relation between multiple Compounds
        Each Composition entry will have required a pubchem_lookup on each
        Compound in the Formula field. 
        the formula_list is a CSV STRING WHERE: 
        ...str_compound,int_amount,.. REPEATING (floats allowed)
        EXAMPLE : Al,27.7,NH4ClO4,72.3

        BIG TODO: be able to input list of cas/cid/whatever for formula_list
        """
        print(inspect.stack()[1][3])

        # query local database for records before performing pubchem
        # lookups
        # expected to return FALSE if no record found
        # if something is there, it will evaluate to true
        for each in formula_list:
            input = Pubchem_lookup.formula_input_validation(each)

        # extend this but dont forget to add more fields in the database model!
        add_to_db(Composition(name       = comp_name,               \
                              units      = units_used,              \
                              compounds  = formula_list,            \
                              notes      = info                     ))

 ###############################################################################   
    async def format_mesage_arbitrary(self, arg1, arg2, arg3):
        pass

############################################################################### 
    async def format_message_discord(ctx, lookup_results_object):
        temp_output_container = []
        formatted_message = discord.Embed( \
            title=lookup_results_object.name,
            #change color option
            colour=discord.Colour(0x3b12ef),  \
            url="",
            description=size_check_256(lookup_results_object.formula),
            timestamp=datetime.datetime.utcfromtimestamp(1580842764))
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
            value=lookup_results_object.formula)
        formatted_message.add_field(
            name="Molecular Weight",
            value=lookup_results_object.molweight)
        formatted_message.add_field(
            name="Charge",
            value=lookup_results_object.charge)
        formatted_message.set_footer(
            text="",
            icon_url="")
        temp_output_container.append([formatted_message])
        #temp_output_container.append([Pubchem_lookup.format_message_discord(ctx, lookup_object)])
        #global lookup_output_container
        lookup_output_container = temp_output_container

################################################################################

######## AND NOW WE RUN THE BOT!!! YAY!!! I HAVE MORE DEBUGGING TO DO!!########
lookup_bot.run(discord_bot_token, bot=True)