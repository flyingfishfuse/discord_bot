#!/usr/bin/python3
import os
import re
import asyncio
import discord
import mendeleev
import threading
import wikipedia
import math, cmath
from itertools import cycle
#from bs4 import BeautifulSoup
from discord.ext import commands, tasks
from discord_key import discord_bot_token

################################################################################
## Chemical element resource database from wikipedia/mendeleev python library ##
##                             for discord bot                                ##
###############################################################################
##    Search by element number, symbol,
##    list resources available
##    TODO: show basic info if no specificity in query
# created by : mr_hai on discord / flyingfishfuse on github
lookup_bot = commands.Bot(command_prefix=("."))
bot_permissions = 92160
devs = [712737412018733076]
cog_directory_files = os.listdir("./cogs")
load_cogs = False

bot_help_message = "I am a beta bot, right now all you can do is \"lookup\" \
    \"element\" \"type_of_data\"."

def function_failure_message(exception_message):
        import inspect
        return "something wierd happened in: " + inspect.currentframe().f_code.co_name + \
            "/n" + exception_message

# GLOBAL OUTPUT CONTAINER FOR FINAL CHECKS
global global_output_container 
global_output_container = []


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
    #await Element_lookup.format_and_print_output(global_output_container)
    await ctx.send(global_output_container)

#class Lookup_tool(commands.Cog):
#    def __init__(self, ctx, discord_arg1, discord_arg2):
#        print("asdf")
#    async def e_lookup():

class Element_lookup(commands.Cog):
    def __init__(self, ctx): #, input_container : list):
        #generate_element_name_list()
        #self.input_container  = input_container
        #self.output_container = []
        print("haha it runs the init but doesnt initialize! thanks discord!")
    
    async def help_message():
        return "Put the element's name, symbol, or atomic number followed \
    by either: physical, chemical, nuclear, ionization, isotopes, \
    oxistates"

    async def user_is_a_doofus_element_message():
        return "Stop being a doofus and feed the data on elements that I expect! "
        
    async def user_is_a_doofus_specific_message():
        return "Stop being a doofus and feed the data on specifics that I expect! "

    async def user_input_was_wrong(ctx, type_of_pebkac_failure : str):
        if type_of_pebkac_failure == "element":
            await ctx.send(Element_lookup.user_is_a_doofus_element_message)
        elif type_of_pebkac_failure == "specifics":
            await ctx.send(Element_lookup.user_is_a_doofus_specific_message)
        else:
            print(type_of_pebkac_failure)
 #           global global_output_container
 #           global_output_container.append(function_failure_message(Exception))

    async def validate_user_input(ctx, element_id_user_input, specifics_requested):
        from variables_for_reality import element_list , symbol_list , specifics_list
        #print(element_id_user_input)
        #print(specifics_requested)
        #print(specifics_list)
        #print(element_list)
        for each in (element_list, symbol_list):
            if any(user_input == element_id_user_input for user_input in each):
                #if element_id_user_input in range(1-118) or element_id_user_input == each:
                #if any(user_input == element_id_user_input for user_input in element_list) or \
                #    any(user_input == element_id_user_input for user_input in symbol_list):
                #(specifics_list)                
                    if any(user_input == specifics_requested for user_input in specifics_list):
                        if specifics_requested.lower()    == "physical":
                            print(element_id_user_input)
                            await Element_lookup.get_physical_properties(element_id_user_input)
                            #await Element_lookup.format_and_print_output(global_output_container)
                        elif specifics_requested.lower()  == "chemical":
                            await Element_lookup.get_chemical_properties(element_id_user_input)
                            #await Element_lookup.format_and_print_output(global_output_container)
                        elif specifics_requested.lower()  == "nuclear":
                            await Element_lookup.get_nuclear_properties(element_id_user_input)
                            #await Element_lookup.format_and_print_output(global_output_container)
                        elif specifics_requested.lower()  == "ionization":
                            await Element_lookup.get_ionization_energy(element_id_user_input)
                            #await Element_lookup.format_and_print_output(global_output_container)
                        elif specifics_requested.lower()  == "isotopes":
                            await Element_lookup.get_isotopes(element_id_user_input)
                            #await Element_lookup.format_and_print_output(global_output_container)
                        elif specifics_requested.lower()  == "oxistates":
                            await Element_lookup.get_oxistates(element_id_user_input)
                            #await Element_lookup.format_and_print_output(global_output_container)
                            # input given by user was NOT found in the validation data
                        else:
                            await Element_lookup.user_input_was_wrong(ctx, "specifics")
                            #await Element_lookup.format_and_print_output(global_output_container)
                    else:
                        await Element_lookup.user_input_was_wrong(ctx, "element")
                        #await Element_lookup.format_and_print_output(global_output_container)

    async def format_and_print_output(container_of_output: list):
        output_string = ""
        for each in container_of_output:
            output_string + each
        global global_output_container
        global_output_container = output_string

    async def compare_element_list(element_id_user_input, data_type : str, less_greater: str):
        element_data_list = []
        return_element_by_id = lambda element_id_input : mendeleev.element(element_id_input)
        element_to_compare   = return_element_by_id(element_id_user_input)
        for each in range(1,118):
            element_object = return_element_by_id(each)
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
            else :
                print("asdf")

    async def get_basic_information(element_id_user_input):
        """
        Returns some basic information about the element requested
        takes either a name,atomic number, or symbol
        """
        output_container = []
        element_object = mendeleev.element(element_id_user_input)
        output_container.append("Description: " + element_object.description  + "/n")
        output_container.append("Sources: " + element_object.sources  + "/n")

    async def get_history(element_id_user_input):
        """
        Returns some historical information about the element requested
        takes either a name,atomic number, or symbol
        """
        output_container = []
        element_object = mendeleev.element(element_id_user_input)
        output_container.append("Uses: " + element_object.uses        + "/n")
        output_container.append("Abundance in Crust" + element_object.abundance_crust + "/n")
        output_container.append("Abundance in Sea: " + element_object.abundance_sea + "/n")
        output_container.append("Discoveries: " + element_object.discoveries  + "/n")
        output_container.append("Discovery Location: " + element_object.discovery_location  + "/n")
        output_container.append("Discovery Year: " + element_object.discovery_year        + "/n")
        await Element_lookup.format_and_print_output(output_container)
        
    async def get_isotopes(element_id_user_input):
        """
        Returns Isotopes of the element requested
        """
        output_container = []
        element_object = mendeleev.element(element_id_user_input)
        output_container.append("Isotopes: " + element_object.isotopes + "/n")
        await Element_lookup.format_and_print_output(output_container)

    async def get_ionization_energy(element_id_user_input):
        """
        Returns Ionization energies of the element requested
        """
        output_container = []
        element_object = mendeleev.element(element_id_user_input)
        output_container.append("Ionization Energies: " + element_object.ionenergies  + "/n")
        await Element_lookup.format_and_print_output(output_container)

    async def get_physical_properties(element_id_user_input):
        """
        Returns physical properties of the element requested
        """
        output_container = []
        element_object = mendeleev.element(element_id_user_input)
        output_container.append("Hardness: "      + element_object.hardness      + "/n")
        output_container.append("Softness: "      + element_object.softness      + "/n")
        output_container.append("Boiling Point:"  + element_object.boiling_point + "/n")
        output_container.append("Melting Point:"  + element_object.melting_point + "/n")
        output_container.append("Specific Heat:"  + element_object.specific_heat + "/n")
        output_container.append("Thermal Conductivity:"  + element_object.thermal_conductivity + "/n")
        await Element_lookup.format_and_print_output(output_container)

    async def get_chemical_properties(element_id_user_input):
        """
        Returns Chemical properties of the element requested
        """
        output_container = []
        element_object = mendeleev.element(element_id_user_input)
        output_container.append("Electron Affinity: "    + element_object.electron_affinity  + "/n")
        output_container.append("Heat Of Formation: "    + element_object.heat_of_formation  + "/n")
        output_container.append("Heat Of Evaportation: " + element_object.evaporation_heat   + "/n")
        output_container.append("Electronegativity: "    + element_object.electronegativity  + "/n")
        output_container.append("Covalent Radius: "      + element_object.covalent_radius    + "/n")
        output_container.append("Polarizability: "       + element_object.dipole_polarizability  + "/n")
        await Element_lookup.format_and_print_output(output_container)

    async def get_nuclear_properties(element_id_user_input):
        """
        Returns Nuclear properties of the element requested
        """
        output_container = []
        element_object = mendeleev.element(element_id_user_input)
        output_container.append("Neutrons: " + element_object.neutrons  + "/n")
        output_container.append("Protons: "  + element_object.protons   + "/n")
        output_container.append("Atomic Radius: "  + element_object.atomic_radius  + "/n")
        output_container.append("Atomic Weight: "  + element_object.atomic_weight  + "/n")
        output_container.append("Radioactivity: "  + element_object.is_radioactive  + "/n")
        await Element_lookup.format_and_print_output(output_container)

    async def get_basic_element_properties(element_id_user_input):
        """
        takes either a name,atomic number, or symbol
        """
        output_container = []
        element_object = mendeleev.element(element_id_user_input)
        output_container.append("Element: "       + element_object.name          + "/n")
        output_container.append("Atomic Weight: " + element_object.atomic_weight + "/n")
        output_container.append("CAS Number: "    + element_object.cas           + "/n")
        output_container.append("Mass: "           + element_object.mass          + "/n")
        await Element_lookup.format_and_print_output(output_container)

lookup_bot.run(discord_bot_token, bot=True)
