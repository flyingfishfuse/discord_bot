
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
from variables_for_reality import function_message
from variables_for_reality import greenprint,redprint,blueprint
from variables_for_reality import lookup_input_container, lookup_output_container
from variables_for_reality import scale_converter_unit_list
from database_setup import Database_functions,Compound,Composition,TESTING

####################################################################################
# module imports
###################################################################################
import sys
import math, cmath
import chempy
from chempy import balance_stoichiometry, mass_fractions
from variables_for_reality import pi,Vbe
from pubchem_test import Pubchem_lookup
#do thnigs with this , this seems nice
import pyEQL

# FORMULA RULES

Formula_entry_rules = '''

How to Enter Valid Chemical Formulas

Generally speaking, type the chemical formula of your solute the “normal” way and pyEQL should be able to inerpret it. Here are some examples:

    Sodium Chloride    - NaCl
    Sodium Sulfate     - Na(SO4)2
    Methanol           - CH4OH or CH5O
    Magnesium Ion      - Mg+2
    Chloride Ion       - Cl-

Formula Rules:

    *  Are composed of valid atomic symbols that start with capital letters
    
    *  Contain no non-alphanumeric characters other than ‘(‘, ‘)’, ‘+’, or ‘-‘
    
    *  If a ‘+’ or ‘-‘ is present, the formula must contain ONLY ‘+’ or ‘-‘ (e.g. ‘Na+-‘ is invalid) and the formula must end with either a series of charges (e.g. ‘Fe+++’) or a numeric charge (e.g. ‘Fe+3’)
    
    *  Formula must contain matching numbers of ‘(‘ and ‘)’
    
    *  Open parentheses must precede closed parentheses

'''

class EquationBalancer():
    def _init_(self):
        print("asdf wat")

    def validate_formula_input(self, equation_user_input : str):
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
        #equation_user_input  = "NH4ClO4,Al => Al2O3,HCl,H2O,N2"

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
                    chempy.Substance(each)
                except Exception:
                    function_message("reactants contents",Exception , "red")
                    Pubchem_lookup.user_input_was_wrong("formula_reactants", each)  
                #validate products contents
            for each in user_input_products:
                try:
                    chempy.Substance(each)
                except Exception:
                    function_message("products contents",Exception , "red")
                    Pubchem_lookup.user_input_was_wrong("formula_products", each)
        # if the inputs passed all the checks
        # RETURN THE REACTANTS AND THE PRODUCTS AS A LIST
        # [ [reactants] , [products] ]
            #return [user_input_reactants, user_input_products]
            self.balance_simple_equation(user_input_reactants, user_input_products)
        except Exception:
            function_message("formula validation exception", Exception, "red")
            Pubchem_lookup.user_input_was_wrong("formula_general", equation_user_input)


    def balance_simple_equation(self, reactants, products):
        #react = chempy.Substance.from_formula(reactants)
        #prod  = chempy.Substance.from_formula(products)
        balanced_reaction = chempy.balance_stoichiometry(reactants,products)
        print(balanced_reaction)
        self.reply_to_query(balanced_reaction)


    def reply_to_query(self, message):
        '''
        Assigns to lookup_output_container.
        ''' 
        #list_to_string = lambda list_to_convert: ''.join(list_to_convert)
        #if isinstance(message,list):
        #    message = list_to_string(message) 
        temp_array = [message]
        global lookup_output_container
        lookup_output_container = temp_array
