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
DANGER_STRING= "TACOCAT"

class Config(object):
    SQLALCHEMY_DATABASE_URI = ''
    SQLALCHEMY_TRACK_MODIFICATIONS = True

discord_chembot_server = Flask(__name__ , template_folder="templates" )
discord_chembot_server.config.from_object(Config)
database = SQLAlchemy(discord_chembot_server)
database.init_app(discord_chembot_server)
#One to many relationship
#parent

# This is for caching any information that takes forever to grab
#AW FUCK I FORGOT HOW THIS WORKS
# TODO: create add_lookup_to_DB()
class Compound(database.Model):
    __tablename__ = 'Compound'
    #PARENT: of UserShip, Primary key must link (be the same)
    id              = database.Column(database.Integer, primary_key = True, unique=True, autoincrement=True)
    #reference to CHILD then reference to SELF
    #blarp          = database.Column(database.relationship('UserShip', \
    #                        primaryjoin = 'and_(User.id == UserShip.user_id)' , \
    #                        backref     = 'User' , \
    #                        uselist     = False ))
#   userid          = database.Column(database.Integer)
    name            = database.Column(database.String(64), index=True)
    formula         = database.Column(database.String(120), index=True)
    thing           = database.Column(database.String(128))

    def __repr__(self):
        return '<Compound:{} Formula: {} >'.format(self.name , self.formula)

#class (User):
#    __tablename__  = 'UserShip'
    #CHILD OF USER: the primary key must link
    #ID is a "universal" identification for the db, SHIP_ID will be a variable 
    # used locally in the system that that user and ship are interacting in
    #id             = database.Column(database.Integer, primary_key=True)
    # The PRIMARY key that is linked bewteen the two, with a new name, the field you want to inherit, is declared next.
    #user_id        = database.Column(database.Integer, database.ForeignKey('User.userid'), nullable=False)
#    ship_id        = database.Column(database.Integer)
#    ship_name      = database.Column(database.String(128))
    # list of 1-whatever of ships
#    ship_type      = database.Column(database.Integer)
    # PARENT OF GENERIC SHIP: the clsses must link like this, backref is __tablename__
    #linked_user    = database.relationship('GenericShip',backref='usership',uselist=False)
#    def __repr__(self):
#        return '<User id:{} name: {} >'.format(self.ship_id , self.ship_name)


test_entry = Compound(name ='test', formula="" )
usership = UserShip(ship_id=3, ship_name='user ship', ship_type=2)
database.create_all()
database.session.add(admin)
database.session.add(usership)

database.session.commit()
#discord_chembot_server.run()

def user_by_id(id_of_user):
    return User.query.all.filter_by(user_id = id_of_user).first()
