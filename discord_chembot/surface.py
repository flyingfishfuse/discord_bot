import numpy
import sys
import os
import ase
from ase import Atom,Atoms
from ase import formula
from variables_for_reality import greenprint,redprint,blueprint,makered
from variables_for_reality import TESTING
from database_setup import Composition,Compound
from database_setup import Database_functions as database
# Need to make a metaclass to represent Atoms that uses the DB and all the libs
# Extending the Atom Class to add some information we need
# class Atom():
#    __init__(self):
#        pass

#should it inherit from Compound?
class Surface():
    def __init__(self,  material : str , doping: list , x_limit : int, y_limit : int, doping_coefficient: list):
        '''
        Material is a single Compound or dict

        Doping is a list
        Doping coeffecient is a list that matches "doping"

            doping   = ["Pd",     "Co"  ]
            dop_coef = [ 0.998  , 0.002 ]

            the probabilities must match the index of the item they probabilititate
            E.G. Pd is 100% and Co is 0.2%
            probabilities must solve to 1

        '''
        self.x_dimension        = x_limit
        self.y_dimension        = y_limit
        self.substrate          = material.formula
        self.doping             = doping
        self.doping_coeffecient = doping_coefficient


    def make_grid(substrate: str, doping_material, depth: int):
        '''
        substrate is an Atom
        material is an Atom from ase
        depth is layers
        '''
        plane1 = [Atom(self.substrate.formula)]
        
        for each in doping_material:
            plane1.append(Atom(each))
        doping_coefficient = [0.998 , 0.002]
        
        derp = numpy.random.choice(a    = herp                     ,\
                                   size = (self.x_dimension , self.y_dimension, self.thickness),\
                                   p    = doping_coeffecient)
        
        thing_to_place = Atom(symbol=doping_material)
        #empty array to init
        self.doped_substrate = []
        

#x_lim = 100
#y_lim = 100
#herp = [Atom("Pd"), Atom("Co")]
#doping_coefficient = [1,0.002]
#derp = numpy.random.choice(herp , size = (x_lim , y_lim), p = doping_coeffecient)