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
"""
PubChemPy caching wrapper

Caching extension to the Python interface for the PubChem PUG REST service.

https://github.com/mcs07/PubChemPy
"""


__author__  = 'Adam Galindo'
__email__   = 'null@null.com'
__version__ = '1'
__license__ = 'GPLv3'
__name__    = "pubchem_caching_wrapper"

import platform
OS_NAME = platform.system()

import os
import re
import csv
import lxml
import requests
import pubchempy as pubchem
from bs4 import BeautifulSoup
from requests.utils import requote_uri
from flask import Flask, render_template, Response, Request ,Config
from flask_sqlalchemy import SQLAlchemy
#from discord_chembot.variables_for_reality import \
#    greenprint,redprint,blueprint,function_message

###############################################################################
# TESTING STUFF
#do a search for if TESTING == True 
# to find the testing blocks
###############################################################################
import colorama
from colorama import init
init()
from colorama import Fore, Back, Style
#Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
#Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
#Style: DIM, NORMAL, BRIGHT, RESET_ALL

TESTING = True
#TESTING = False
#The sqlite :memory: identifier is the default if no filepath is present. 
# Specify sqlite:// and nothing else:
#e = create_engine('sqlite://')
TEST_DB = 'sqlite://'

#TESTING colored print functions
# ok so according to some website on the internet (professional, I know)
# https://thispointer.com/python-how-to-use-if-else-elif-in-lambda-functions/
# You can do THIS:
# lambda <args> : <return Value> if <condition > ( <return value > if <condition> else <return value>)
# make them global scope for testing purposes

# this one is used inline to convert lists top strings in front of print functions
list_to_string = lambda list_to_convert: ''.join(list_to_convert)
# so it prints to screen as a return "value" IF it's in "test mode" but returns NONE if test mode is off
blueprint = lambda text: print(Fore.BLUE + ' ' +  text + ' ' + Style.RESET_ALL) if (TESTING == True) else None
greenprint = lambda text: print(Fore.GREEN + ' ' +  text + ' ' + Style.RESET_ALL) if (TESTING == True) else None
redprint = lambda text: print(Fore.RED + ' ' +  text + ' ' + Style.RESET_ALL) if (TESTING == True) else None

################################################################################
# Random stuff 
################################################################################

# Filter None values from kwargs
# kwargs = dict((k, v) for k, v in kwargs.items() if v is not None)

#  Stackoverflow of course.
# >>> lod = [{1: "a"}, {2: "b"}]
# >>> any(1 in d for d in lod) 
# >>> True
GRAB_DESCRIPTION = True

# GLOBAL OUTPUT CONTAINER FOR FINAL CHECKS
global lookup_output_container 
lookup_output_container = []

# GLOBAL INPUT CONTAINER FOR USER INPUT VALIDATION
global lookup_input_container
lookup_input_container = []

################################################################################
##############                      CONFIG                     #################
################################################################################

# pubchem REST API service
pubchem_search_types = ["iupac_name", "cid", "cas"]
API_BASE_URL         = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug'

DATABASE_HOST      = "localhost"
DATABASE           = "chembot"
DATABASE_USER      = "admin"
DATABASE_PASSWORD  = "password"
SERVER_NAME        = "Discord Chemistry lookup tool"
LOCAL_CACHE_FILE   = 'sqlite:///' + DATABASE + DATABASE_HOST + DATABASE_USER + ".db"

SQLALCHEMY_TRACK_MODIFICATIONS = False

class Config(object):
    if TESTING == True:
        SQLALCHEMY_DATABASE_URI = TEST_DB
        SQLALCHEMY_TRACK_MODIFICATIONS = False
    elif TESTING == False:
        SQLALCHEMY_DATABASE_URI = LOCAL_CACHE_FILE
        SQLALCHEMY_TRACK_MODIFICATIONS = False


try:
    chembot_server = Flask(__name__ , template_folder="templates" )
    chembot_server.config.from_object(Config)
    database = SQLAlchemy(chembot_server)
    database.init_app(chembot_server)
except Exception:
    redprint(Exception.with_traceback)

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
    cid                 = database.Column(database.String(16))
    iupac_name          = database.Column(database.Text)
    cas                 = database.Column(database.String(64))
    smiles              = database.Column(database.Text)
    formula             = database.Column(database.String(256))
    molweight           = database.Column(database.String(32))
    charge              = database.Column(database.String(32))
    description         = database.Column(database.Text)

    def __repr__(self):
        return 'IUPAC name         : {} \n \
CAS                : {} \n \
Formula            : {} \n \
Molecular Weight   : {} \n \
Charge             : {} \n \
CID                : {} \n \
Description:       : {} \n '.format( \
     self.iupac_name, self.cas , self.formula, self.molweight, \
    self.charge, self.cid, self.description)


class Composition(database.Model):
    __tablename__       = 'Composition'
    __table_args__      = {'extend_existing': True}
    id                  = database.Column(database.Integer, \
                            index=True,                     \
                            primary_key = True,             \
                            unique=True,                    \
                            autoincrement=True)
    name                = database.Column(database.String(64))
    units               = database.Column(database.Integer)
    compounds           = database.Column(database.String(256))
    notes               = database.Column(database.Text)

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
        greenprint(formula_list)
        formula = ""

        # what the hell was I doing here?
        # seriously, I forgot
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
test_entry1 = Compound(iupac_name ='tentacles', formula="HeNTaI" )
test_entry2 = Composition(name = "flash", units="%wt", compounds="Al,27.7,NH4ClO4,72.3", notes=test_comp_notes )
database.create_all()
database.session.add(test_entry1)
database.session.add(test_entry2)
database.session.commit()

#while True:
    #database_server = threading.Thread.start(chembot_server.run() )
################################################################################
##############                       Routes                    #################
################################################################################

@chembot_server.route('/pubchem_route')
def pubchem_route():
    # you make the template here
    pass

################################################################################
##############                     FUNCTIONS                   #################
################################################################################
class Database_functions():
    def __init__(self):
        self.TESTING = False
     
    def Compound_by_id(cid_of_compound : str):
        """
        Returns a compound from the local DB
        Returns FALSE if entry does not exist
        :param: cid_of_compound
        """
        cid_passed = cid_of_compound
        try:
            #return database.session.query(Compound).filter_by(Compound.cid == cid_passed)
            #                                * See that right there? "cid" ?
            return Compound.query.filter_by(cid = cid_passed).first()
            # SQL-Alchemy interprets that as the record to lookup
            # it DOES NOT evaluate the contents of a variable
            # do not forget that! It uses the name as is! The contents do not matter!
        except Exception:
            redprint("[-] Failure in Compound_by_id")
            redprint(str(Exception.__cause__))
            return False

    ################################################################################
    def internal_local_database_lookup(entity : str, id_of_record:str ):
        """
        feed it a formula or CID followed buy "formula" or "cid"
        Returns False and raises and exception/prints exception on error
        Returns an SQLAlchemy database object if record exists
        Don't forget this is for compounds only!
        """
        try:
            greenprint("[+] performing internal lookup")
            pubchem_search_types = {"cid","iupac_name","cas"}
            if id_of_record in pubchem_search_types:
                kwargs  = { id_of_record : entity}
                lookup_result  = Compound.query.filter_by(**kwargs ).first()
                #lookup_result  = database.Compound.query.filter_by(id_of_record = entity).first()
            return lookup_result
        except Exception:
            redprint("[-] Not in local database")
            return lookup_result


    def add_to_db(thingie):
        """
        Takes SQLAchemy Class_model Objects 
        For updating changes to Class_model.Attribute using the form:

            Class_model.Attribute = some_var 
        add_to_db(some_var)

        """
        try:
            blueprint("start of Database_functions.add_to_db()")
            database.session.add(thingie)
            database.session.commit
        except Exception:
            redprint("[-] add_to_db() FAILED")
            print(Exception.__cause__)
    ################################################################################

    def update_db():
        """
        DUH
        """
        try:
            database.session.commit()
        except Exception:
            redprint("[-] Update_db FAILED")

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
    ###############################################################################

    def compound_to_database(lookup_list: list):
        """
        Puts a pubchem lookup to the database
        ["CID", "cas" , "smiles" , "Formula", "Name", "Description"]
        """
        lookup_cid                 = lookup_list[0].get('cid')
        #lookup_cas                = lookup_list[0].get('cas')
        lookup_smiles              = lookup_list[0].get('smiles')
        lookup_formula             = lookup_list[0].get('formula')        
        lookup_molweight           = lookup_list[0].get('molweight')        
        lookup_charge              = lookup_list[0].get('charge')
        lookup_name                = lookup_list[0].get('iupac_name')
        lookup_description         = lookup_list[0].get('description')

        Database_functions.add_to_db(Compound(                       \
            cid              = lookup_cid                    ,\
            #cas             = lookup_cas                    ,\
            smiles           = lookup_smiles                 ,\
            formula          = lookup_formula                ,\
            molweight        = lookup_molweight              ,\
            charge           = lookup_charge                 ,\
            iupac_name       = lookup_name                   ,\
            description      = lookup_description            ))

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
#        for each in formula_list:
#            input = Pubchem_lookup.formula_input_validation(each)

        # extend this but dont forget to add more fields in the database model!
        Database_functions.add_to_db(Composition(\
                name       = comp_name,               \
                units      = units_used,              \
                compounds  = formula_list,            \
                notes      = info                     ))

 ###############################################################################   

###############################################################################
# Additional REST request required, regrettably, return 
# values lack the description field
class pubchemREST_Description_Request():
    # hey it rhymes
    '''
    This class is to be used only with validated information
    Returns the description field using the XML return from the REST service
    Does Compounds ONLY!, Needs a second class or modifications to this one 
    To return a Substance type

    results are stored in :
        pubchemREST_Description_Request.parsed_results

    the url of the API call is stored in :
        pubchemREST_Description_Request.request_url
    '''
    def __init__(self, record_to_request: str ,input_type = 'iupac_name' ):
        # it doesnt work the other way elsewhere in the script, I dont know why
        # to avoid that issue im just using it for everything
        fuck_this = lambda fuck: fuck in pubchem_search_types 
        if fuck_this(input_type) :#in pubchem_search_types:
            if TESTING == True:
                greenprint("searching for a Description : " + record_to_request)
            if input_type  == "iupac_name":
                self.thing_type = "name"
            else :
                self.thing_type = input_type
        self.record_to_request  = record_to_request

        #finalized URL        
        self.request_url        = requote_uri("{}/compound/{}/{}/description/XML".format(\
                                    API_BASE_URL,self.thing_type,self.record_to_request))
        blueprint("[+] Requesting: ")
        redprint(self.request_url)
        #make the request
        self.request_return     = requests.get(self.request_url)
        #make some soup
        self.soupyresults       = BeautifulSoup(self.request_return.text , features='lxml').contents[1]
        #serve up the Descriptions
        self.parsed_result       = self.soupyresults.find_all(lambda tag:  tag.name =='description')
        #if it's not empty
        if self.parsed_result != [] :
            # I know its ugly, forgive me
            #print(str(self.parsed_result[0].contents[0]))
            self.parsed_result = str(self.parsed_result[0].contents[0])
        #if it is empty
        elif self.parsed_result == [] or NoneType:
            blueprint("No Description Available in XML REST response")
            self.parsed_result = "No Description Available in XML REST response"

###############################################################################
class Pubchem_lookup():
    '''
Class to perform lookups on CID's and IUPAC names
Also does chempy translation to feed data to the calculation engine

NOTE: to grab a description requires a seperate REST request.
    Therefore, you must specify if the bot collects that information

    SUBNOTE: TURNED ON BY DEFAULT because reasons
    '''
    def __init__(self, user_input, type_of_input, description = True):
        self.internal_lookup_bool   = bool
        self.user_input             = user_input
        self.type_of_input          = type_of_input
        self.grab_description       = description
        if TESTING == True:
            self.local_output_container = {"test" : "sample text"} # wahoo! more abstraction!
        else: 
            self.local_output_container = {}
        #do the thing 
        self.validate_user_input(self.user_input , self.type_of_input)
        #say the thing
        self.reply_to_query()


    def help_message():
        return """
input CID/CAS or IUPAC name or synonym
Provide a search term and "term type", term types are "cas" , "iupac_name" , "cid"
Example 1 : .pubchem_lookup methanol iupac_name
Example 2 : .pubchem_lookup 3520 cid
Example 3 : .pubchem_lookup 113-00-8 cas
"""
###############################################################################
    def reply_to_query(self):
        '''    
        oh wow nothing to document?
        ''' 
        temp_array = []
        global lookup_output_container
        # dict.get() returns None if key not present, ONE *SHOULD* be empty
        # if internal lookup, which was run first, returns False...
        # it should be empty
        
        #the internal lookup was false, 
        # I.E. This is the first time this compound was searched for
        if "internal_lookup" in self.local_output_container:
            redprint("local output container empty")
            pass
        else:
            if self.internal_lookup_bool == False:
                temp_array.append(self.local_output_container.get("lookup_object"))
            elif self.internal_lookup_bool == True:
                temp_array.append(self.local_output_container.get("internal_lookup"))
            else:
                redprint("[-] Failure in reply_to_query if/elif/else")
                greenprint(str(self.local_output_container))
                temp_array.append(self.local_output_container.get("description"))
                blueprint("Temp_array contents:" + str(temp_array))
        
        # clear the output from any previous lookups
        lookup_output_container.clear()
        # add the new message
        lookup_output_container.append(temp_array)
        # this code only runs if TESTING is set to True
        redprint("=============================================")
        greenprint("[+] Sending the following reply via global output container")
        blueprint(str(lookup_output_container))
        redprint("=============================================")
        # clean up just in case
        self.local_output_container.clear()


    def user_input_was_wrong(self , type_of_pebkac_failure : str, bad_string = ""):
        """
        You can put something funny here!
            This is something the creator of the bot needs to modify to suit
            Thier community.
        """
        derp = {"bad_CAS" :"Bad CAS input"                     ,\
                "bad_CID" : "Input given was " + bad_string    ,\
                "lookup_function" : bad_string                 ,\
                "input_id" : 'bloop'                            }
        # clear the container for cleanliness
        self.local_output_container.clear()
        self.local_output_container[type_of_pebkac_failure] = derp.get(type_of_pebkac_failure) + bad_string + "\n"

    def do_lookup(self, user_input, type_of_input):
        try:
            internal_lookup = Database_functions.internal_local_database_lookup(user_input, type_of_input)
            # if internal lookup is false, we do a remote lookup and then store the result
            if internal_lookup == None or False:
                redprint("[-] Internal Lookup returned false")
                # perform the REST description lookup
                description_lookup = pubchemREST_Description_Request(user_input, type_of_input)
                # store the result
                self.lookup_description = description_lookup.parsed_result
                # perform the remote lookup
                lookup_object = self.pubchem_lookup_by_name_or_CID(user_input, type_of_input)
                # append the remote lookup to the internal output container
                # remember, the remote lookup returns the local DB entry
                # it has performed a search and stored it locally
                greenprint("CONTROL FLOW!!!!")
                greenprint(str(lookup_object))
                self.local_output_container.append({ "lookup_object" : lookup_object })
            # we return the internal lookup if the entry is already in the DB
            # for some reason, asking if it's true doesn't work here so we use a NOT instead of an Equals.
            elif internal_lookup != None or False:
                greenprint("[+] Internal Lookup returned TRUE")
                # append the internal lookup to the internal output container
                self.local_output_container.append({ "internal_lookup" : internal_lookup})
                greenprint("CONTROL FLOW!!!!")
                greenprint(str(internal_lookup))
        # bad things happened do stuff with this stuff please
        # its in dire need of proper exception handling              
        except Exception:
            redprint('[-] Something happened in the try/except block for the function do_lookup')
            blueprint(Exception.with_traceback)


    def validate_user_input(self, user_input: str, type_of_input:str):
        """
    User Input is expected to be the proper identifier.
        type of input is one of the following:
        cid , iupac_name , cas
    
        """
        import re
        cas_regex = re.compile('[1-9]{1}[0-9]{1,5}-\d{2}-\d')
        # seriously, 
        # if type_of_input in pubchem_search_types:
        # didnt work.
        # no idea why.
        pubchem_search_types = ["iupac_name", "cid", "cas"]
        fuck_this = lambda fuck: fuck in pubchem_search_types 
        if fuck_this(type_of_input) :#in pubchem_search_types:
            greenprint("user supplied a : " + type_of_input)
            try:
                #user gave a CAS
                if type_of_input == "cas":
                    greenprint("[+} trying to match regular expression for CAS")
                    #regex cas number
                    if re.match(cas_regex,user_input):
                        greenprint("[+] Good CAS Number")
                        #do the thing
                        self.do_lookup(user_input, type_of_input)
                    else:
                        redprint("[-] Bad CAS Number")
                        # dont do the thing
                        self.user_input_was_wrong("bad_CAS", user_input)
                #do the thing
                elif type_of_input == "cid" or "iupac_name":
                    self.do_lookup(user_input, type_of_input)
                else:
                    redprint("[-] Something really wierd happened inside the validated control flow")
            except Exception:
                #some thing was bad
                redprint("[-] reached the exception : input_type was wrong somehow")
                blueprint(str(Exception.with_traceback))

        else:
            #user was doofus
            self.user_input_was_wrong("input_type" , type_of_input)  

    def pubchem_lookup_by_name_or_CID(self , compound_id, type_of_data:str):
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
        # return_index is the result to return, 0 is the first one
        return_index = 0
        data = ["iupac_name","cid","cas"]
        if type_of_data in data:
        #different methods are used depending on the type of input
        #one way
            if type_of_data == ("iupac_name" or "cas"):                     
                try:
                    greenprint("[+] Performing Pubchem Query")
                    lookup_results = pubchem.get_compounds(compound_id,'name')
                    #if GRAB_DESCRIPTION == True:
                    #    greenprint("[+] Grabbing Description")
                        #lookup_description = pubchemREST_Description_Request(compound_id, "iupac_name")
                except Exception :# pubchem.PubChemPyError:
                    redprint("[-] Error in pubchem_lookup_by_name_or_CID : NAME exception")
                    self.user_input_was_wrong("pubchem_lookup_by_name_or_CID")
        # CID requires another way
            elif type_of_data == "cid":
                try:
                    greenprint("[+] Performing Pubchem Query")
                    lookup_results = pubchem.Compound.from_cid(compound_id)
                    #lookup_description = pubchemREST_Description_Request(compound_id, "cid")
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
                            'iupac_name' : each.iupac_name          ,\
                            'description' : self.lookup_description        }]
                    return_relationships.append(query_appendix)
                    ####################################################
                    # Right here we need to find a way to store multiple records
                    # and determine the best record to store as the main entry
                    ####################################################
                    #Database_functions.compound_to_database() TAKES A LIST
                    # first element of first element
                    #[ [this thing here] , [not this one] ]
                    redprint("=========RETURN RELATIONSHIPS=======multiple")
                    blueprint(str(return_relationships[return_index]))
                    redprint("=========RETURN RELATIONSHIPS=======multiple")
                    Database_functions.compound_to_database(return_relationships[return_index])
            
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
                            'iupac_name' : lookup_results.iupac_name          ,\
                            'description' : self.lookup_description                  }]

                return_relationships.append(query_appendix)
                redprint("=========RETURN RELATIONSHIPS=======")
                blueprint(str(return_relationships[return_index]))
                redprint("=========RETURN RELATIONSHIPS=======")
                Database_functions.compound_to_database(return_relationships[return_index])
            else:
                redprint("PUBCHEM LOOKUP BY CID : ELSE AT THE END")
        #and then, once all that is done return the LOCAL database entry to
        # the calling function so this is just an API to the db code
        return_query = return_relationships[return_index]
        redprint("==BEGINNING==return query for pubchem/local lookup===========")
        query_cid    = return_query[0].get('cid')
        local_query  = Compound.query.filter_by(cid = query_cid).first()
        # you can itterate over the database query
        greenprint(local_query)
        redprint("=====END=====return query for pubchem/local lookup===========")
        #after storing the lookup to the local database, retrive the local entry
        #This returns an SQLALchemy object
        return local_query
        # OR return the remote lookup entry, either way, the information was stored
        # and you get a common "api" to draw data from.


if TESTING == True:
    import time
    #craft a list of queries to test with
    test_query_list = [["420","cid"],\
            ["methanol","iupac_name"],\
             ["phenol","iupac_name"],\
              ["methylene chloride","iupac_name"] ,\
               ["6623","cid"],\
                ["5462309","cid"],\
                 ["24823","cid"],\
                  ["water","iupac_name"]]
    ###################################################################
    # First we do some lookups to pull data and populate the database]
    #add more tests
    ###################################################################
    for each in test_query_list:
        time.sleep(5)
        Pubchem_lookup(each[0],each[1])
    ###################################################################
    # then we test the "is it stored locally?" function
    ###################################################################
    for each in test_query_list:
        Pubchem_lookup(each[0],each[1])
    #pubchemREST_Description_Request("methanol","iupac_name")
    #pubchemREST_Description_Request("caffeine","iupac_name")
    #pubchemREST_Description_Request("water","iupac_name")


