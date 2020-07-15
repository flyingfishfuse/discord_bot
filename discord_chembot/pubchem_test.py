import mendeleev
import asyncio
import os
from flask import Flask, render_template, Response, Request ,Config
from flask_sqlalchemy import SQLAlchemy
from variables_for_reality import *
import re
import chempy
import datetime
import math, cmath
import pubchempy as pubchem






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
        #global lookup_output_container
        temp_output_container = []
        element_object = mendeleev.element(element_id_user_input)
        temp_output_container.append("Uses: " + element_object.uses        + "\n")
        temp_output_container.append("Abundance in Crust" + str(element_object.abundance_crust) + "\n")
        temp_output_container.append("Abundance in Sea: " + str(element_object.abundance_sea) + "\n")
        temp_output_container.append("Discoveries: " + element_object.discoveries  + "\n")
        temp_output_container.append("Discovery Location: " + element_object.discovery_location  + "\n")
        temp_output_container.append("Discovery Year: " + str(element_object.discovery_year)        + "\n")
        #await Element_lookup.format_and_print_output(output_container)
        lookup_output_container = temp_output_container

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
        #global lookup_output_container
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
        #global lookup_output_container
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
        #global lookup_output_container
        lookup_output_container = temp_output_container

###############################################################################

    def get_ionization_energy(element_id_user_input):
        """
        Returns Ionization energies of the element requested
        """
        temp_output_container = []
        element_object = mendeleev.element(element_id_user_input)
        temp_output_container.append("Ionization Energies: " + str(element_object.ionenergies)  + "\n")
        #global lookup_output_container
        lookup_output_container = temp_output_container
        
        
        

class Pubchem_lookup():
    '''
Class to perform lookups on CID's and IUPAC names
Also does chempy translation to feed data to the calculation engine
    '''
    def __init__(self, user_input, type_of_input):
        self.user_input     = user_input
        self.type_of_input  = type_of_input
        self.validate_user_input(self.user_input , self.type_of_input)

    def balancer_help_message(self):
        return " Reactants and Products are Comma Seperated Values using"+\
        "symbolic names for elements e.g. \n "        +\
        "user input for reactants => NH4ClO4,Al \n"   +\
        "user input for products  => Al2O3,HCl,H2O,N2 \n"

    def help_message(self):
        return """
input CID/CAS or IUPAC name or synonym
Provide a search term and "term type", term types are "cas" , "name" , "cid"
Example 1 : .pubchemlookup methanol name
Example 2 : .pubchemlookup 3520 cid
Example 3 : .pubchemlookup 113-00-8 cas
"""
###############################################################################
    def reply_to_query(self, message):
        '''    Takes a list or string, if list, joins the list to a string and assigns to 
    lookup_output_container.
        ''' 
        list_to_string = lambda list_to_convert: ''.join(list_to_convert)
        if isinstance(message,list):
            message = list_to_string(message) 
        temp_array = [message]
        lookup_output_container = temp_array
        print(lookup_output_container) 

###############################################################################
    def parse_lookup_to_chempy(self, pubchem_lookup : list):
        '''
        creates a chempy something or other based on what you feed it
        like cookie monster
        '''
        #lookup_cid       = pubchem_lookup[0].get('cid')
        lookup_formula    = pubchem_lookup[1].get('formula')
        #lookup_name      = pubchem_lookup[2].get('name')
        try:
            greenprint(chempy.Substance.from_formula(lookup_formula))
        except Exception:
            function_message("asdf", "blue")
###############################################################################

    def user_input_was_wrong(self, type_of_pebkac_failure : str, bad_string = ""):
        """
        You can put something funny here!
            This is something the creator of the bot needs to modify to suit
            Thier community.
        """
        user_is_a_doofus_CID_message        = 'Stop being a doofus! Accepted types are "name","cas" or "cid" '
        user_is_a_doofus_input_id_message   = 'bloop '
        user_is_a_doofus_formula_message    = "Stop being a doofus and feed me a good formula!"
        user_is_a_doofus_form_react_message = "the following input was invalid: " + bad_string 
        user_is_a_doofus_form_prod_message  = "the following input was invalid: " + bad_string
        #user_is_a_doofus_form_gen_message  = "the following input was invalid: " + bad_string
        if type_of_pebkac_failure   == "pubchem_lookup_by_name_or_CID":
            self.reply_to_query(user_is_a_doofus_CID_message)
        elif type_of_pebkac_failure == "specifics":
            self.reply_to_query(user_is_a_doofus_formula_message)
        elif type_of_pebkac_failure == "formula_reactants":
            self.reply_to_query(user_is_a_doofus_form_react_message)
        elif type_of_pebkac_failure == "formula_products":
            self.reply_to_query(user_is_a_doofus_form_prod_message)
        elif type_of_pebkac_failure == "user_input_identification":
            self.reply_to_query(user_is_a_doofus_input_id_message)
        else:
            #change this to sonething reasonable
            self.reply_to_query(type_of_pebkac_failure)

    def lookup_failure(self, type_of_failure: str):
        """
        does what it says on the label, called when a lookup is failed
        """
        #TODO: find sqlalchemy exception object
        # why cant I find the type of object I need fuck me
        if type_of_failure == "SQL":
            ##global lookup_output_container
            lookup_output_container = ["SQL QUERY FAILURE"]
        elif type_of_failure == pubchem.PubChemPyError:
            ##global lookup_output_container
            lookup_output_container = ["chempy failure"]
        pass
    
    def internal_local_database_lookup(self, entity : str, id_of_record:str ):
        if id_of_record in pubchem_search_types:
            lookup_result  = Compound.query.all().filter_by(id_of_record = entity).first()
            return lookup_result

    def validate_user_input(self, user_input: str, type_of_input:str):
        """
    User Input is expected to be the proper identifier.
        only one input, we are retrieving one record for one entity
    
    Remove self and async from the code to transition to non-discord
        """
        import re
        #cas_regex = re.compile('[1-9]{1}[0-9]{1,5}-\d{2}-\d')
        temp_output_container = []
        input_types_requestable = ["name", "cid", "cas"]
        fuck_this = lambda fuck: fuck in input_types_requestable 
        if fuck_this(type_of_input) :#in input_types_requestable:
            greenprint("user supplied a : " + type_of_input)
            try:
                if type_of_input == "cas":
                    try:
                        greenprint("[+} trying to match regular expression for CAS")
                        if re.match(cas_regex,user_input):
                            greenprint("[+] Good CAS Number")
                            internal_lookup = internal_local_database_lookup(user_input, type_of_input)
                            if internal_lookup == None or False:
                                redprint("[-] Internal Lookup returned false")
                                lookup_object = self.pubchem_lookup_by_name_or_CID(user_input, type_of_input)
                                self.reply_to_query(lookup_object)
                            elif internal_lookup == True:
                                greenprint("============Internal Lookup returned TRUE===========")
                                self.reply_to_query(lookup_object)
                        else:
                            function_message("[-] Bad CAS Number validation CAS lookup checks", "red")                    
                    except Exception:
                        function_message('[-] Something happened in the try/except block for cas numbers', 'red')
                else:
                    try:
                        internal_lookup = self.internal_local_database_lookup(user_input, type_of_input)
                        if internal_lookup == NoneType or False:
                            redprint("[-] Internal Lookup returned false")
                            lookup_object = self.pubchem_lookup_by_name_or_CID(user_input, type_of_input)
                            self.reply_to_query(lookup_object)
                        elif internal_lookup == True:
                            greenprint("============Internal Lookup returned TRUE===========")
                            self.reply_to_query(lookup_object)
                        else:
                            function_message("[-] Something is wrong with the database", "red")
                    except Exception:
                        function_message("reached exception : name/cid lookup - control flow", "red")
            except Exception:
                function_message("reached the exception : input_type was wrong somehow" , "red")

        else:
            self.user_input_was_wrong("user_input_identification", user_input + " : " + type_of_input)

  

    def pubchem_lookup_by_name_or_CID(self, compound_id, type_of_data:str):
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
        # you get multiple records returned from a pubchem search VERY often
        # so you have to choose the best one to store, This needs to be 
        # presented as an option to the user,and not programmatically 
        return_index = 0
        data = ["name","cid","cas"]
        if type_of_data in data:
            if type_of_data == ("name" or "cas"):                     
                try:
                    greenprint("[+] Performing Pubchem Query")
                    lookup_results = pubchem.get_compounds(compound_id,'name')
                except Exception :# pubchem.PubChemPyError:
                    function_message("lookup by NAME/CAS exception - name", "red")
                    self.user_input_was_wrong("pubchem_lookup_by_name_or_CID")
            elif type_of_data == "cid":
                try:
                    greenprint("[+] Performing Pubchem Query")
                    lookup_results = pubchem.Compound.from_cid(compound_id)
                except Exception :# pubchem.PubChemPyError:
                    function_message("lookup by NAME/CAS exception - name", "red")
                    self.user_input_was_wrong("pubchem_lookup_by_name_or_CID")
                #once we have the lookup results, do something
            if isinstance(lookup_results, list):# and len(lookup_results) > 1 :
                greenprint("[+] Multiple results returned ")
                for each in lookup_results:
                    redprint(each.molecular_formula)
                    query_appendix = [{'cid' : each.cid                 ,\
                            #dis bitch dont have a CAS NUMBER!
                            #'cas'       : each.cas                 ,\
                            'smiles'     : each.isomeric_smiles     ,\
                            'formula'    : each.molecular_formula   ,\
                            'molweight'  : each.molecular_weight    ,\
                            'charge'     : each.charge              ,\
                            'iupac_name' : each.iupac_name          }]
                    return_relationships.append(query_appendix)
                    ####################################################
                    #Right here we need to find a way to store multiple records
                    # and determine the best record to store as the main entry
                    ####################################################
                    #compound_to_database() TAKES A LIST
                    # first element of first element
                    #[ [this thing here] , [not this one] ]
                    redprint("=========RETURN RELATIONSHIPS=======multiple")
                    blueprint(str(return_relationships[return_index]))
                    redprint("=========RETURN RELATIONSHIPS=======multiple")
                    compound_to_database(return_relationships[return_index])
            
            # if there was only one result or the user supplied a CID for a single chemical
            elif isinstance(lookup_results, pubchem.Compound) :#\
              #or (len(lookup_results) == 1 and isinstance(lookup_results, list)) :
                greenprint("[+] One Result Returned!")
                query_appendix = [{'cid' : lookup_results.cid                 ,\
                            #'cas'       : lookup_results.cas                 ,\
                            'smiles'     : lookup_results.isomeric_smiles     ,\
                            'formula'    : lookup_results.molecular_formula   ,\
                            'molweight'  : lookup_results.molecular_weight    ,\
                            'charge'     : lookup_results.charge              ,\
                            'iupac_name' : lookup_results.iupac_name          }]
                return_relationships.append(query_appendix)
                redprint("=========RETURN RELATIONSHIPS=======")
                blueprint(str(return_relationships[return_index]))
                redprint("=========RETURN RELATIONSHIPS=======")
                compound_to_database(return_relationships[return_index])

            else:
                function_message("PUBCHEM LOOKUP BY CID : ELSE AT THE END", "red")
        #and then, once all that is done return the LOCAL database entry to
        # the calling function so this is just an API to the db code
        return_query = return_relationships[return_index]
        redprint("==BEGINNING==return query for pubchem/local lookup===========")
        query_cid    = return_query[0].get('cid')
        local_query  = Compound.query.filter_by(cid = query_cid).first()
        # you can itterate over the database query
        for each in local_query:
            blueprint(str(each) + "\n")
        redprint("=====END=====return query for pubchem/local lookup===========")

        #after storing the lookup to the local database, retrive the local entry
        #This returns an SQLALchemy object
        print(Compound_by_id(query_cid))
        return Compound_by_id(query_cid)

        # OR return the remote lookup entry, either way, the information was stored.
        #this returns a pubchempy.Compound() Object type
        #return lookup_results

Pubchem_lookup("420","cid")
Pubchem_lookup("methanol","name")
Pubchem_lookup("phenol","name")
