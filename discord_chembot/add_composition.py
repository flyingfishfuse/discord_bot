
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

# basic imports for a module, color print not required
#from variables_for_reality import greenprint,redprint,blueprint
from variables_for_reality import lookup_input_container, lookup_output_container
from database_setup import Database_functions,Compound,Composition,TESTING
from equation_balancer import EquationBalancer
####################################################################################
# module imports for functionality, this can include local library functions
###################################################################################
import sys
import math, cmath
import chempy
from chempy import balance_stoichiometry, mass_fractions


#we dont have to do class methods and it makes it easier not to in this 
#particular instance, notice the standalone versions have "self" instead
class AddComposition():
    '''
Adds a composition to database from user input.
Performs pubchem queries on each of the compounds in the compositions
and adds database entries for each. while also calculating the products
of reaction and storing the result of that.
    '''
    def __init__(self):
        #super().__init__()
        print("nope")
    
    #every module gets a help message
    def help_message():
        return """ asdf help message goes here"""

    #every module has a validation function for the user input
    def validate_user_input(comp_name,units,formula,info):
        #validate each input term to make sure it conforms to spec
        if isinstance(comp_name, str):
            #do thing
            pass
        
        Database_functions.composition_to_database(composition_name,\
                                                   units_used      ,\
                                                   formula_list    ,\
                                                   informational_paragraph)
        pass
    