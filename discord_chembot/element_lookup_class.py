# -*- coding: utf-8 -*-
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
################################################################################

from variables_for_reality import *
import mendeleev
#list_of_resources = "https://en.wikipedia.org/wiki/List_of_data_references_for_chemical_elements"
#data_pages_list   = "https://en.wikipedia.org/wiki/Category:Chemical_element_data_pages"
# https://chemspipy.readthedocs.io/en/latest/

class Element_lookup():
    def __init__(self, element_id_user_input: str or int, specifics_requested : str):
        #self.element_id_user_input = element_id_user_input
        #self.specifics_requested   = specifics_requested
        #self.validate_user_input(self.element_id_user_input, self.specifics_requested)
        print("wat")

    def help_message():
        return "Put the element's name, symbol, or atomic number followed \
by either: basic, historical, physical, chemical, nuclear, ionization, \
isotopes, oxistates\n "
        
    def reply_to_query(message):
        '''
     assigns to lookup_output_container.
        '''
        # Takes a list or string, if list, joins the list to a string and
        #list_to_string = lambda list_to_convert: ''.join(list_to_convert)
        #if isinstance(message,list):
        #    message = list_to_string(message) 
        #temp_array = [message]
        global lookup_output_container
        lookup_output_container.append(message)
        
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

    def validate_user_input(element_id_user_input: str or int, specifics_requested : str):
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
        # you extend this when you add more functions
        # this is the function list
        #it should be refactored... I know... yes its badcode
        ## i plan on it
        if element_valid and specifics_valid == True:      
            #global lookup_output_container
            if specifics_requested    == "basic":
                Element_lookup.get_basic_element_properties(element_id_user_input)
                # so now you got the basic structure of the control loop!
            elif specifics_requested  == "historical":
                Element_lookup.get_history(element_id_user_input)
            elif specifics_requested  == "physical":
                Element_lookup.get_physical_properties(element_id_user_input)
            elif specifics_requested  == "chemical":
                Element_lookup.get_chemical_properties(element_id_user_input)
            elif specifics_requested  == "nuclear":
                Element_lookup.get_nuclear_properties(element_id_user_input)
            elif specifics_requested  == "ionization":
                Element_lookup.get_ionization_energy(element_id_user_input)
            elif specifics_requested  == "isotopes":
                Element_lookup.get_isotopes(element_id_user_input)
            elif specifics_requested  == "oxistates":
                Element_lookup.get_oxistates(element_id_user_input)
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
    def compare_element_list(element_id_user_input, data_type : str, less_greater: str):
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
        #global lookup_output_container
        temp_output_container = []
        element_object = mendeleev.element(element_id_user_input)
        temp_output_container.append("Uses: " + element_object.uses        + "\n")
        temp_output_container.append("Abundance in Crust" + str(element_object.abundance_crust) + "\n")
        temp_output_container.append("Abundance in Sea: " + str(element_object.abundance_sea) + "\n")
        temp_output_container.append("Discoveries: " + element_object.discoveries  + "\n")
        temp_output_container.append("Discovery Location: " + element_object.discovery_location  + "\n")
        temp_output_container.append("Discovery Year: " + str(element_object.discovery_year)        + "\n")
        #global lookup_output_container
        #lookup_output_container.append(temp_output_container)
        Element_lookup.reply_to_query(lookup_output_container)

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
        #global lookup_output_container
        #lookup_output_container.append(temp_output_container)
        Element_lookup.reply_to_query(lookup_output_container)

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
        #global lookup_output_container
        #lookup_output_container.append(temp_output_container)
        Element_lookup.reply_to_query(lookup_output_container)

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
        #global lookup_output_container
        #lookup_output_container.append(temp_output_container)
        Element_lookup.reply_to_query(temp_output_container)

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
        #global lookup_output_container
        #lookup_output_container.append(temp_output_container)
        Element_lookup.reply_to_query(temp_output_container)

###############################################################################
    
    def get_isotopes(element_id_user_input):
        """
        Returns Isotopes of the element requested
        """
        temp_output_container = []
        element_object = mendeleev.element(element_id_user_input)
        temp_output_container.append("Isotopes: " + str(element_object.isotopes) + "\n")
        #global lookup_output_container
        #lookup_output_container.append(temp_output_container)
        Element_lookup.reply_to_query(temp_output_container)
        
###############################################################################

    def get_ionization_energy(element_id_user_input):
        """
        Returns Ionization energies of the element requested
        """
        temp_output_container = []
        element_object = mendeleev.element(element_id_user_input)
        temp_output_container.append("Ionization Energies: " + str(element_object.ionenergies)  + "\n")
        #global lookup_output_container
        #lookup_output_container.append(temp_output_container)
        Element_lookup.reply_to_query(temp_output_container)