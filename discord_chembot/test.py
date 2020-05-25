#!/usr/bin/python3
import os
#import re
import asyncio
import discord
import itertools
import mendeleev
import threading
import wikipedia
import math, cmath
import pubchempy as pubchem
#from bs4 import BeautifulSoup
from discord.ext import commands, tasks
from discord_key import *
from variables_for_reality import greenprint, redprint, blueprint
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
##stuff:
# https://www.thecrazyprogrammer.com/2018/05/wikipedia-api-python-tutorial.html
# https://pypi.org/project/mendeleev/
# https://wikipedia.readthedocs.io/en/latest/code.html#module-wikipedia
# https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#context
# https://mendeleev.readthedocs.io/en/stable\notebooks/01_intro_to_mendeleev.html#Getting-list-of-elements

#list_of_resources = "https://en.wikipedia.org/wiki/List_of_data_references_for_chemical_elements"
#data_pages_list   = "https://en.wikipedia.org/wiki/Category:Chemical_element_data_pages"

################################################################################
##############                BASIC VARIABLES                  #################
################################################################################
#bot = commands.Bot(command_prefix=("."))
#who dis?
#TODO: give this as an option eventually.
#data_list           = wikipedia.page(title='List_of_data_references_for_chemical_elements')

#https://discord.com/oauth2/authorize?client_id=712737412018733076&scope=bot&permissions=92160

################################################################################
##############                     BOT CORE                    #################
#    Every new command, needs a corrosponding function assigned in the class   #
################################################################################
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

#FIRST COMMAND
# right here we define behavior for the command
#   we are only ALLOWING two arguments:
#     the element identification
#     level of data requested
# instantiate the class and pass the data the user provided to the validation
#   function that will call everything else and parse the arguments. Once the
#   arguments are parsed, the algorhithm is applied, the output is formatted,
#   and the user is sent a reply@bot.command()


@lookup_bot.command()
async def lookup(ctx, arg1, arg2):
    await Element_lookup.validate_user_input(ctx, arg1, arg2)
    #await Element_lookup.format_and_print_output(lookup_output_container)
    #await ctx.send(lookup_output_container)
    list_to_string = lambda list_to_convert: ''.join(list_to_convert)
    string_to_send = list_to_string(lookup_output_container)
    await ctx.send(string_to_send)
###############################################################################

###############################################################################
class Element_lookup(commands.Cog):
    def __init__(self, ctx): #, input_container : list):
        #generate_element_name_list()
        #self.input_container  = input_container
        #self.output_container = []
        print("wat")    
################################################################################
##############              INTERNAL  FUNCTIONS                #################
################################################################################
#return_element_by_id = lambda element_id_input : mendeleev.element(element_id_input)
#for each in range(1,118):
#     asdf = return_element_by_id(each)
#     print(asdf.name)
#
#   list_to_string = lambda list_to_convert: ''.join(list_to_convert)
################################################################################
    async def help_message():
        return "Put the element's name, symbol, or atomic number followed \
    by either: physical, chemical, nuclear, ionization, isotopes, \
    oxistates"
        
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

        from variables_for_reality import element_list , symbol_list , specifics_list
        element_id_user_input = cap_if_string(element_id_user_input)
        element_valid   = bool
        specifics_valid = bool
        # if they are using an atomic number
        #OMG <3
        if isinstance(element_id_user_input, int) and element_id_user_input in range(1-118):
            element_valid = True
            #for some reason its turning it into a string so we kinda have to do THIS
            #element_id_user_input = int(element_id_user_input)
        # if they are using a name or symbol
        elif isinstance(element_id_user_input, str):
            #using a symbol
            if len(element_id_user_input) < 3:
                #for each in symbol_list:
                if any(user_input == element_id_user_input for user_input in symbol_list):
                    element_valid = True
                    print(element_id_user_input + "symbol TRUE")
                    print("element valid true wtf")
                elif any(user_input == element_id_user_input for user_input in element_list):
                    print(element_id_user_input + "name TRUE")
                    element_valid = True
                else:
                    print(" both false wtf")
                    Element_lookup.user_input_was_wrong("element")
        # if user send a string
        if isinstance(specifics_requested, str):
            specifics_requested = specifics_requested.lower()
            #for each in specifics_list:
            if any(user_input == specifics_requested for user_input in specifics_list):
                print(specifics_requested + "specifics")
                specifics_valid = True
            else:
                redprint("specifics 1 wtf")
                Element_lookup.user_input_was_wrong("specifics")
        else:
            redprint("specifics 2 wtf")
            Element_lookup.user_input_was_wrong("specifics")
        #they passed good data
        if element_valid and specifics_valid == True:      
            global lookup_output_container
            if specifics_requested    == "basic":
                Element_lookup.get_basic_element_properties(element_id_user_input)
                Element_lookup.reply_to_query(lookup_output_container)
                # so now you got the basic structure of the control loop!
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
        if element_id_user_input.isnumeric():
            element_object = mendeleev.element(int(element_id_user_input))
            greenprint(element_id_user_input + " ---- IN THE FUNCTION ")
        else:
            element_object = mendeleev.element(element_id_user_input)
            redprint(element_id_user_input + "---- IN THE FUNCTION")
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



###################################################
###               RUN THE BOT                   ###
###################################################

lookup_bot.run(discord_bot_token, bot=True)

########################################################################
########             RANDOM CODE SNIPPETS               ################
########################################################################
## links = My_table.findAll('a')
## return_element_by_id = lambda element_id_input : mendeleev.element(element_id_input)
#
# table_headers = resource_soup.find_all('th')
# data_table = soup.find('table',{'class':'wikitable sortable'})
#
#######################################################################
### This is how you get lists of data for ALL the elements at once:
##
### return_element_by_id = lambda element_id_input : mendeleev.element(element_id_input)
### for each in range(1,118):
###     asdf = return_element_by_id(each)
###     print(asdf.name)
###############################################################################
# CHANGE ELEMENT_OBJECT.NAME to ELEMENT_OBJECT.SOMETHING_ELSE
#
#    def generate_element_name_list():
#       return_element_by_id = lambda element_id_input : mendeleev.element(element_id_input)
#           for each in range(1,118):
#               element_object = return_element_by_id(each)
#               element_list.append(element_object.name)
################################################################################
#    async def list_resources(self, ctx, *,):
#        listy_list = []
#        resource_soup = BeautifulSoup(requests.get(data_pages_list).text,'lxml')
#        content = resource_soup.find_all('div' , {'class' : 'mw-content-ltr'})
#        for each in content.find_all('a'):
#            output_container.append(each)
###############################################################################
