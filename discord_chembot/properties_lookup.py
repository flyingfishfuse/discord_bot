#!/usr/bin/python3
import os
import ionize
import discord
import asyncio
import argparse
import itertools
import mendeleev
import threading
import wikipedia
import math, cmath
from ionize import *
import pubchempy as pubchem
#from bs4 import BeautifulSoup
from discord.ext import commands, tasks
from discord_chembot.discord_key import *
from discord_chembot.database_setup import *
################################################################################
## Chemical element resource database from wikipedia/mendeleev python library ##
##                             for discord bot                                ##
# Licenced under GPLv3                                                        ##
# https://www.gnu.org/licenses/gpl-3.0.en.html                                ##
################################################################################
##    Search by element number, symbol,
##    list resources available
##    TODO: show basic info if no specificity in query
# created by : mr_hai on discord / flyingfishfuse on github
#list_of_resources = "https://en.wikipedia.org/wiki/List_of_data_references_for_chemical_elements"
#data_pages_list   = "https://en.wikipedia.org/wiki/Category:Chemical_element_data_pages"
#
parser = argparse.ArgumentParser(description='Discord ChemBot')
parser.add_argument('--devs',
                                 dest    = 'dev_list_input',
                                 action  = "store" ,
                                 default = "" ,
                                 help    = "" )
parser.add_argument('--modules',
                                 dest    = 'modules_to_load_input',
                                 action  = "store" ,
                                 default = 'everything' ,
                                 help    = "CSVals; everything OR m_lookup,p_lookup,i_lookup" )
parser.add_argument('--bongo',
                                 dest    = '',
                                 action  = "store" ,
                                 default = '' ,
                                 help    = "" )

arguments = parser.parse_args()
#now work on args!!
################################################################################
##############                     BOT CORE                    #################
#    Every new command, needs a corrosponding function assigned in the class   #
################################################################################

##################################################
##########   BASIC VARIABLES    #################
##################################################
#data_list         = wikipedia.page(title='List_of_data_references_for_chemical_elements')

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
async def lookup(ctx, arg1, arg2):
    await Element_lookup.validate_user_input(ctx, arg1, arg2)
    list_to_string = lambda list_to_convert: ''.join(list_to_convert)
    string_to_send = list_to_string(lookup_output_container)
    await ctx.send(string_to_send)

###############################################################################
class Element_lookup(commands.Cog):
    def __init__(self, ctx): #, input_container : list):
        print("wat")    

#################################################
##########    INTERNAL  FUNCTIONS   #############
#################################################
    async def help_message():
        return "Put the element's name, symbol, or atomic number followed \
    by either: physical, chemical, nuclear, ionization, isotopes, \
    oxistates"
        
    def reply_to_query(message):
        '''
    Takes a list or string, if list, joins the list to a string and assigns to 
    lookup_output_container. Sends the global output container with ctx.send()
        '''
        list_to_string = lambda list_to_convert: ''.join(list_to_convert)
        if isinstance(message,list):
            message = list_to_string(message) 
        temp_array = [message]
        global lookup_output_container
        lookup_output_container = temp_array
        print(list_to_string(lookup_output_container))
        
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
        ########################################
        #this is bullshit                      #
        #mendeleeve needs to implement this    #
        #check internally                      #
        def cap_if_string(thing):              #
            """                                   
            If the element name isn't capitalized 
            do so.                                
            """                                #
            if isinstance(thing, str):         #
                return thing.capitalize()      #
            else:                              #
                return int(thing)              #
        ########################################
        list_to_string = lambda list_to_convert: ''.join(list_to_convert)
        global lookup_output_container
        from discord_chembot.variables_for_reality import element_list , symbol_list , specifics_list
        print(element_id_user_input)
        element_id_user_input = cap_if_string(element_id_user_input)
        ## TODO: play with this to get it working right
        # it needs to evaluate ONCE NOT TWICE!
        for each in element_list and symbol_list: # (element_list, symbol_list)
            if any(user_input == element_id_user_input for user_input in each) or element_id_user_input in range(1-118):
                    if any(user_input == specifics_requested for user_input in specifics_list):
                        if specifics_requested.lower()    == "basic":
                            Element_lookup.get_basic_element_properties(element_id_user_input)
                            Element_lookup.reply_to_query(lookup_output_container)
                        # so now you got the basic structure of the control loop!
                        elif specifics_requested.lower()  == "physical":
                            Element_lookup.get_physical_properties(element_id_user_input)
                            Element_lookup.reply_to_query(lookup_output_container)
                        elif specifics_requested.lower()  == "chemical":
                            Element_lookup.get_chemical_properties(element_id_user_input)
                            Element_lookup.reply_to_query(lookup_output_container)
                        elif specifics_requested.lower()  == "nuclear":
                            Element_lookup.get_nuclear_properties(element_id_user_input)
                            Element_lookup.reply_to_query(lookup_output_container)
                        elif specifics_requested.lower()  == "ionization":
                            Element_lookup.get_ionization_energy(element_id_user_input)
                            Element_lookup.reply_to_query(lookup_output_container)
                        elif specifics_requested.lower()  == "isotopes":
                            Element_lookup.get_isotopes(element_id_user_input)
                            Element_lookup.reply_to_query(lookup_output_container)
                        elif specifics_requested.lower()  == "oxistates":
                            Element_lookup.get_oxistates(element_id_user_input)
                            Element_lookup.reply_to_query(lookup_output_container)
                    # input given by user was NOT found in the validation data
                    else:
                        Element_lookup.user_input_was_wrong("specifics")
            else:
                Element_lookup.user_input_was_wrong("element")
        # then the control loop exits and the next line of code in the command is 
        # EXECUTED

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

################################################################################
    def pubchem_lookup_by_name_or_CID(user_input:str or int):
        '''
        Future site of the "formula to name/ name to formula" converter
        expecting either an IUPAC chemical name or integer
        '''
        from variables_for_reality import compound_name_formula_cache
        # expecting either an IUPAC chemical name or integer
        ## TODO: make a cache file to store a local copy of the lookup data
        # Gotta find a way to make all this portable and fast

# have to ask the user to select which one they want
#>>> results = pcp.get_compounds('Glucose', 'name')
#>>> print results
#[Compound(79025), Compound(5793), Compound(64689), Compound(206)]
# and then we can lookup by ID to get the whole thing
        if isinstance(user_input, str):
            name_lookup_results_list = pubchem.get_compounds(user_input , 'name')
            result_1 = name_lookup_results_list[0]
            result_2 = name_lookup_results_list[1]
            result_3 = name_lookup_results_list[2]
         
        elif isinstance(user_input, int):
            name_lookup_result = pubchem.Compound(user_input)



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
        lookup_output_container.append("Abundance in Crust" + element_object.abundance_crust + "\n")
        lookup_output_container.append("Abundance in Sea: " + element_object.abundance_sea + "\n")
        lookup_output_container.append("Discoveries: " + element_object.discoveries  + "\n")
        lookup_output_container.append("Discovery Location: " + element_object.discovery_location  + "\n")
        lookup_output_container.append("Discovery Year: " + element_object.discovery_year        + "\n")
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

###############################################################################

    def get_physical_properties(element_id_user_input):
        """
        Returns physical properties of the element requested
        """
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
        temp_output_container.append("Electron Affinity: "    + element_object.electron_affinity  + "\n")
        temp_output_container.append("Heat Of Formation: "    + element_object.heat_of_formation  + "\n")
        temp_output_container.append("Heat Of Evaportation: " + element_object.evaporation_heat   + "\n")
        temp_output_container.append("Electronegativity: "    + element_object.electronegativity  + "\n")
        temp_output_container.append("Covalent Radius: "      + element_object.covalent_radius    + "\n")
        temp_output_container.append("Polarizability: "       + element_object.dipole_polarizability  + "\n")
        global lookup_output_container
        lookup_output_container = temp_output_container

###############################################################################

    def get_nuclear_properties(element_id_user_input):
        """
        Returns Nuclear properties of the element requested
        """
        temp_output_container = []
        element_object = mendeleev.element(element_id_user_input)
        temp_output_container.append("Neutrons: " + element_object.neutrons  + "\n")
        temp_output_container.append("Protons: "  + element_object.protons   + "\n")
        temp_output_container.append("Atomic Radius: "  + element_object.atomic_radius  + "\n")
        temp_output_container.append("Atomic Weight: "  + element_object.atomic_weight  + "\n")
        temp_output_container.append("Radioactivity: "  + element_object.is_radioactive  + "\n")
        global lookup_output_container
        lookup_output_container = temp_output_container

###############################################################################
    
    def get_isotopes(element_id_user_input):
        """
        Returns Isotopes of the element requested
        """
        temp_output_container = []
        element_object = mendeleev.element(element_id_user_input)
        temp_output_container.append("Isotopes: " + element_object.isotopes + "\n")
        global lookup_output_container
        lookup_output_container = temp_output_container

###############################################################################

    def get_ionization_energy(element_id_user_input):
        """
        Returns Ionization energies of the element requested
        """
        temp_output_container = []
        element_object = mendeleev.element(element_id_user_input)
        temp_output_container.append("Ionization Energies: " + element_object.ionenergies  + "\n")
        global lookup_output_container
        lookup_output_container = temp_output_container



###################################################
###               RUN THE BOT                   ###
###################################################

lookup_bot.run(discord_bot_token, bot=True)
