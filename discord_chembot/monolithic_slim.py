
import re
import os
import chempy
import datetime
import math, cmath
import pubchempy as pubchem
from flask import Flask, render_template, Response, Request ,Config
from flask_sqlalchemy import SQLAlchemy
###############################################################################
## TESTING VARS
TESTING = True
#TESTING = False
#The sqlite :memory: identifier is the default if no filepath is present. 
# Specify sqlite:// and nothing else:
#e = create_engine('sqlite://')
TEST_DB = 'sqlite://'
import threading
###############################################################################
import colorama
from colorama import init
init()
from colorama import Fore, Back, Style
#Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
#Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
#Style: DIM, NORMAL, BRIGHT, RESET_ALL

blueprint = lambda text: print(Fore.BLUE + ' ' +  text + ' ' + Style.RESET_ALL)
greenprint = lambda text: print(Fore.GREEN + ' ' +  text + ' ' + Style.RESET_ALL)
redprint = lambda text: print(Fore.RED + ' ' +  text + ' ' + Style.RESET_ALL)

COMMAND_PREFIX = "."
devs = ['581952454124372068']
list_to_string = lambda list_to_convert: ''.join(list_to_convert)
# GLOBAL OUTPUT CONTAINER FOR FINAL CHECKS
global lookup_output_container 
lookup_output_container = []
# GLOBAL INPUT CONTAINER FOR USER INPUT VALIDATION
global lookup_input_container
lookup_input_container = []
# Establish an error reporting function

blueprint = lambda text: print(Fore.BLUE + ' ' +  text + ' ' + Style.RESET_ALL)
greenprint = lambda text: print(Fore.GREEN + ' ' +  text + ' ' + Style.RESET_ALL)
redprint = lambda text: print(Fore.RED + ' ' +  text + ' ' + Style.RESET_ALL)

def function_message(exception_message : str, color_to_print="red"):
    """
    A Robust exception message passing class? that uses colorama and inspect
    Takes red, green, blue as color arguments. WORK IN PROGERESS!
    """
    import inspect
    if color_to_print == "red":
        redprint("something wierd happened in: "  + exception_message)
    elif color_to_print == "green":
        greenprint("something wierd happened in: " + exception_message)
    elif color_to_print == "blue":
        blueprint("something wierd happened in: " + exception_message)

 ###############################################################################   
 ###############################################################################   
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
easter_egg_string  = ["AuTiSTiC", "DyNAmITe", "HeLiCoPtEr", "SeNPaI", "HoOKErS ", "CoCaINe",\
                      "COWS"]
################################################################################
##############                      CONFIG                     #################
################################################################################
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
    if TESTING == True:
        database.metadata.clear()
except Exception:
    function_message("[-] Database Init failed!","red")

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
    formula             = database.Column(database.String(120))
    molweight           = database.Column(database.String(32))
    charge              = database.Column(database.String(32))

    def __repr__(self):
        return 'IUPAC name         : {} \n \
CAS                : {} \n \
Formula            : {} \n \
Molecular Weight   : {} \n \
Charge             : {} \n \
CID                : {} \n '.format( \
    self.iupac_name, self.cas , self.formula ,\
    self.molweight, self.charge, self.cid)

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
    compounds           = database.Column(database.String(120))
    notes               = database.Column(database.String(256))

#{
#  "composition" : "flash",
#  "units"       : "%wt",
#  "formula"     : { "Al": 27.7 , "NH4ClO4": 72.3 }
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
test_entry1 = Compound(iupac_name ='tentacles', formula="HeNTaI" )
test_entry2 = Composition(name = "flash", units="%wt", compounds="Al,27.7,NH4ClO4,72.3", notes=test_comp_notes )
database.create_all()
database.session.add(test_entry1)
database.session.add(test_entry2)
database.session.commit()
blueprint("this works here")
print(Compound.query.filter_by(iupac_name = "tentacles").first())
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
def Compound_by_id(cid_of_compound):
    cid_passed = str(cid_of_compound[0].get("cid"))
    lookup = Compound.query.filter_by(cid = cid_passed).first()
    #return database.session.query(Compound).filter_by(Compound.cid == cid_passed)
    return lookup

################################################################################
def internal_local_database_lookup(entity : str, id_of_record:str ):
    #pubchem_search_types = ["cid","name","cas"]
    if id_of_record in pubchem_search_types:
        blueprint("this DOESNT WORK here")
        lookup_result  = Compound.query.filter_by(id_of_record = entity).first()
        redprint(dir())
        greenprint(type(lookup_result))
        return lookup_result
    #except Exception:
    #    function_message("not in local database", "red")
    #    return lookup_result

def add_to_db(thingie):
    try:
        blueprint("start of add_to_db()")
        database.session.add(thingie)
        database.session.commit
    except Exception:
        redprint("add_to_db() failed")
################################################################################

def update_db():
    try:
        database.session.commit()
    except Exception:
        function_message("Update_db() failed", "red")
###############################################################################

def compound_to_database(lookup_list: list):
    """
    Puts a pubchem lookup to the database
    ["CID", "cas" , "smiles" , "Formula", "Name"]
    """
    temp_list = []
    temp_list = lookup_list
    lookup_cid                 = temp_list[0].get('cid')
    #lookup_cas                = temp_list[0].get('cas')
    lookup_smiles              = temp_list[0].get('smiles')
    lookup_formula             = temp_list[0].get('formula')        
    lookup_molweight           = temp_list[0].get('molweight')        
    lookup_charge              = temp_list[0].get('charge')
    lookup_name                = temp_list[0].get('iupac_name')
    add_to_db(Compound(                       \
        cid              = lookup_cid                    ,\
        #cas             = lookup_cas                    ,\
        smiles           = lookup_smiles                 ,\
        formula          = lookup_formula                ,\
        molweight        = lookup_molweight              ,\
        charge           = lookup_charge                 ,\
        iupac_name       = lookup_name                   ))
###############################################################################
def composition_to_database(comp_name: str, units_used :str, \
                            formula_list : list , info : str):
    add_to_db(Composition(\
            name       = comp_name,               \
            units      = units_used,              \
            compounds  = formula_list,            \
            notes      = info                     ))

 ###############################################################################   
 ###############################################################################   

input_types_requestable = ["name", "cid", "cas"]
cas_regex = re.compile('[1-9]{1}[0-9]{1,5}-\d{2}-\d')
pubchem_search_types = ["cas", "cid" , "name" ] #, "formula"]

class Pubchem_lookup():
    def __init__(self, user_input, type_of_input):
        self.user_input     = user_input
        self.type_of_input  = type_of_input
        self.validate_user_input(self.user_input , self.type_of_input)
    ###############################################################################
    def validate_user_input(self, user_input: str, type_of_input:str):
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
                            elif internal_lookup == True:
                                greenprint("============Internal Lookup returned TRUE===========")
                        else:
                            function_message("[-] Bad CAS Number validation CAS lookup checks", "red")                    
                    except Exception:
                        function_message('[-] Something happened in the try/except block for cas numbers', 'red')
                else:
                    try:
                        internal_lookup = internal_local_database_lookup(user_input, type_of_input)
                        asdf_test = redprint(dir())
                        qwer_test = greenprint(type(internal_lookup))
                        if internal_lookup == None:
                            redprint("[-] Internal Lookup returned None")
                            lookup_object = self.pubchem_lookup_by_name_or_CID(user_input, type_of_input)
                        elif internal_lookup == NoneType:
                            redprint("[-] Internal Lookup returned NoneType")
                            lookup_object = self.pubchem_lookup_by_name_or_CID(user_input, type_of_input)
                        elif internal_lookup == False:
                            redprint("[-] Internal Lookup returned False")
                            lookup_object = self.pubchem_lookup_by_name_or_CID(user_input, type_of_input)
                        elif internal_lookup == True:
                            greenprint("============Internal Lookup returned TRUE===========")
                        else:
                            function_message("[-] Something is wrong with the database", "red")
                    except Exception:
                        function_message("reached exception : name/cid lookup - control flow", "red")
            except Exception:
                function_message("reached the exception : input_type was wrong somehow" , "red")
        else:
            print("end of control loop")
    def pubchem_lookup_by_name_or_CID(self, compound_id, type_of_data:str):
        return_relationships = []
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
            if isinstance(lookup_results, list):# and len(lookup_results) > 1 :
                greenprint("[+] Multiple results returned ")
                for each in lookup_results:
                    redprint(each.molecular_formula)
                    query_appendix = [{'cid' : each.cid                 ,\
                            'smiles'     : each.isomeric_smiles     ,\
                            'formula'    : each.molecular_formula   ,\
                            'molweight'  : each.molecular_weight    ,\
                            'charge'     : each.charge              ,\
                            'iupac_name' : each.iupac_name          }]
                    return_relationships.append(query_appendix)
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
        for each in local_query:
            blueprint(str(each) + "\n")
        redprint("=====END=====return query for pubchem/local lookup===========")
        print(Compound_by_id(query_cid))
        return Compound_by_id(query_cid)
        # OR return the remote lookup entry, either way, the information was stored.
        #this returns a pubchempy.Compound() Object type
        #return lookup_results

Pubchem_lookup("420","cid")
Pubchem_lookup("methanol","name")
Pubchem_lookup("phenol","name")
