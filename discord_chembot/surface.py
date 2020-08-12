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
    def __init__(self,  material , doping_material , x_limit : int, y_limit : int, z_limit : int, doping_coefficient: list):
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
        self.z_dimension        = z_limit
        self.substrate          = material
        self.doping_material    = doping_material
        self.doping_coeffecient = doping_coefficient
        self.make_grid(self.substrate, self.doping_material)

    def make_grid(self, substrate, doping_material : list):
        '''

        '''
        self.substrate = substrate
        if ASE == True:
            plane1 = [Atom(self.substrate.formula)]
            for each in doping_material:
                plane1.append(Atom(each))
        elif SUBSTANCE == True:
            # do a db call here to grab entities
            plane1 = [Compound(self.substrate.formula)]
            for each in doping_material:
                plane1.append(Atom(each))
        else:
            print("wat")
        
        derp = numpy.random.choice(a    = plane1                     ,\
                                   size = (self.x_dimension , self.y_dimension, self.z_dimension),\
                                   p    = self.doping_coeffecient)
        
        #empty array to init
        self.doped_substrate = derp
        
Surface("Pd", "Co", 100, 100, 10, [0.998 , 0.002])
#x_lim = 100
#y_lim = 100
#herp = [Atom("Pd"), Atom("Co")]
#doping_coefficient = [1,0.002]
#derp = numpy.random.choice(herp , size = (x_lim , y_lim), p = doping_coeffecient)