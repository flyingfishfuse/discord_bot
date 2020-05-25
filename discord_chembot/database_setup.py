#!/usr/bin/python3
import os
from flask import Flask, render_template, Response, Request ,Config
from flask_sqlalchemy import SQLAlchemy

# took this from my game, gonna change it up
DATABASE_HOST      = "localhost"
DATABASE           = "solar_empire-python"
DATABASE_USER      = "moop"
DATABASE_PASSWORD  = "password"
SERVER_NAME        = "Solar Empire: 2020 - Python Edition"
HTTP_HOST          = "gamebiscuits"
ADMIN_NAME         = "Emperor of Sol"
ADMIN_PASSWORD     = "password"
ADMIN_EMAIL        = "game_admin" + "@" + HTTP_HOST
DANGER_STRING= "TACOCAT"


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///solar_empire_test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

solar_empire_server = Flask(__name__ , template_folder="templates" )
solar_empire_server.config.from_object(Config)
database = SQLAlchemy(solar_empire_server)
database.init_app(solar_empire_server)
#One to many relationship
#parent
