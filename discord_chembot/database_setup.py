#!/usr/bin/python3
import os
import csv
from flask import Flask, render_template, Response, Request ,Config
from flask_sqlalchemy import SQLAlchemy
from discord_chembot.variables_for_reality import \
    greenprint,redprint,blueprint,function_message

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
easter_egg_string  = ["AuTiSTiC", "DyNAmITe", "HeLiCoPtEr", "SeNPaI", "HoOKErS ", "CoCaINe"]
################################################################################
##############                      CONFIG                     #################
################################################################################
class Config(object):
    try:
        if TESTING == True:
            SQLALCHEMY_DATABASE_URI = TEST_DB
        elif TESTING == False:
            SQLALCHEMY_DATABASE_URI = LOCAL_CACHE_FILE
        else:
            function_message(TESTING, "red")
    except Exception:
        function_message(Exception, "red")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
try:
    discord_chembot_server = Flask(__name__ , template_folder="templates" )
    discord_chembot_server.config.from_object(Config)
    database = SQLAlchemy(discord_chembot_server)
    database.init_app(discord_chembot_server)
except Exception:
    function_message(Exception,"red")

#One to many relationship
#parent

################################################################################
##############                      Models                     #################
################################################################################
# This is for caching any information that takes forever to grab
# TODO: create add_lookup_to_DB()

class Compound(database.Model):
    __tablename__       = 'Compound'
    id                  = database.Column(database.Integer, \
                            index=True, \
                            primary_key = True, \
                            unique=True, \
                            autoincrement=True)
    cid                 = database.Column(database.String(128))
    name                = database.Column(database.String(64))
    cas                 = database.Column(database.String(64))
    smiles              = database.Column(database.Text)
    formula             = database.Column(database.String(120), index=True)

    def __repr__(self):
        return 'Compound: {} \n \
                CAS     : {} \n \
                Formula : {} \n '.format(self.name , self.cas, self.formula)

class Composition(Compound.Model):
    __tablename__       = 'Compound'
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
        # csv reader returns an iterable, here it would be the formula supplied
        formula_list = csv.reader(self.compounds, delimiter=",")
        formula = ""
        for each in formula_list:
            greenprint(each)
            #catches the amount
            if each.isnumeric():
                amount = str(each)
                redprint(amount)
            #catches the element/compound
            else:
                compound = str(each)
                redprint(compound)
            ## OOF I hope this does what I expect
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
test_entry1 = Compound(name ='test', formula="HeNTaI" )
test_entry2 = Composition(name = "flash", units="%wt", compounds="Al,27.7,NH4ClO4,72.3", notes=test_comp_notes )
database.create_all()
database.session.add(test_entry1)
database.session.add(test_entry2)
database.session.commit()
#discord_chembot_server.run()


################################################################################
##############                     FUNCTIONS                   #################
################################################################################

def Compound_by_id(cid_of_compound):
    """
    Returns a compound from the local DB

    """
    try:

        return Compound.query.all.filter_by(id = cid_of_compound).first()
    except Exception:
        function_message(Exception, "red")
        return False
    
################################################################################
def internal_local_database_lookup(entity : str, id_of_record:str ):
    """
    feed it a formula or CID followed buy "formula" or "cid"
    Returns False and raises and exception/prints exception on error
    """
    try:
        if id_of_record    == "cid":
            lookup_result  = database.Query(entity).filter_by("cid").first()
            blueprint(lookup_result)
        elif id_of_record  == "formula":
            lookup_result  = database.Query(entity).filter_by("formula").first()
            blueprint(lookup_result)
        elif id_of_record  == "cas":
            lookup_result  = database.Query(entity).filter_by("cas").first()
            blueprint(lookup_result)
        return lookup_result
    except Exception:
        function_message(Exception, "red")
        return False
    
def add_to_db(thingie):
    """
    Takes SQLAchemy Class_model Objects 
    For updating changes to Class_model.Attribute using the form:
    Class_model.Attribute = some_var 
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