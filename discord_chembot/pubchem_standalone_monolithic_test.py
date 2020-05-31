import os
import re
import csv

import chempy
import ionize
import asyncio
import inspect
import datetime
import itertools
import mendeleev
import threading
#import wikipedia
import math, cmath
from pprint import pprint
import pubchempy as pubchem
from chempy import mass_fractions
from flask_sqlalchemy import SQLAlchemy
from chempy import balance_stoichiometry
from flask import Flask, render_template, Response, Request ,Config

import colorama
from colorama import init
init()
from colorama import Fore, Back, Style
#Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
#Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
#Style: DIM, NORMAL, BRIGHT, RESET_ALL

def function_message(exception_message : str,  location="", color_to_print="red"):
    """
    A Robust exception message passing class? that uses colorama and inspect
    Takes red, green, blue as color arguments. WORK IN PROGERESS!
    """
    blueprint = lambda text: print(Fore.BLUE + ' ' +  text + ' ' + Style.RESET_ALL)
    greenprint = lambda text: print(Fore.GREEN + ' ' +  text + ' ' + Style.RESET_ALL)
    redprint = lambda text: print(Fore.RED + ' ' +  text + ' ' + Style.RESET_ALL)
    import inspect
    if color_to_print == "red":
        # gets name of object calling this function, the previous frame calling this object
        #f_back next outer frame object (this frame’s caller)

        #This code would be used INSIDE the function being tested
        #f_code code object being executed in this frame
        #inspect.currentframe().f_back.__base__
        redprint("something wierd happened in: "  + location)
        blueprint("\n" + exception_message)
    elif color_to_print == "green":
        greenprint("something wierd happened in: " + location)
        blueprint("\n" + exception_message)
    elif color_to_print == "blue":
        blueprint("something wierd happened in: " + location)
        blueprint("\n" + exception_message)
    blueprint("\n" + exception_message)


#make them global scope for testing purposes
show_line_number = lambda line: blueprint('line:' + inspect.getframeinfo(inspect.currentframe()).lineno)
blueprint = lambda text: print(Fore.BLUE + ' ' +  text + ' ' + Style.RESET_ALL)
greenprint = lambda text: print(Fore.GREEN + ' ' +  text + ' ' + Style.RESET_ALL)
redprint = lambda text: print(Fore.RED + ' ' +  text + ' ' + Style.RESET_ALL)


cas_regex = re.compile('\b[1-9]{1}[0-9]{1,5}-\d{2}-\d\b')
###############################################################################
## TESTING VARS
TESTING = True
#The sqlite :memory: identifier is the default if no filepath is present. 
# Specify sqlite:// and nothing else:
#e = create_engine('sqlite://')
TEST_DB = 'sqlite://'

pubchem_search_types = ["cas", "cid" , "name" ] #, "formula"]
###############################################################################

DATABASE_HOST      = "localhost"
DATABASE           = "chembot"
DATABASE_USER      = "admin"
DATABASE_PASSWORD  = "password"
SERVER_NAME        = "Discord Chemistry lookup tool"
HTTP_HOST          = "fihtbiscuits"
ADMIN_NAME         = "mr_hai"
ADMIN_PASSWORD     = "password"
ADMIN_EMAIL        = "game_admin" + "@" + HTTP_HOST
DANGER_STRING      = "TACOCAT"

LOCAL_CACHE_FILE   = 'sqlite:///' + DATABASE + DATABASE_HOST + DATABASE_USER + ".db"
easter_egg_string  = ["AuTiSTiC", "DyNAmITe", "HeLiCoPtEr", "SeNPaI", "HoOKErS ", "CoCaINe"]
################################################################################
##############                      CONFIG                     #################
################################################################################
SQLALCHEMY_TRACK_MODIFICATIONS = False

class Config(object):
    if TESTING == True:
        SQLALCHEMY_DATABASE_URI = TEST_DB
        #SQLALCHEMY_TRACK_MODIFICATIONS = True
    elif TESTING == False:
        SQLALCHEMY_DATABASE_URI = LOCAL_CACHE_FILE

try:
    chembot_server = Flask(__name__ , template_folder="templates" )
    chembot_server.config.from_object(Config)
    database = SQLAlchemy(chembot_server)
    database.init_app(chembot_server)
except Exception:
    function_message(Exception,"red")

###############################################################################
# from stack overflow
#In the second case when you're just restarting the app I would write a 
#test to see if the table already exists using the reflect method:

#db.metadata.reflect(engine=engine)

#Where engine is your db connection created using create_engine(), and see 
#if your tables already exist and only define the class if the table is undefined.

#this will clear the everything?
database.metadata.clear()

################################################################################
################################################################################
##############                      Models                     #################
################################################################################
# This is for caching any information that takes forever to grab
class Compound(database.Model):
    __tablename__       = 'Compound'
    __table_args__      = {'extend_existing': True}
    id                  = database.Column(database.Integer, \
                            index=True, \
                            primary_key = True, \
                            unique=True, \
                            autoincrement=True)
    cid                 = database.Column(database.String(128))
    name                = database.Column(database.String(64))
    cas                 = database.Column(database.String(64))
    smiles              = database.Column(database.Text)
    formula             = database.Column(database.String(120))

    def __repr__(self):
        return 'Compound: {} \n \
                CAS     : {} \n \
                Formula : {} \n '.format(self.name , self.cas, self.formula)

class Composition(database.Model):
    __tablename__       = 'Composition'
    __table_args__      = {'extend_existing': True}
    id                  = database.Column(database.Integer, \
                            index=True,                     \
                            primary_key = True,             \
                            unique=True,                    \
                            autoincrement=True)
    name                = database.Column(database.String(64))
    units               = database.Column(database.String(12))
    compounds           = database.Column(database.String(120))
    notes               = database.Column(database.String(256))

#{
#  "composition": "flash",
#  "units": "%wt",
#  "formula": {
#    "Al": 27.7,
#    "NH4ClO4": 72.3
#  }
#}
    def __repr__(self):
        list_to_string = lambda list_to_convert: ''.join(list_to_convert)
        formula_list = str.split(self.compounds, sep=",")
        print(formula_list)
        formula = ""
        def format_asdf():
            for each in formula_list:
            #catches the amount
                if list_to_string(each).isnumeric():
                    amount  = list_to_string(str(each))
                #catches the element/compound
                else:
                    compound = str(each)
                formula + '{} : {} {}'.format(compound, amount , "\n\t")
        return 'Composition: {} \n\
Units: {} \n\
Formula: {} \n\
Notes: {}'.format(self.name, self.units, formula, self.notes)

# dirty, dirty, chemistry

test_comp_notes = """
This is a test entry for the DB, it is a flash composition.
Remember, the finer the Aluminum, the faster the flash. 
"""

redprint("made it this far")
test_entry1 = Compound(name ='test', formula="HeNTaI" )
test_entry2 = Composition(name = "flash", units="%wt", compounds="Al,27.7,NH4ClO4,72.3", notes=test_comp_notes )
database.create_all()
database.session.add(test_entry1)
database.session.add(test_entry2)
database.session.commit()
#chembot_server.run()


################################################################################
##############                     FUNCTIONS                   #################
################################################################################

def Compound_by_id(cid_of_compound):
    """
    Returns a compound from the local DB
    Returns FALSE if entry does not exist

    """
    print(inspect.stack()[1][3])
    try:

        return Compound.query.all.filter_by(id = cid_of_compound).first()
    except Exception:
        function_message("compound by cid local db" , Exception, "red")
        return False
    
################################################################################
def internal_local_database_lookup(entity : str, id_of_record:str ):
    """
    feed it a formula or CID followed buy "formula" or "cid"
    Returns False and raises and exception/prints exception on error
    Returns an SQLAlchemy database object if record exists
    Don't forget this is for compounds only!
    """
    print(inspect.stack()[1][3])

    try:
        if id_of_record    == "cid":
            lookup_result  = Compound.query.filter_by(cid=entity).first()
            blueprint(lookup_result)
        elif id_of_record  == "name":
            lookup_result  = Compound.query.filter_by(name=entity).first()
            blueprint(lookup_result)
        elif id_of_record  == "cas":
            lookup_result  = Compound.query.filter_by(cas=entity).first()
            blueprint(lookup_result)
    except Exception:
        function_message("internal lookup" , Exception, "red")
        return False
    finally:
        return lookup_result
    
def add_to_db(thingie):
    """
    Takes SQLAchemy Class_model Objects 
    For updating changes to Class_model.Attribute using the form:

        Class_model.Attribute = some_var 
        add_to_db(some_var)

    """
    try:
        database.session.add(thingie)
        database.session.commit
    except Exception:
        function_message(Exception, "red")
################################################################################

def update_db():
    """
    DUH
    """
    try:
        database.session.commit()
    except Exception:
        function_message(Exception, "red")

###############################################################################

def dump_db():
    """
Prints database to screen
    """
    redprint("-------------DUMPING DATABASE------------")
    records1 = database.session.query(Compound).all()
    records2 = database.session.query(Composition).all()
    for each in records1, records2:
        print (each)
    redprint("------------END DATABASE DUMP------------")

###############################################################################

def dump_compositions():
    """
Prints database to screen
    """
    redprint("-------------DUMPING COMPOSITIONS------------")
    records = database.session.query(Composition).all()
    for each in records:
        print (each)
    redprint("--------------END DATABASE DUMP--------------")

###############################################################################

def dump_compounds():
    """
Prints database to screen
    """
    redprint("-------------DUMPING COMPOUNDS------------")
    records = database.session.query(Compounds).all()
    for each in records:
        print (each)
    redprint("-------------END DATABASE DUMP------------")

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
            "Stop being a doofus and feed me a good CID! "
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
    
    async def validate_user_input(user_input: str, type_of_input:str):
        """
    User Input is expected to be the proper identifier.
        only one input, we are retrieving one record for one entity
    
    Remove self and async from the code to transition to non-discord
        """
        import inspect
        temp_output_container = []
        ######################################################
        # if CAS
        if type_of_input == "cas":
            greenprint("user supplied a CAS")
            try:
                #regex for a CAS number
                # if good
                greenprint("trying to match regular expression for CAS")
                if re.match(cas_regex,user_input):
                    greenprint("GOOD CAS NUMBER")
                    print(Pubchem_lookup.pubchem_lookup_by_name_or_CID(user_input))
                    show_line_number()
                    #returns an SQLAlchemy object or false
                    internal_lookup = internal_local_database_lookup(user_input, "cas")
                    print(internal_lookup + "step 1")
                    # NOT IN THE LOCAL DB
                    if internal_lookup == False:
                        redprint("============Internal Lookup returned FALSE===========")
                        blueprint("Performing a PubChem lookup")
                        # every good lookup will add an entry to the db and return 
                        # the local db entry... two queries... gotta fix that...
                        print(Pubchem_lookup.pubchem_lookup_by_name_or_CID(user_input))
                        lookup_object = Pubchem_lookup.pubchem_lookup_by_name_or_CID(user_input, "cas")
                        formatted_message = Pubchem_lookup.format_message_discord(lookup_object)
                        # output is now formatted Discord.Embed() object
                        # in list in list
                        # [ [lookup_object] ]
                        ctx.send(lookup_object)
                        temp_output_container.append([formatted_message])
                        #global lookup_output_container
                        lookup_output_container = temp_output_container
                    #IN THE LOCAL DB
                    elif internal_lookup == True:
                        greenprint("============Internal Lookup returned TRUE===========")
                        print(internal_lookup)
                        formatted_message = Pubchem_lookup.format_message_discord(internal_lookup)
                        temp_output_container.append([formatted_message])
                        ##global lookup_output_container
                        lookup_output_container = temp_output_container
                        dump_db()
                    else:
                        function_message("reached an else", "validation CAS lookup checks", "red") 
                else:
                    function_message("reached second else ","validation CAS lookup checks", "red")                    
            except Exception:
                function_message(Exception, " reached the exception", "red") 
 ##############################################################################
#if CID
        if type_of_input == "cid":
            greenprint("user supplied a CID")
            try:
                internal_lookup = internal_local_database_lookup(user_input, "cid")
                if internal_lookup == False:
                    redprint("============Internal Lookup returned FALSE===========")
                    lookup_object = Pubchem_lookup.pubchem_lookup_by_name_or_CID(user_input, "cid")
                    formatted_message = Pubchem_lookup.format_message_discord(lookup_object)
                    temp_output_container.append([formatted_message])
                    ##global lookup_output_container
                    lookup_output_container = temp_output_container
                elif internal_lookup:
                    greenprint("============Internal Lookup returned TRUE===========")
                    formatted_message = Pubchem_lookup.format_message_discord(internal_lookup)
                    temp_output_container.append([formatted_message])
                    #global lookup_output_container
                    lookup_output_container = temp_output_container
                    dump_db()
                else:
                    function_message("cid - main loop, else at end", "red")
            except Exception:
                function_message(Exception, "cid - main loop", "blue") 
###############################################################################
# if NAME
        if type_of_input == "name":
            greenprint("user supplied a name")
            try:
                blueprint("[+] attempting internal lookup")
                internal_lookup = internal_local_database_lookup(user_input, "name")
                if internal_lookup == False:
                    redprint("============Internal Lookup returned false===========")
                    lookup_object = Pubchem_lookup.pubchem_lookup_by_name_or_CID(user_input, "name")
                    formatted_message = Pubchem_lookup.format_message_discord(lookup_object)
                    temp_output_container.append([formatted_message])
                    #global lookup_output_container
                    lookup_output_container = temp_output_container
                elif internal_lookup:
                    greenprint("============Internal Lookup returned TRUE===========")
                    formatted_message = Pubchem_lookup.format_message_discord(internal_lookup)
                    temp_output_container.append([formatted_message])
                    #global lookup_output_container
                    lookup_output_container = temp_output_container
                    dump_db()
                else:
                    function_message("validation lookup checks", "red")
            except Exception:
                function_message(Exception, "blue") 
###############################################################################
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
            try:
                lookup_results = pubchem.get_compounds(compound_id,'name')
            except Exception :# pubchem.PubChemPyError:
                function_message("lookup by cid exception - name", Exception, "red")
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
                function_message("lookup by cid exception - cid", Exception, "red")
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
                function_message("lookup by cid exception - CAS", Exception, "red")            
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
                function_message("PUBCHEM LOOKUP BY CID","ELSE AT THE END", "red")
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
        print(inspect.stack()[1][3])

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
    async def format_message_discord(lookup_results_object):
        greenprint(inspect.stack()[1][3])
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
    #user_input_reactants = "NH4ClO4,Al"
    #user_input_products  = "Al2O3,HCl,H2O,N2"
    #equation_user_input  = "NH4ClO4,Al=>Al2O3,HCl,H2O,N2"
#    reactants =  {'NH4ClO4', 'Al'} 
#    products  =  {'Al2O3', 'HCl', 'H2O', 'N2'}

    
    formula_list1 , formula_list2 = []
    reactants  = str.split(parsed_equation[0], sep =",")
    products   = str.split(parsed_equation[1], sep =",")
    for each in reactants:
        formula_list1.append(chempy.Substance(each))
    for each in products:
        formula_list2.append(chempy.Substance(each))
        test_entity1 = chempy.Substance.from_formula(formula_input)
        test_entity2 = chempy.Substance.from_formula
        function_message(test_entity1, "red")
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
   
    #THIS CODE IS FOR LATER WHEN I WORK ON 
    # ADVANCED BALANCING
    #check the DB for the reactants
    #for each in user_input_reactants:
        #local_db_query = internal_local_database_lookup(each, "formula")
        #it was in the database
        #if local_db_query == True:
        #    return local_db_query
        #it was not in the database
        #elif local_db_query ==False:
        #    function_message("local db query returned NEGATIVE", "red")
        #    Pubchem_lookup.pubchem_lookup_by_name_or_CID(each)

