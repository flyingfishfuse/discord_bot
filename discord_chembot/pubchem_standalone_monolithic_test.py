import mendeleev
import asyncio
import os
from flask import Flask, render_template, Response, Request ,Config
from flask_sqlalchemy import SQLAlchemy


import re
import chempy
import datetime
import math, cmath
import pubchempy as pubchem

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

input_types_requestable = ["name", "cid", "cas"]
cas_regex = re.compile('[1-9]{1}[0-9]{1,5}-\d{2}-\d')

pubchem_search_types = ["cas", "cid" , "name" ] #, "formula"]

specifics_list = ["basic" , "historical" , "physical" , "chemical", "nuclear", "ionization",\
        "isotopes", "oxistates"]

yotta = 1000000000000000000000000#
zetta = 1000000000000000000000  #
exa =  1000000000000000000      #
peta = 1000000000000000        #
tera = 1000000000000         #
giga = 1000000000          #
mega = 1000000          #
kilo = 1000          #
hecto = 100       #
deca = 10       #
deci = 0.1     #
centi = 0.01      #
milli = 0.001       #
micro = 0.00001       #
nano = 0.00000001        #
pico = 0.000000000001      #
femto = 0.000000000000001    #
atto = 0.000000000000000001    #
zepto = 0.000000000000000000001 #
yocto = 0.000000000000000000000001
pi = 3.14159
Vbe= 0.7 # volts

# I am stupid and did dumb dumb things but this seems useful so I keep
element_list_uncapitalized = ['hydrogen', 'helium', 'lithium', 'beryllium', 'boron', \
        'carbon', 'nitrogen', 'oxygen', 'fluorine', 'neon', 'sodium', \
        'magnesium', 'aluminum', 'silicon', 'phosphorus', 'sulfur', \
        'chlorine', 'argon', 'potassium', 'calcium', 'scandium', \
        'titanium', 'vanadium', 'chromium', 'manganese', 'iron', \
        'cobalt', 'nickel', 'copper', 'zinc', 'gallium', 'germanium', \
        'arsenic', 'selenium', 'bromine', 'krypton', 'rubidium', \
        'strontium', 'yttrium', 'zirconium', 'niobium', 'molybdenum', \
        'technetium', 'ruthenium', 'rhodium', 'palladium', 'silver', \
        'cadmium', 'indium', 'tin', 'antimony', 'tellurium', 'iodine', \
        'xenon', 'cesium', 'barium', 'lanthanum', 'cerium', \
        'praseodymium', 'neodymium', 'promethium', 'samarium', \
        'europium', 'gadolinium', 'terbium', 'dysprosium', 'holmium', \
        'erbium', 'thulium', 'ytterbium', 'lutetium', 'hafnium', \
        'tantalum', 'tungsten', 'rhenium', 'osmium', 'iridium', 'platinum', \
        'gold', 'mercury', 'thallium', 'lead', 'bismuth', 'polonium', \
        'astatine', 'radon', 'francium', 'radium', 'actinium', 'thorium', \
        'protactinium', 'uranium', 'neptunium', 'plutonium', 'americium', \
        'curium', 'berkelium', 'californium', 'einsteinium', 'fermium', \
        'mendelevium', 'nobelium', 'lawrencium', 'rutherfordium', \
        'dubnium', 'seaborgium', 'bohrium', 'hassium', 'meitnerium', \
        'darmstadtium', 'roentgenium', 'copernicium', 'nihonium', \
        'flerovium', 'moscovium', 'livermorium', 'tennessine']

element_list = ['Hydrogen', 'Helium', 'Lithium', 'Beryllium', 'Boron', \
        'Carbon', 'Nitrogen', 'Oxygen', 'Fluorine', 'Neon', 'Sodium', \
        'Magnesium', 'Aluminum', 'Silicon', 'Phosphorus', 'Sulfur', \
        'Chlorine', 'Argon', 'Potassium', 'Calcium', 'Scandium', \
        'Titanium', 'Vanadium', 'Chromium', 'Manganese', 'Iron', 'Cobalt',\
        'Nickel', 'Copper', 'Zinc', 'Gallium', 'Germanium', 'Arsenic', \
        'Selenium', 'Bromine', 'Krypton', 'Rubidium', 'Strontium', \
        'Yttrium', 'Zirconium', 'Niobium', 'Molybdenum', 'Technetium',\
        'Ruthenium', 'Rhodium', 'Palladium', 'Silver', 'Cadmium', \
        'Indium', 'Tin', 'Antimony', 'Tellurium', 'Iodine', 'Xenon', \
        'Cesium', 'Barium', 'Lanthanum', 'Cerium', 'Praseodymium', \
        'Neodymium', 'Promethium', 'Samarium', 'Europium', 'Gadolinium', \
        'Terbium', 'Dysprosium', 'Holmium', 'Erbium', 'Thulium', \
        'Ytterbium','Lutetium', 'Hafnium', 'Tantalum', 'Tungsten', \
        'Rhenium', 'Osmium', 'Iridium', 'Platinum', 'Gold', 'Mercury', \
        'Thallium', 'Lead', 'Bismuth', 'Polonium', 'Astatine', \
        'Radon', 'Francium', 'Radium', 'Actinium', 'Thorium', \
        'Protactinium', 'Uranium', 'Neptunium', 'Plutonium', \
        'Americium', 'Curium', 'Berkelium', 'Californium', \
        'Einsteinium', 'Fermium', 'Mendelevium', 'Nobelium', \
        'Lawrencium', 'Rutherfordium', 'Dubnium', 'Seaborgium', \
        'Bohrium', 'Hassium', 'Meitnerium', 'Darmstadtium', \
        'Roentgenium', 'Copernicium', 'Nihonium', 'Flerovium', \
        'Moscovium', 'Livermorium', 'Tennessine']

symbol_list = ['H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na', \
        'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', \
        'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', \
        'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', \
        'In', 'Sn', 'Sb', 'Te', 'I', 'Xe', 'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd', \
        'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf', \
        'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', \
        'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', \
        'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', \
        'Mt', 'Ds', 'Rg', 'Cn', 'Nh', 'Fl', 'Mc', 'Lv', 'Ts']

###############################################################################
## TESTING VARS
TESTING = True
TESTING = False
#The sqlite :memory: identifier is the default if no filepath is present. 
# Specify sqlite:// and nothing else:
#e = create_engine('sqlite://')
TEST_DB = 'sqlite://'
import threading
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
     self.cid, self.iupac_name , self.cas, self.formula, \
    self.molweight, self.charge)

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
test_entry1 = Compound(iupac_name ='tentacles', formula="HeNTaI" )
test_entry2 = Composition(name = "flash", units="%wt", compounds="Al,27.7,NH4ClO4,72.3", notes=test_comp_notes )
database.create_all()
database.session.add(test_entry1)
database.session.add(test_entry2)
database.session.commit()
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
class Database_functions():
    def _init_(self):
        print("whyyyyy!")
     
    def Compound_by_id(cid_of_compound):
        """
        Returns a compound from the local DB
        Returns FALSE if entry does not exist
        Expects the whole lookup object cause I am gonna expand this function
        :param: cid_of_compound
        """
        cid_passed = str(cid_of_compound[0].get("cid"))

        try:
            #return database.session.query(Compound).filter_by(Compound.cid == cid_passed)    
            return Compound.query.filter_by(cid = cid_passed)
        except Exception:
            redprint("the bad thing in Compound_by_id")
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
            list_thing = ["cid","name","cas"]
            if id_of_record in list_thing:
                #WHY!>!>!>
                lookup_result  = database.session.query(Compound).all().filter_by(id_of_record = entity).first()
                #lookup_result  = Compound.query.filter_by(id_of_record = entity).first()
                #print(Compound.query.filter_by(id_of_record=entity).first())
                return lookup_result
        except Exception:
            function_message("not in local database", "red")
            return False


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
            redprint("add_to_db() failed")
    ################################################################################

    def update_db():
        """
        DUH
        """
        try:
            database.session.commit()
        except Exception:
            function_message("Update_db() failed", "red")

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
        Database_functions.add_to_db(Compound(                       \
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
        """
        The composition is a relation between multiple Compounds
        Each Composition entry will have required a pubchem_lookup on each
        Compound in the Formula field. 
        the formula_list is a CSV STRING WHERE: 
        ...str_compound,int_amount,.. REPEATING (floats allowed)
        EXAMPLE : Al,27.7,NH4ClO4,72.3

        BIG TODO: be able to input list of cas/cid/whatever for formula_list
        """

        # extend this but dont forget to add more fields in the database model!
        Database_functions.add_to_db(Composition(\
                name       = comp_name,               \
                units      = units_used,              \
                compounds  = formula_list,            \
                notes      = info                     ))

 ###############################################################################   

class Element_lookup():
    def __init__(self, element_id_user_input: str or int, specifics_requested : str):
        self.element_id_user_input = element_id_user_input
        self.specifics_requested   = specifics_requested
        self.validate_user_input(self.element_id_user_input, self.specifics_requested)

    def help_message(self):
        return "Put the element's name, symbol, or atomic number followed \
by either: basic, historical, physical, chemical, nuclear, ionization, \
isotopes, oxistates\n For Pubchem lookup, use a CID or IUPAC name ONLY"
        
    def reply_to_query(self,message):
        '''
    Takes a list or string, if list, joins the list to a string and assigns to 
    lookup_output_container. Sends the global output container 
        '''
        list_to_string = lambda list_to_convert: ''.join(list_to_convert)
        if isinstance(message,list):
            message = list_to_string(message) 
        temp_array = [message]
        global lookup_output_container
        lookup_output_container = temp_array        
        
    def user_input_was_wrong(self, type_of_pebkac_failure : str):
        """
        You can put something funny here!
            This is something the creator of the bot needs to modify to suit
            Thier community.
        """
        user_is_a_doofus_element_message  = "Stop being a doofus and feed the data on elements that I expect! "
        user_is_a_doofus_specific_message = "Stop being a doofus and feed the data on specifics that I expect!"
        if type_of_pebkac_failure   == "element":
            self.reply_to_query(user_is_a_doofus_element_message)
        elif type_of_pebkac_failure == "specifics":
            self.reply_to_query(user_is_a_doofus_specific_message)
        else:
            self.reply_to_query(type_of_pebkac_failure)

    async def validate_user_input(self, element_id_user_input: str or int, specifics_requested : str):
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

            #Right here is where you uncomment when you plit variables off to different files
        #from variables_for_reality import element_list , symbol_list , specifics_list
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
            self.user_input_was_wrong("element")

        if isinstance(specifics_requested, str):
            specifics_requested = specifics_requested.lower()

            if any(user_input == specifics_requested for user_input in specifics_list):
                specifics_valid = True
            else:
                self.user_input_was_wrong("specifics")

        else:
            self.user_input_was_wrong("specifics")
        # you extend this when you add more functions
        # this is the function list
        if element_valid and specifics_valid == True:      
            #global lookup_output_container
            if specifics_requested    == "basic":
                self.get_basic_element_properties(element_id_user_input)
                self.reply_to_query(lookup_output_container)
                # so now you got the basic structure of the control loop!
            elif specifics_requested  == "historical":
                self.get_history(element_id_user_input)
                self.reply_to_query(lookup_output_container)
            elif specifics_requested  == "physical":
                self.get_physical_properties(element_id_user_input)
                self.reply_to_query(lookup_output_container)
            elif specifics_requested  == "chemical":
                self.get_chemical_properties(element_id_user_input)
                self.reply_to_query(lookup_output_container)
            elif specifics_requested  == "nuclear":
                self.get_nuclear_properties(element_id_user_input)
                self.reply_to_query(lookup_output_container)
            elif specifics_requested  == "ionization":
                self.get_ionization_energy(element_id_user_input)
                self.reply_to_query(lookup_output_container)
            elif specifics_requested  == "isotopes":
                self.get_isotopes(element_id_user_input)
                self.reply_to_query(lookup_output_container)
            elif specifics_requested  == "oxistates":
                self.get_oxistates(element_id_user_input)
                self.reply_to_query(lookup_output_container)
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
                            internal_lookup = Database_functions.internal_local_database_lookup(user_input, type_of_input)
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
                        internal_lookup = Database_functions.internal_local_database_lookup(user_input, type_of_input)
                        if internal_lookup == None or False:
                            redprint("[-] Internal Lookup returned false")
                            #its breaking here
                            lookup_object = self.pubchem_lookup_by_name_or_CID(user_input, type_of_input)
                            self.reply_to_query(lookup_object)
                        elif internal_lookup == True:
                            greenprint("============Internal Lookup returned TRUE===========")
                            self.reply_to_query(lookup_object)
                        else:
                            function_message("", "[-] Something is wrong with the database", "red")
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
                            'iupac_name' : lookup_results.iupac_name          }]
                return_relationships.append(query_appendix)
                redprint("=========RETURN RELATIONSHIPS=======")
                blueprint(str(return_relationships[return_index]))
                redprint("=========RETURN RELATIONSHIPS=======")
                Database_functions.compound_to_database(return_relationships[return_index])

            else:
                function_message("PUBCHEM LOOKUP BY CID : ELSE AT THE END", "red")
        #and then, once all that is done return the LOCAL database entry to
        # the calling function so this is just an API to the db code
        return_query = return_relationships[return_index]
        redprint("==BEGINNING==return query for pubchem/local lookup===========")
        query_cid    = return_query[0].get('cid')
        local_query  = database.Compound.query.filter_by(cid = query_cid).first()
        # you can itterate over the database query
        for each in local_query:
            blueprint(str(each) + "\n")
        redprint("=====END=====return query for pubchem/local lookup===========")

        #after storing the lookup to the local database, retrive the local entry
        #This returns an SQLALchemy object
        print(Database_functions.Compound_by_id(return_query)[0].get('cid'))
        return Database_functions.Compound_by_id(return_query[0].get('cid'))

        # OR return the remote lookup entry, either way, the information was stored.
        #this returns a pubchempy.Compound() Object type
        #return lookup_results

Pubchem_lookup("420","cid")
Pubchem_lookup("methanol","name")
Pubchem_lookup("phenol","name")
