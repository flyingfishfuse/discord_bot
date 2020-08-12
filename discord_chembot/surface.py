# -*- coding: utf-8 -*-
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
####
################################################################################
"""
I dont know what to call this

It makes a "surface" represented by a numpy multidimensional array

The arrays are populated by ase.Atom() or database.Compound()

or both.
"""
import os
import ase
import sys
import numpy
import pubchem_test
from ase import formula
from ase import Atom,Atoms
from pubchem_test import Pubchem_lookup
from variables_for_reality import TESTING
from database_setup import Composition,Compound
from database_setup import Database_functions as database
from variables_for_reality import greenprint,redprint,blueprint,makered

# Need to make a metaclass to represent Atoms that uses the DB and all the libs
# Extending the Atom Class to add some information we need
# class Atom():
#    __init__(self):
#        pass

class Molecule(Compound):
    def __init__(self):
        pass


class Surface():
    def __init__(self,  material : dict, xyz_ints = (100,100,10)):
        '''
        Material is a dict of Compound names or a dict of chemical elements
            - palladium substrate doped with cobalt
                material = {"Pd" : 0.998 , "Co" : 0.002 }

            - Probabilities must solve to 1

        xyz_ints is a tuple
            - 100 units x 100 units x 10 units
                xyz_ints = (100, 100, 10)

        derp = numpy.random.choice( material_array , size = (x_lim , y_lim), p = doping_array)

        '''
        self.x_dimension        = xyz_ints[0]
        self.y_dimension        = xyz_ints[1]
        self.z_dimension        = xyz_ints[2]
        self.substrate          = material
        self.ATOMS              = False
        self.SUBSTANCE          = True
        self.make_grid(self.substrate)

    def make_grid(self):
        '''
        substrate is a name or iupac_name

        '''
        surface_size      = (self.x_dimension , self.y_dimension, self.z_dimension)
        primary_material  = []
        doping_floats     = []
        for key,value in self.substrate.items():
            if self.ATOMS == True:
            # list of CHEMICAL ELEMENTS
                primary_material.append(Atom(key))
                doping_floats.append(Atom(value))        
    # if we want to use Compounds
            elif self.SUBSTANCE == True:
            # do a db call here to grab entities
                primary_material.append(Pubchem_lookup(key, "iupac_name"))
                doping_floats.append(value)
        else:
            print("wat")
        surface_with_z = numpy.random.choice(a    = primary_material ,\
                                             size = surface_size     ,\
                                             p    = doping_floats     )
        self.grid_container = surface_with_z
        

try:
    if (__name__ == '__main__') and (TESTING == True):
        material = {"Pd" : 0.998 , "Co" : 0.002 }
        size_of  = (100, 100, 10)
        Surface(material, size_of)
except Exception as derp:
    print(derp) 