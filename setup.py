from setuptools import setup
import pip
import datetime

things_this_app_needs = ['flask' , ' discord', 'pubchempy', 'mendeleev' ,\
    "flask-sqlalchemy" , 'asyncio' , "biopython" , "ionize" , "scipy"]

def import_or_install(package):
    for each in package:
        try:
            __import__(package)
        except ImportError:
            pip.main(['install', package])       
#get all the things!
import_or_install(things_this_app_needs)

setup(
   name='discord_chembot',
   version='01A',
   description='A useful chemical lookup module',
   author='Mr-Hai/flyingishfuse',
   author_email='foomail@foo.com',
   packages=["discord_chem_bot"],  #same as name
   install_requires= things_this_app_needs, #external packages as dependencies
)
