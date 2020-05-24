#/usr/bin/python3

import colorama
from colorama import init
init()
from colorama import Fore, Back, Style


blueprint = lambda text: print(Fore.BLUE + ' ' +  text + ' ' + Style.RESET_ALL)

greenprint = lambda text: print(Fore.GREEN + ' ' +  text + ' ' + Style.RESET_ALL)

redprint = lambda text: print(Fore.RED + ' ' +  text + ' ' + Style.RESET_ALL)

#deprecated
#     def generate_element_validation_name_list(self):
#        from variables_for_reality import element_list , symbol_list , specifics_list
#        return_element_by_id = lambda element_id_input : mendeleev.element(element_id_input)
#        for element in range(1,118):
#            element_object = return_element_by_id(element)
#            element_list.append(element_object.name)
#            symbol_list.append(element_object.symbol)

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

specifics_list = ["physical" , "chemical", "nuclear", "ionization",\
        "isotopes", "oxistates"]
