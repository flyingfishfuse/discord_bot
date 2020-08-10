#/usr/bin/python3
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
#list_of_resources = "https://en.wikipedia.org/wiki/List_of_data_references_for_chemical_elements"
#data_pages_list   = "https://en.wikipedia.org/wiki/Category:Chemical_element_data_pages"
# https://chemspipy.readthedocs.io/en/latest/

###############################################################################
# This file contains all of the information that needs to be globally available
# Some people will say this is a bad idea, they are wrong. Absolute statements
# are, for the most part, not possible. Only, in matters of good and evil
# can there be absolutes.
###############################################################################

# THIS IS A TOP LEVEL FILE
# DO NOT CREATE CYCLIC DEPENDENCIES!

import colorama
from colorama import init
init()
from colorama import Fore, Back, Style
#Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
#Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
#Style: DIM, NORMAL, BRIGHT, RESET_ALL

#TESTING colored print functions
# ok so according to some website on the internet (professional, I know)
# https://thispointer.com/python-how-to-use-if-else-elif-in-lambda-functions/
# You can do THIS:
# lambda <args> : <return Value> if <condition > ( <return value > if <condition> else <return value>)
# make them global scope for testing purposes

# this one is used inline to convert lists to strings inside of print functions
list_to_string = lambda list_to_convert: ''.join(list_to_convert)
# so it prints to screen as a return "value" IF it's in "test mode"
#TODO: OR VERBOSE!!
#  but returns NONE if test mode is off
blueprint = lambda text: print(Fore.BLUE + ' ' +  text + ' ' + Style.RESET_ALL) if (TESTING == True) else None
greenprint = lambda text: print(Fore.GREEN + ' ' +  text + ' ' + Style.RESET_ALL) if (TESTING == True) else None
redprint = lambda text: print(Fore.RED + ' ' +  text + ' ' + Style.RESET_ALL) if (TESTING == True) else None

    
# inline colorization for lambdas in a lambda
makered    = lambda text: Fore.RED + ' ' +  text + ' ' + Style.RESET_ALL
makegreen  = lambda text: Fore.GREEN + ' ' +  text + ' ' + Style.RESET_ALL
makeblue   = lambda text: Fore.BLUE + ' ' +  text + ' ' + Style.RESET_ALL
makeyellow = lambda text: Fore.YELLOW + ' ' +  text + ' ' + Style.RESET_ALL

yellow_bold_print = lambda text: print(Fore.YELLOW + Style.BRIGHT + ' {} '.format(text) + Style.RESET_ALL) if (TESTING == True) else None

# Filter None values from kwargs
#kwargs = dict((k, v) for k, v in kwargs.items() if v is not None)

################################################################################
## TESTING VARS
################################################################################

TESTING = True
#TESTING = False
#The sqlite :memory: identifier is the default if no filepath is present. 
# Specify sqlite:// and nothing else:
#e = create_engine('sqlite://')
TEST_DB = 'sqlite://'

################################################################################
################################################################################

COMMAND_PREFIX = "."
devs = ['581952454124372068']
list_to_string = lambda list_to_convert: ''.join(list_to_convert)
GRAB_DESCRIPTION = True

# GLOBAL OUTPUT CONTAINER FOR FINAL CHECKS
global lookup_output_container 
lookup_output_container = []

# GLOBAL INPUT CONTAINER FOR USER INPUT VALIDATION
global lookup_input_container
lookup_input_container = []

# pubchem REST API service
pubchem_search_types = ["iupac_name", "cid", "cas"]
search_validate      = lambda search: search in pubchem_search_types 
API_BASE_URL         = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug'
STORE_BASE64         = True
#move to your whatever.py discord module
discord_color = 0x3b12ef
#deprecated but VERY useful
#iutterates over Mendeleev library's elements and returns various datas
#     def generate_element_validation_name_list(self):
#        from variables_for_reality import element_list , symbol_list , specifics_list
#        return_element_by_id = lambda element_id_input : mendeleev.element(element_id_input)
#        for element in range(1,118):
#            element_object = return_element_by_id(element)
#            element_list.append(element_object.name)
#            symbol_list.append(element_object.symbol)


yotta = 1000000000000000000000000
zetta = 1000000000000000000000
exa =  1000000000000000000
peta = 1000000000000000
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

scale_converter_unit_list = {"mega"  : mega  , "kilo" : kilo , "hecto" : hecto , \
                             "deca"  : deca  , "deci" : deci , "milli" : milli ,\
                             "micro" : micro , "pico" : pico , "nano"  : nano }

#def scale_converter(number, unit):
#    """
#    This function is used to convert numbers input by the user to something the
#    Program can understand. It allows the user to say, for example :
#
#    jazzy_prompt #> 150 milli volts * 200 milli amps
#
#    """
#    if unit in scale_converter_unit_list:
#        return number* scale_converter_unit_list.get(unit)

specifics_list = ["basic" , "historical" , "physical" , "chemical", "nuclear", "ionization",\
        "isotopes", "oxistates"]

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

class CompoundIdType(object):
    """"""
    #: Original Deposited Compound
    DEPOSITED = 0
    #: Standardized Form of the Deposited Compound
    STANDARDIZED = 1
    #: Component of the Standardized Form
    COMPONENT = 2
    #: Neutralized Form of the Standardized Form
    NEUTRALIZED = 3
    #: Deposited Mixture Component
    MIXTURE = 4
    #: Alternate Tautomer Form of the Standardized Form
    TAUTOMER = 5
    #: Ionized pKa Form of the Standardized Form
    IONIZED = 6
    #: Unspecified or Unknown Compound Type
    UNKNOWN = 255


class BondType(object):
    SINGLE = 1
    DOUBLE = 2
    TRIPLE = 3
    QUADRUPLE = 4
    DATIVE = 5
    COMPLEX = 6
    IONIC = 7
    UNKNOWN = 255


class CoordinateType(object):
    TWO_D = 1
    THREE_D = 2
    SUBMITTED = 3
    EXPERIMENTAL = 4
    COMPUTED = 5
    STANDARDIZED = 6
    AUGMENTED = 7
    ALIGNED = 8
    COMPACT = 9
    UNITS_ANGSTROMS = 10
    UNITS_NANOMETERS = 11
    UNITS_PIXEL = 12
    UNITS_POINTS = 13
    UNITS_STDBONDS = 14
    UNITS_UNKNOWN = 255


class ProjectCategory(object):
    MLSCN = 1
    MPLCN = 2
    MLSCN_AP = 3
    MPLCN_AP = 4
    JOURNAL_ARTICLE = 5
    ASSAY_VENDOR = 6
    LITERATURE_EXTRACTED = 7
    LITERATURE_AUTHOR = 8
    LITERATURE_PUBLISHER = 9
    RNAIGI = 10
    OTHER = 255


ELEMENTS = {
    1: 'H',
    2: 'He',
    3: 'Li',
    4: 'Be',
    5: 'B',
    6: 'C',
    7: 'N',
    8: 'O',
    9: 'F',
    10: 'Ne',
    11: 'Na',
    12: 'Mg',
    13: 'Al',
    14: 'Si',
    15: 'P',
    16: 'S',
    17: 'Cl',
    18: 'Ar',
    19: 'K',
    20: 'Ca',
    21: 'Sc',
    22: 'Ti',
    23: 'V',
    24: 'Cr',
    25: 'Mn',
    26: 'Fe',
    27: 'Co',
    28: 'Ni',
    29: 'Cu',
    30: 'Zn',
    31: 'Ga',
    32: 'Ge',
    33: 'As',
    34: 'Se',
    35: 'Br',
    36: 'Kr',
    37: 'Rb',
    38: 'Sr',
    39: 'Y',
    40: 'Zr',
    41: 'Nb',
    42: 'Mo',
    43: 'Tc',
    44: 'Ru',
    45: 'Rh',
    46: 'Pd',
    47: 'Ag',
    48: 'Cd',
    49: 'In',
    50: 'Sn',
    51: 'Sb',
    52: 'Te',
    53: 'I',
    54: 'Xe',
    55: 'Cs',
    56: 'Ba',
    57: 'La',
    58: 'Ce',
    59: 'Pr',
    60: 'Nd',
    61: 'Pm',
    62: 'Sm',
    63: 'Eu',
    64: 'Gd',
    65: 'Tb',
    66: 'Dy',
    67: 'Ho',
    68: 'Er',
    69: 'Tm',
    70: 'Yb',
    71: 'Lu',
    72: 'Hf',
    73: 'Ta',
    74: 'W',
    75: 'Re',
    76: 'Os',
    77: 'Ir',
    78: 'Pt',
    79: 'Au',
    80: 'Hg',
    81: 'Tl',
    82: 'Pb',
    83: 'Bi',
    84: 'Po',
    85: 'At',
    86: 'Rn',
    87: 'Fr',
    88: 'Ra',
    89: 'Ac',
    90: 'Th',
    91: 'Pa',
    92: 'U',
    93: 'Np',
    94: 'Pu',
    95: 'Am',
    96: 'Cm',
    97: 'Bk',
    98: 'Cf',
    99: 'Es',
    100: 'Fm',
    101: 'Md',
    102: 'No',
    103: 'Lr',
    104: 'Rf',
    105: 'Db',
    106: 'Sg',
    107: 'Bh',
    108: 'Hs',
    109: 'Mt',
    110: 'Ds',
    111: 'Rg',
    112: 'Cp',
    113: 'ut',
    114: 'uq',
    115: 'up',
    116: 'uh',
    117: 'us',
    118: 'uo',
}

greenprint("[+] Loaded Variables")