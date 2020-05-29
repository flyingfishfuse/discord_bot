#!/usr/bin/python3
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
import discord_chembot.database_setup
from discord.ext import commands, tasks
from chempy import balance_stoichiometry
from discord_chembot.discord_key import *
from discord_chembot.database_setup import *
#from discord_chembot.discord_commands import *
from discord_chembot.element_lookup_class import Element_lookup
from discord_chembot.variables_for_reality import greenprint,redprint,blueprint
from discord_chembot.variables_for_reality import show_line_number,cas_regex
#pretend main file, move contents to properties_lookup.py

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
if load_cogs == True:
    for filename in cog_directory_files:
        if filename.endswith(".py"):
            lookup_bot.load_extension(f"cogs.{filename[:-3]}")
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
    await lookup_bot.change_presence(activity=discord.Game(name="THIS IS BETA !"))

#HELP COMMAND
@lookup_bot.command()
async def element_lookup_usage(ctx):
    await ctx.send(await Element_lookup.help_message())

@lookup_bot.command()
async def pubchem_lookup_usage(ctx):
    await ctx.send(await Pubchem_lookup.help_message())

@lookup_bot.command()
async def balancer_usage(ctx):
    await ctx.send(await Pubchem_lookup.balancer_message())

@lookup_bot.command()
async def bot_usage(ctx):
    await ctx.send(bot_help_message)

@lookup_bot.command()
async def element_lookup(ctx, arg1, arg2):
    await Element_lookup.validate_user_input(ctx, arg1, arg2)
    #await Element_lookup.format_and_print_output(lookup_output_container)
    #await ctx.send(lookup_output_container)
    list_to_string = lambda list_to_convert: ''.join(list_to_convert)
    string_to_send = list_to_string(lookup_output_container)
    await ctx.send(string_to_send)

@lookup_bot.command()
async def pubchem_lookup(ctx, arg1):
    await Pubchem_lookup.validate_user_input(ctx, arg1)
    #list_to_string = lambda list_to_convert: ''.join(list_to_convert)
    #string_to_send = list_to_string(lookup_output_container)
    #await ctx.send(string_to_send)
    
    # The lookup_output_container can be used to store objects!    
    #await ctx.send(content="lol", embed=formatted_reply_object)
    await ctx.send(content="lol", embed=lookup_output_container[0])

#@lookup_bot.command()
#async def pubsearch(ctx, arg1, arg2, arg3):
#    user_input = self.validate_user_input( arg1, arg2, arg3 )
#    lookup = self.pubchem_lookup_by_name_or_CID(user_input)

# now we can just start copying code and changing it slightly to implement
# new functionality

##############################################################################
#figure out WHY this is doing and make it less ugly
def size_check_256(thing_to_check):
    if len(thing_to_check) != None and 150 < len(thing_to_check) < 256:
        return (str(thing_to_check[:100]) + "... sliced ...")
    else:
        function_message(thing_to_check, "red")
##############################################################################

class Pubchem_lookup(commands.Cog):
    '''
Class to perform lookups on CID's and IUPAC names
Also does chempy translation to feed data to the calculation engine
    '''
    def __init__(self, ctx):
        self.asdf                 = ["test_init : self.asdf"]
        self,lookup_result        = ["test_init : self.lookup_result"]
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

    def user_input_was_wrong(type_of_pebkac_failure : str):
        """
        You can put something funny here!
            This is something the creator of the bot needs to modify to suit
            Thier community.
        """
        user_is_a_doofus_CID_message  = "Stop being a doofus and feed me a good CID! "
        user_is_a_doofus_formula_message = "Stop being a doofus and feed me a good formula!"
        if type_of_pebkac_failure   == "pubchem_lookup_by_name_or_CID":
            Pubchem_lookup.reply_to_query(user_is_a_doofus_CID_message)
        elif type_of_pebkac_failure == "specifics":
            Pubchem_lookup.reply_to_query(user_is_a_doofus_formula_message)
        else:
            #change this to sonething reasonable
            Element_lookup.reply_to_query(type_of_pebkac_failure)

    def lookup_failure(type_of_failure: str):
        """
        does what it says on the label, called when a lookup is failed
        """
        #TODO: find sqlalchemy exception object
        # why cant I find the type of object I need fuck me
        if type_of_failure == "SQL":
            global lookup_output_container
            lookup_output_container = ["SQL QUERY FAILURE"]
        elif type_of_failure == pubchem.PubChemPyError:
            global lookup_output_container
            lookup_output_container = ["chempy failure"]
        pass
    
    def dump_db():
        """
    Prints database to screen
        """
        redprint("--------------DUMPING DATABASE-----------")
        records1 = database.session.query(Compound).all()
        records2 = database.session.query(Composition).all()
        for each in records1, records2:
            print (each)
        redprint("------------END DATABASE DUMP------------")


    async def validate_user_input(self, ctx, user_input: str, type_of_input:str):
        """
    User Input is expected to be the proper identifier.
        only one input, we are retrieving one record for one entity
    
    Remove self, ctx and async from the code to transition to non-discord
        """
        #this is a joke: "Hard Pass". 
        # lambda hard = True : hard ; pass  
        import inspect
        temp_output_container = []
        ######################################################
        # if CAS
        if type_of_input == "cas":
            try:
                #regex for a CAS number
                # if good
                if re.match(cas_regex,user_input):
                    greenprint("GOOD CAS NUMBER")
                    print(self.pubchem_lookup_by_name_or_CID(user_input))
                    show_line_number()
                    internal_lookup = internal_local_database_lookup(user_input, "cas")
                    # NOT IN THE LOCAL DB
                    if internal_lookup == False:
                        redprint("============Internal Lookup returned FALSE===========")
                        blueprint("Performing a PubChem lookup")
                        # every good lookup will add an entry to the db
                        print(Pubchem_lookup.pubchem_lookup_by_name_or_CID(user_input))
                        #this returns an SQLAlchemy Object
                        lookup_object = Pubchem_lookup.pubchem_lookup_by_name_or_CID(user_input)
                        #output is now object in list in list
                        # [ [lookup_object] ]
                        temp_output_container.append(lookup_object)
                        global lookup_output_container
                        lookup_output_container = temp_output_container
                    #IN THE LOCAL DB
                    elif internal_lookup == True:
                        greenprint("============Internal Lookup returned TRUE===========")
                        print(internal_lookup)
                        self.dump_db()
                    else:
                        function_message("validation lookup checks", "red")                    
            except Exception:
                function_message(Exception, "blue") 
        ######################################################
        # if formula
        if type_of_input == "formula":
            try:
                if Pubchem_lookup.validate_formula_input(user_input) == True:
                    lookup = internal_local_database_lookup(user_input, "formula")
                if lookup == False:
                    redprint("============Internal Lookup returned false===========")
                    Pubchem_lookup.pubchem_lookup_by_name_or_CID(user_input)
                elif lookup == True:
                    greenprint("============Internal Lookup returned TRUE===========")
                else:
                    function_message("validation lookup checks", "red")
            except Exception:
                function_message(Exception, "blue")            
##############################################################################
#if CAS
        if type_of_input == "cid":
            try:
                wat = Pubchem_lookup.validate_formula_input()
                lookup = internal_local_database_lookup(user_input, "formula")
                if lookup == False:
                    redprint("============Internal Lookup returned false===========")
                    Pubchem_lookup.pubchem_lookup_by_name_or_CID(user_input)
                elif internal_lookup == True:
                    greenprint("============Internal Lookup returned TRUE===========")
                else:
                    function_message("validation lookup checks", "red")
            except Exception:
                function_message(Exception, "blue") 
###############################################################################
# if CID
        if type_of_input == "cid":
            try:
                wat = Pubchem_lookup.validate_formula_input()
                internal_lookup = internal_local_database_lookup(user_input, "formula")
                if internal_lookup == False:
                    redprint("============Internal Lookup returned false===========")
                    Pubchem_lookup.pubchem_lookup_by_name_or_CID(user_input)
                elif internal_lookup == True:
                    greenprint("============Internal Lookup returned TRUE===========")
                else:
                    function_message("validation lookup checks", "red")
            except Exception:
                function_message(Exception, "blue") 
###############################################################################
    def validate_formula_input(formula_input : str):
        """
        :param formula_input: comma seperated values of element symbols
        :type formula_input: str     
    makes sure the formula supplied to the code is valid
    This is an input side function
        """
        # maybe we can feed the formula CSV to chempy directly and use the 
        # error and validation functions of chempy to determine if the 
        # user supplied good information? We can strongly reduce our own checks
        # EVERYWHERE if we validate on the input function. Don't write more 
        # code than necessary!

        # SO! Here we have fed the input to a chempy.Substance!
        parsed_csv = csv.reader(formula_input, delimiter=",")
        for each in parsed_csv:
            greenprint(each)
            blueprint(chempy.Substance(each))
        try:
            test_entity1 = chempy.Substance.from_formula(formula_input)
            test_entity2 = chempy.Substance.from_formula
            function_message(test_entity1, "red")
        # if it doesn't work, lets see why!
        except Exception:
            function_message(Exception, "red")
            function_message(test_entity1, "red")
        
    #remove async and ctx to make non-discord
    #async def send_reply(self, ctx, formatted_reply_object):
    #    reply = format_message_discord(self, ctx, formatted_reply)
    #    await ctx.send(content="lol", embed=formatted_reply_object)
    #    await ctx.send(content="lol", embed=reply)
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
        global lookup_output_container
        lookup_output_container = temp_array 

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
    def pubchem_lookup_by_name_or_CID(compound_id:str or int, type_of_data:str):
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
        TODO: SEARCH BY CAS!!!!
        '''
        #make a thing
        return_relationships = list
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
        #if isinstance(compound_id, str):
            try:
                lookup_results = pubchem.get_compounds(compound_id,'name')
            except Exception :# pubchem.PubChemPyError:
                function_message(Exception)
                user_input_was_wrong("pubchem_lookup_by_name_or_CID")
            #if there were multiple results
            # TODO: we have to figure out a good way to store the extra results
                   #as possibly a side record
            if isinstance(lookup_results, list):
                for each in lookup_results:
                    return_relationships.append([                  \
                    {'cid'     : each.cid                        },\
                    {'cas'     : each.cas                        },\
                    {'smiles'  : each.smiles                     },\
                    {'formula' : each.molecular_formula          },\
                    {'name'    : each.iupac_name                 }])
                    ####################################################
                    #Right here we need to find a way to store multiple records
                    # and determine the best record to store as the main entry
                    ####################################################
                    #compound_to_database() TAKES A LIST
                    # first element of first element
                    #[ [this thing here] , [not this one] ]
                    redprint("=========RETURN RELATIONSHIPS=======")
                    blueprint(return_relationships)
                    redprint("=========RETURN RELATIONSHIPS=======")
                    compound_to_database(return_relationships[return_index])
            
            # if there was only one result
            elif isinstance(lookup_results, pubchem.Compound):
                return_relationships.append([                       \
                    {'cid'     : lookup_results.cid               },\
                    {'cas'     : lookup_results.cas               },\
                    {'smiles'  : lookup_results.smiles            },\
                    {'formula' : lookup_results.molecular_formula },\
                    {'name'    : lookup_results.iupac_name        }])
                redprint("=========RETURN RELATIONSHIPS=======")
                blueprint(return_relationships)
                redprint("=========RETURN RELATIONSHIPS=======")
                compound_to_database(return_relationships)

        ###################################
        #if the user supplied a CID
        ###################################
        elif type_of_data == "cid":
        #elif isinstance(compound_id, int):
            try:
                lookup_results = pubchem.Compound.from_cid(compound_id)
            except Exception :# pubchem.PubChemPyError:
                function_message(Exception)
                #if there were multiple results
                # TODO: we have to figure out a good way to store the extra results
                   #as possibly a side record
            if isinstance(lookup_results, list):
                return_relationships.append([                        \
                    {'cid'     : lookup_results.cid                },\
                    {'cas'     : each.cas                          },\
                    {'smiles'  : each.smiles                       },\
                    {'formula' : lookup_results.molecular_formula  },\
                    {'name'    : lookup_results.iupac_name         }])
            ####################################################
            #Right here we need to find a way to store multiple records
            # and determine the best record to store as the main entry
            ####################################################
                    #compound_to_database() TAKES A LIST
                    # first element of first element
                    #[ [this thing here] , [not this one] ]
                redprint("=========RETURN RELATIONSHIPS=======")
                blueprint(return_relationships)
                redprint("=========RETURN RELATIONSHIPS=======")
                compound_to_database(return_relationships[return_index])

            #if there was only one result
            elif isinstance(lookup_results, pubchem.Compound):
                return_relationships.append([                        \
                    {'cid'     : lookup_results.cid                },\
                    {'cas'     : lookup_results.cas                },\
                    {'smiles'  : lookup_results.smiles             },\
                    {'formula' : lookup_results.molecular_formula  },\
                    {'name'    : lookup_results.iupac_name         }])
                redprint("=========RETURN RELATIONSHIPS=======")
                blueprint(return_relationships)
                redprint("=========RETURN RELATIONSHIPS=======")
                compound_to_database(return_relationships)

        ###################################
        #if the user supplied a CAS
        ###################################
        elif type_of_data == "cas":
        #elif isinstance(compound_id, int):
            try:
                lookup_results = pubchem.get_compounds(compound_id,'name',)
            except Exception :# pubchem.PubChemPyError:
                function_message(Exception)                
            #if there were multiple results
            # TODO: we have to figure out a good way to store the extra results
            #as possibly a side record
            if isinstance(lookup_results, list):
                return_relationships.append([                        \
                    {'cid'     : lookup_results.cid                },\
                    {'cas'     : each.cas                          },\
                    {'smiles'  : each.smiles                       },\
                    {'formula' : lookup_results.molecular_formula  },\
                    {'name'    : lookup_results.iupac_name         }])
            ####################################################
            #Right here we need to find a way to store multiple records
            # and determine the best record to store as the main entry
            ####################################################
                    #compound_to_database() TAKES A LIST
                    # first element of first element
                    #[ [this thing here] , [not this one] ]
                redprint("=========RETURN RELATIONSHIPS=======")
                blueprint(return_relationships)
                redprint("=========RETURN RELATIONSHIPS=======")
                compound_to_database(return_relationships[return_index])

            #if there was only one result
            elif isinstance(lookup_results, pubchem.Compound):
                return_relationships.append([                        \
                    {'cid'     : lookup_results.cid                },\
                    {'cas'     : lookup_results.cas                },\
                    {'smiles'  : lookup_results.smiles             },\
                    {'formula' : lookup_results.molecular_formula  },\
                    {'name'    : lookup_results.iupac_name         }])
                redprint("=========RETURN RELATIONSHIPS=======")
                blueprint(return_relationships)
                redprint("=========RETURN RELATIONSHIPS=======")
                compound_to_database(return_relationships)
            else:
                function_message("PUBCHEM LOOKUP BY CID", "red")
        #and then, once all that is done return the LOCAL database entry to
        # the calling function so this is just an API to the db code
        return_query = return_relationships[return_index.get("cid")]
        redprint("==BEGINNING==return query for pubchem/local lookup===========")
        blueprint(return_query)
        redprint("=====END=====return query for pubchem/local lookup===========")

        return Compound_by_id(return_query)

###############################################################################
    def compound_to_database(lookup_list: list):
        """
        Puts a pubchem lookup to the database
        ["CID", "cas" , "smiles" , "Formula", "Name"]
        """
        lookup_cid                 = lookup_list[0].get('cid')
        lookup_cas                 = lookup_list[1].get('cas')
        lookup_smiles              = lookup_list[2].get('smiles')
        lookup_formula             = lookup_list[3].get('formula')
        lookup_name                = lookup_list[4].get('name')
        add_to_db(Compound(cid     = lookup_cid,                    \
                           cas     = lookup_cas,                    \
                           smiles  = lookup_smiles,                 \
                           formula = lookup_formula,                \
                           name    = lookup_name                   ))
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
    async def format_mesage_arbitrary(self, ctx, arg1, arg2, arg3):
        pass

###############################################################################    
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
    reactants =  {'NH4ClO4', 'Al'} 
    products  =  {'Al2O3', 'HCl', 'H2O', 'N2'}
    #balance the equation
    chem_react , chem_prod = chempy.balance_stoichiometry(reactants,products)
    #pprint(dict(reac))
    #{'Al': 10, 'NH4ClO4': 6}
    #pprint(dict(prod))
    #{'Al2O3': 5, 'H2O': 9, 'HCl': 6, 'N2': 3}
    #iterates over reactants and products with the function 

    for each in mass_fractions(chem_react):
        pass
    for each in mass_fractions(chem_prod):
        pass

    for fractions in map(mass_fractions, [react, prod]):
        #{k: '{0:.3g} wt%'.format(v*100) for k, v in fractions.items()}
        #[{'C': x1 + 2, 'O2': x1 + 1}, {'CO': 2, 'CO2': x1}]
        print(fractions)
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
            function_message("local db query returned NEGATIVE", "red")
            Pubchem_lookup.pubchem_lookup_by_name_or_CID(each)


################################################################################
################################################################################
## WE DONT HAVE TO PAY ATENTION TO ANYTHING BELOW THIS
## WE DONT HAVE TO PAY ATENTION TO ANYTHING BELOW THIS
################################################################################
################################################################################

class Element_lookup(commands.Cog):
    def __init__(self, ctx): #, input_container : list):
        #generate_element_name_list()
        #self.input_container  = input_container
        #self.output_container = []
        print("wat") 

    async def help_message():
        return "Put the element's name, symbol, or atomic number followed \
by either: basic, historical, physical, chemical, nuclear, ionization, \
isotopes, oxistates\n For Pubchem lookup, use a CID or IUPAC name ONLY"
        
    def reply_to_query(message):
        '''
    Takes a list or string, if list, joins the list to a string and assigns to 
    lookup_output_container. Sends the global output container with ctx.send()
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
        global lookup_output_container
        lookup_output_container = temp_array        
        
    def user_input_was_wrong(type_of_pebkac_failure : str):
        """
        You can put something funny here!
            This is something the creator of the bot needs to modify to suit
            Thier community.
        """
        user_is_a_doofus_element_message  = "Stop being a doofus and feed the data on elements that I expect! "
        user_is_a_doofus_specific_message = "Stop being a doofus and feed the data on specifics that I expect!"
        if type_of_pebkac_failure   == "element":
            Element_lookup.reply_to_query(user_is_a_doofus_element_message)
        elif type_of_pebkac_failure == "specifics":
            Element_lookup.reply_to_query(user_is_a_doofus_specific_message)
        else:
            Element_lookup.reply_to_query(type_of_pebkac_failure)

    async def validate_user_input(ctx, element_id_user_input: str or int, specifics_requested : str):
        """
        checks if the user is requesting an actual element and set of data.
        This is the main function that "does the thing", you add new
        behaviors here, and tie them to the commands in the bot core code
        """
        def cap_if_string(thing):              
            """                                   
            If the element name isn't capitalized 
            do so.                                
            """                                
            if isinstance(thing, str):         
                return thing.capitalize()      
            elif isinstance(thing , int):                              
                return int(thing)              

        from discord_chembot.variables_for_reality import element_list , symbol_list , specifics_list
        element_id_user_input = cap_if_string(element_id_user_input)
        element_valid   = bool
        specifics_valid = bool
        #atomic number
        if element_id_user_input.isnumeric() and int(element_id_user_input) in range(0,119):
                element_valid = True
                element_id_user_input = int(element_id_user_input)
        #symbol        
        elif isinstance(element_id_user_input, str) and (0 < len(element_id_user_input) < 3):
            if any(user_input == element_id_user_input for user_input in symbol_list):
                element_valid = True
        #name        
        elif isinstance(element_id_user_input , str) and (2 < len(element_id_user_input) < 25) :
            if any(user_input == element_id_user_input.capitalize() for user_input in element_list):
                element_valid = True
        else:
            Element_lookup.user_input_was_wrong("element")

        if isinstance(specifics_requested, str):
            specifics_requested = specifics_requested.lower()

            if any(user_input == specifics_requested for user_input in specifics_list):
                specifics_valid = True
            else:
                Element_lookup.user_input_was_wrong("specifics")

        else:
            Element_lookup.user_input_was_wrong("specifics")

        if element_valid and specifics_valid == True:      
            global lookup_output_container
            if specifics_requested    == "basic":
                Element_lookup.get_basic_element_properties(element_id_user_input)
                Element_lookup.reply_to_query(lookup_output_container)
                # so now you got the basic structure of the control loop!
            elif specifics_requested  == "historical":
                Element_lookup.get_history(element_id_user_input)
                print(lookup_output_container)
                Element_lookup.reply_to_query(lookup_output_container)
            elif specifics_requested  == "physical":
                Element_lookup.get_physical_properties(element_id_user_input)
                print(lookup_output_container)
                Element_lookup.reply_to_query(lookup_output_container)
            elif specifics_requested  == "chemical":
                Element_lookup.get_chemical_properties(element_id_user_input)
                Element_lookup.reply_to_query(lookup_output_container)
                print(lookup_output_container)
            elif specifics_requested  == "nuclear":
                Element_lookup.get_nuclear_properties(element_id_user_input)
                Element_lookup.reply_to_query(lookup_output_container)
                print(lookup_output_container)
            elif specifics_requested  == "ionization":
                Element_lookup.get_ionization_energy(element_id_user_input)
                Element_lookup.reply_to_query(lookup_output_container)
                print(lookup_output_container)
            elif specifics_requested  == "isotopes":
                Element_lookup.get_isotopes(element_id_user_input)
                Element_lookup.reply_to_query(lookup_output_container)
                print(lookup_output_container)
            elif specifics_requested  == "oxistates":
                Element_lookup.get_oxistates(element_id_user_input)
                Element_lookup.reply_to_query(lookup_output_container)
                print(lookup_output_container)
            # input given by user was NOT found in the validation data
            else:
                print("wtf")
        else:
            print("wtf")

################################################################################
##############          COMMANDS AND USER FUNCTIONS            #################
################################################################################
# command is {prefix}{compare_element_list}{"affinity" OR "electronegativity"}{"less" OR "greater"}
############################
# alpha FUNCTIONS
###########################
# these needs to be integrated to the main script
# This function compares ALL the elements to the one you provide
# you can extend the functionality by copying the relevant code
###############################################################################
    def compare_element_list(self, element_id_user_input, data_type : str, less_greater: str):
        element_data_list = []
        return_element_by_id = lambda element_id_input : mendeleev.element(element_id_input)
        element_to_compare   = return_element_by_id(element_id_user_input)
        for each in range(1,118):
            element_object = return_element_by_id(each)
            # CHANGE ELEMENT_OBJECT.NAME to ELEMENT_OBJECT.SOMETHING_ELSE
            # That is all you need to do, then add the new functionality to the
            # help and list
            if data_type == "affinity":
                if less_greater == "less":
                    if element_object.electron_affinity < element_to_compare.electron_affinity:
                        element_data_list.append(element_object.electron_affinity)
                elif less_greater == "greater":
                    if element_object.electron_affinity > element_to_compare.electron_affinity:
                        element_data_list.append(element_object.electron_affinity)
            elif data_type == "electronegativity":
                if less_greater == "less":
                    if element_object.electronegativity < element_to_compare.electronegativity:
                        element_data_list.append(element_object.electronegativity)
                elif less_greater == "greater":
                    if element_object.electronegativity > element_to_compare.electronegativity:
                        element_data_list.append(element_object.electronegativity)

###############################################################################

    name_lookup_results_list = []
    name_lookup_result = None
    def pubchem_lookup_by_name_or_CID(compound_id:str or int):
        if isinstance(compound_id, str):
            name_lookup_results_list = pubchem.get_compounds(compound_id,\
                                        'name' , \
                                        list_return='flat')
            #name = name_lookup_results_list[0]
            #result_2 = name_lookup_results_list[1]
            #result_3 = name_lookup_results_list[2]

        elif isinstance(compound_id, int):
            self.name_lookup_result = pubchem.Compound.from_cid(compound_id)
            # so now we have stuff.

###############################################################################
    def get_history(element_id_user_input):
        """
        Returns some historical information about the element requested
        takes either a name,atomic number, or symbol
        """
        global lookup_output_container
        lookup_output_container = []
        element_object = mendeleev.element(element_id_user_input)
        lookup_output_container.append("Uses: " + element_object.uses        + "\n")
        lookup_output_container.append("Abundance in Crust" + str(element_object.abundance_crust) + "\n")
        lookup_output_container.append("Abundance in Sea: " + str(element_object.abundance_sea) + "\n")
        lookup_output_container.append("Discoveries: " + element_object.discoveries  + "\n")
        lookup_output_container.append("Discovery Location: " + element_object.discovery_location  + "\n")
        lookup_output_container.append("Discovery Year: " + str(element_object.discovery_year)        + "\n")
        #await Element_lookup.format_and_print_output(output_container)
        #return output_container

    def calculate_hardness_softness(element_id_user_input, hard_or_soft, ion_charge):
        """
        calculates hardness/softness of an ion
        """
        output_container = []
        element_object = mendeleev.element(element_id_user_input)
        if hard_or_soft == "hardness":
            #electron_affinity = element_object.hardness(charge = charge)[0]
            #ionization_energy = element_object.hardness(charge = charge)[1]
            output_container.append("Hardness: "      + element_object.hardness(charge = ion_charge)      + "\n")
        elif hard_or_soft == "soft":
            output_container.append("Softness: "      + element_object.softness(charge = ion_charge)      + "\n")

############################
# beta FUNCTIONS
###########################
#these are already integrated into the core code of the script

#    async def get_information(element_id_user_input):
#        """
#        Returns information about the element requested
#        takes either a name,atomic number, or symbol
#        """
#        output_container = []
#        element_object = mendeleev.element(element_id_user_input)
#        output_container.append(" yatta yatta yata " + element_object.description  + "\n")
#        return output_container

###############################################################################

    def get_basic_element_properties(element_id_user_input):
        """
        takes either a name,atomic number, or symbol
        """
        temp_output_container = []
        element_object = mendeleev.element(element_id_user_input)
        temp_output_container.append("Element: "       + element_object.name          + "\n")
        temp_output_container.append("Atomic Weight: " + str(element_object.atomic_weight) + "\n")
        temp_output_container.append("CAS Number: "    + str(element_object.cas)           + "\n")
        temp_output_container.append("Mass: "           + str(element_object.mass)          + "\n")
        temp_output_container.append("Description: " + element_object.description  + "\n")
        temp_output_container.append("Sources: " + element_object.sources  + "\n")
        global lookup_output_container
        lookup_output_container = temp_output_container
        print(temp_output_container)

###############################################################################

    def get_physical_properties(element_id_user_input):
        """
        Returns physical properties of the element requested
        """
        #sends to global as a list of multiple strings
        # those strings are then 
        temp_output_container = []
        element_object = mendeleev.element(element_id_user_input)
        temp_output_container.append("Boiling Point:"  + str(element_object.boiling_point) + "\n")
        temp_output_container.append("Melting Point:"  + str(element_object.melting_point) + "\n")
        temp_output_container.append("Specific Heat:"  + str(element_object.specific_heat) + "\n")
        temp_output_container.append("Thermal Conductivity:"  + str(element_object.thermal_conductivity) + "\n")
        global lookup_output_container
        lookup_output_container = temp_output_container

###############################################################################

    def get_chemical_properties(element_id_user_input):
        """
        Returns Chemical properties of the element requested
        """
        temp_output_container = []
        element_object = mendeleev.element(element_id_user_input)
        temp_output_container.append("Electron Affinity: "    + str(element_object.electron_affinity)  + "\n")
        temp_output_container.append("Heat Of Formation: "    + str(element_object.heat_of_formation)  + "\n")
        temp_output_container.append("Heat Of Evaportation: " + str(element_object.evaporation_heat)   + "\n")
        #temp_output_container.append("Electronegativity: "    + str(element_object.electronegativity)  + "\n")
        #temp_output_container.append("Covalent Radius: "      + str(element_object.covalent_radius)    + "\n")
        #temp_output_container.append("Polarizability: "       + str(element_object.dipole_polarizability)  + "\n")
        global lookup_output_container
        lookup_output_container = temp_output_container

###############################################################################

    def get_nuclear_properties(element_id_user_input):
        """
        Returns Nuclear properties of the element requested
        """
        temp_output_container = []
        element_object = mendeleev.element(element_id_user_input)
        temp_output_container.append("Neutrons: " + str(element_object.neutrons)  + "\n")
        temp_output_container.append("Protons: "  + str(element_object.protons)   + "\n")
        temp_output_container.append("Atomic Radius: "  + str(element_object.atomic_radius)  + "\n")
        temp_output_container.append("Atomic Weight: "  + str(element_object.atomic_weight)  + "\n")
        temp_output_container.append("Radioactivity: "  + str(element_object.is_radioactive)  + "\n")
        global lookup_output_container
        lookup_output_container = temp_output_container

###############################################################################
    
    def get_isotopes(element_id_user_input):
        """
        Returns Isotopes of the element requested
        """
        temp_output_container = []
        element_object = mendeleev.element(element_id_user_input)
        temp_output_container.append("Isotopes: " + str(element_object.isotopes) + "\n")
        #await Element_lookup.format_and_print_output(output_container)
        global lookup_output_container
        lookup_output_container = temp_output_container

###############################################################################

    def get_ionization_energy(element_id_user_input):
        """
        Returns Ionization energies of the element requested
        """
        temp_output_container = []
        element_object = mendeleev.element(element_id_user_input)
        temp_output_container.append("Ionization Energies: " + str(element_object.ionenergies)  + "\n")
        global lookup_output_container
        lookup_output_container = temp_output_container
