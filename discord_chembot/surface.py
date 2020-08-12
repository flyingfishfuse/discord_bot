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
import pubchem_test
from pubchem_test import Pubchem_lookup
# Need to make a metaclass to represent Atoms that uses the DB and all the libs
# Extending the Atom Class to add some information we need
# class Atom():
#    __init__(self):
#        pass

#should it inherit from Compound?
class Surface():
    def __init__(self,  material : dict, x_limit : int, y_limit : int, z_limit : int):
        '''
        Material is a dict of Compound or a dict of chemical elements
            - palladium substrate doped with cobalt
                material = {"Pd" : 0.998 , "Co" : 0.002 }
            
            derp = numpy.random.choice( material_array , size = (x_lim , y_lim), p = doping_array)

            the probabilities must match the index of the item they probabilititate
            E.G. Pd is 100% and Co is 0.2%
            probabilities must solve to 1

        '''
        self.x_dimension        = x_limit
        self.y_dimension        = y_limit
        self.z_dimension        = z_limit
        self.substrate          = material
        self.ATOMS              = False
        self.SUBSTANCE          = True
        self.make_grid(self.substrate)

    def make_grid(self, substrate : dict):
        '''
        substrate is a name or iupac_name

        '''
        primary_material = []
        doping_floats  = []
        for key,value in substrate.items():
            if self.ATOMS == True:
            # list of CHEMICAL ELEMENTS
                primary_material.append(Atom(key))
                doping_floats.append(Atom(value))        
    # if we want to use Compounds
            elif self.SUBSTANCE == True:
                # do a db call here to grab entities
                primary_material.append(Pubchem_lookup(key, "iupac_name"))
            # list of FLOATS
                doping_floats.append(value)
        else:
            print("wat")
        surface_with_z = numpy.random.choice(a    = primary_material                                       ,\
                                             size = (self.x_dimension , self.y_dimension, self.z_dimension),\
                                             p    = doping_floats)
        self.grid_container = surface_with_z
        

try:
    if __name__ == '__main__':
        if TESTING == True:
            Surface("Pd", "Co", 100, 100, 10, [0.998 , 0.002])
except Exception as derp:
    print(derp) 