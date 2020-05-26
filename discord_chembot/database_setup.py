#!/usr/bin/python3
import os
from flask import Flask, render_template, Response, Request ,Config
from flask_sqlalchemy import SQLAlchemy

# took this from my game, gonna change it up
# needed a template
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
    SQLALCHEMY_DATABASE_URI = LOCAL_CACHE_FILE
    SQLALCHEMY_TRACK_MODIFICATIONS = True

discord_chembot_server = Flask(__name__ , template_folder="templates" )
discord_chembot_server.config.from_object(Config)
database = SQLAlchemy(discord_chembot_server)
database.init_app(discord_chembot_server)
#One to many relationship
#parent



################################################################################
##############                      Models                     #################
################################################################################
# This is for caching any information that takes forever to grab
#AW FUCK I FORGOT HOW THIS WORKS
# TODO: create add_lookup_to_DB()
class Compound(database.Model):
    __tablename__ = 'Compound'
    id              = database.Column(database.Integer, primary_key = True, unique=True, autoincrement=True)
    name            = database.Column(database.String(64), index=True)
    formula         = database.Column(database.String(120), index=True)
    thing           = database.Column(database.String(128))

    def __repr__(self):
        return '<Compound:{} Formula: {} >'.format(self.name , self.formula)

test_entry = Compound(name ='test', formula="HeNTaI" )
database.create_all()
database.session.add(test_entry)
database.session.commit()
#discord_chembot_server.run()


################################################################################
##############                     FUNCTIONS                   #################
################################################################################
def Compound_by_id(id_of_user):
    return Compound.query.all.filter_by(id = id_of_user).first()

def add_to_db(thingie):
    """
    Takes SQLAchemy Class_model Objects like NEW USERS and SHIPS
    For updating changes to Class_model.Attribute using the form:
    Class_model.Attribute = some_var 
    
    for USERS: change_user_var(user_id, var, value)
    for SHIPS: change_ship_var(ship_id, var, value)
    for UNIV : change_game_var(var, value)
    """
    database.session.add(thingie)
    database.session.commit

def update_db():
    database.session.commit()