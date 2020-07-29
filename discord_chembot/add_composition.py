#!/usr/bin/python3
#step one: slap a license on it
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


####################################################################################
# This is not a tutorial, this is only a tribute to the 
# greatest tutorial in the world
###################################################################################

# basic imports for a module, color print not required
#from variables_for_reality import greenprint,redprint,blueprint
from variables_for_reality import lookup_input_container, lookup_output_container
from database_setup import Database_functions,Compound,Composition,TESTING
from equation_balancer import EquationBalancer
from pubchem_test import Pubchem_lookup
####################################################################################
# module imports for functionality
###################################################################################
import sys
import chempy
import math, cmath
from chempy import balance_stoichiometry, mass_fractions

class AddComposition():
    '''
Adds a composition to database from user input.
Performs pubchem queries on each of the compounds in the compositions
and adds database entries for each. while also calculating the products
of reaction and storing the result of that.
    '''
    #we dont have to do class methods and it makes it easier not to in this 
    #particular instance, notice the standalone versions have "self" instead
    def __init__(self):
        #super().__init__()
        print("nope")
    
    #every module gets a help message
    def help_message():
        return """ asdf help message goes here"""

    # every module has this reply function
    def reply_to_query(message_object):
        '''    
        Just accepts an object of your choice, then you import the 
        lookup_output_container to your main file and work in that file

        The commented out code is for turning everything to a string
        from a list or string for inline formatting
        maybe do a bool in the input to switch between one or the other
        ''' 
        #list_to_string = lambda list_to_convert: ''.join(list_to_convert)
        #if isinstance(message,list):
        #    message = list_to_string(message) 
        #temp_array = [message]
        global lookup_output_container
        lookup_output_container.append(message_object)
        if TESTING == True:
            blueprint("=============================================")
            greenprint("[+] Sending the following reply to output container")
            print(lookup_output_container)
            blueprint("=============================================")

    #every module has a validation function for the user input
    def validate_user_input(comp_name : str , units : str , formula : str ,info : str):
        '''
        "units" is a string:
        Note the lack of spaces and the slash
        "formula" is in the form of :
            compound,int
            where "compound" is either a molecule, element, or name of arbitrary compound
                The molecule can be an iupac_name or symbolic
                The element is the iupac_name or symbolic
                Arbitrary compound is a string
        
        '''
        #validate each input term to make sure it conforms to spec
        #make sure the units are in the form int/unit
        #e.g. : 12/grams
        try:
            split_units = units.split("/")
            if isinstance(units.split("/"), list) and (units[0] == int and units[1] == str):

                pass
            else :
                AddComposition.reply_to_query("units were formatted wrong")
        if isinstance(,):

            pass
        if isinstance(,):

            pass

        Database_functions.composition_to_database(composition_name,\
                                                   units_used      ,\
                                                   formula_list    ,\
                                                   informational_paragraph)
        pass
    