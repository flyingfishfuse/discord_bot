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
################################################################################
"""

Molecule visualizer
   -  defaults to 2-d because 3-d will take more overhead
    - contains the code for requesting pubchem images
        - might move to pubchem file, I dunno.

"""

__author__ = 'Adam Galindo'
__email__ = 'null@null.com'
__version__ = '1'
__license__ = 'GPLv3'

import pybel
from variables_for_reality import TESTING
from variables_for_reality import greenprint,redprint,blueprint,makered
from database_setup import Database_functions,Compound,Composition,TESTING
from variables_for_reality import lookup_input_container, lookup_output_container

###############################################################################
# defaults to 2-d because 3-d will take more overhead
class TwoDimensional_Image_from_SMILES():
    '''
    SMILES string : str
    out_file defaults to "mol_img" with proceeding index
    '''
    def __init__(self, SMILES_input, out_file = "mol_img"):
        mymol = readstring("smi", "CCCC")
        print(mymol.molwt)
        pass

class ThreeDimensional_Image_from_SMILES():
    def __init__(self, SMILES_input):
        pass