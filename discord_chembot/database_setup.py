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
#list_of_resources = "https://en.wikipedia.org/wiki/List_of_data_references_for_chemical_elements"
#data_pages_list   = "https://en.wikipedia.org/wiki/Category:Chemical_element_data_pages"
# https://chemspipy.readthedocs.io/en/latest/
import os
import csv
from flask import Flask, render_template, Response, Request ,Config
from flask_sqlalchemy import SQLAlchemy
#from discord_chembot.variables_for_reality import \
#    greenprint,redprint,blueprint,function_message
from variables_for_reality import greenprint,redprint,blueprint,function_message
import inspect
###############################################################################
## TESTING VARS
TESTING = True
#The sqlite :memory: identifier is the default if no filepath is present. 
# Specify sqlite:// and nothing else:
#e = create_engine('sqlite://')
TEST_DB = 'sqlite://'

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
    cid                 = database.Column(database.Integer)
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
#database_server = threading.Thread.start(chembot_server.run() )

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

        """
        cid_passed = str(cid_of_compound[0].get("cid"))
        redprint("start of Compound_by_id()")
        blueprint("CID passed to function: " + cid_passed)
        #print(inspect.stack()[1][3])
        #print(Compound.query.filter_by(cid = cid_passed).first().__repr__)
        try:
            #return database.session.query(Compound).filter_by(Compound.cid == cid_passed)    
            #print(Compound.query.filter_by(cid = cid_passed)).first()
            return Compound.query.filter_by(cid = cid_passed).first()
        except Exception:
            redprint("the bad thing in Compound_by_id")
            print(str(Exception.__cause__))
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
            if id_of_record    == "cid":
                lookup_result  = Compound.query.filter_by(cid=entity).first()
                return lookup_result
            elif id_of_record  == "name":
                lookup_result  = Compound.query.filter_by(name=entity).first()
                return lookup_result
            elif id_of_record  == "cas":
                lookup_result  = Compound.query.filter_by(cas=entity).first()
                return lookup_result
        except Exception:
            function_message("internal lookup" , Exception, "red")
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
            print(Exception.__cause__)
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
        lookup_name                = temp_list[0].get('name')
        Database_functions.add_to_db(Compound(                       \
            cid       = lookup_cid                    ,\
            #cas      = lookup_cas                    ,\
            smiles    = lookup_smiles                 ,\
            formula   = lookup_formula                ,\
            molweight = lookup_molweight              ,\
            charge    = lookup_charge                 ,\
            name      = lookup_name                   ))

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
#        for each in formula_list:
#            input = Pubchem_lookup.formula_input_validation(each)

        # extend this but dont forget to add more fields in the database model!
        Database_functions.add_to_db(Composition(\
                name       = comp_name,               \
                units      = units_used,              \
                compounds  = formula_list,            \
                notes      = info                     ))

 ###############################################################################   