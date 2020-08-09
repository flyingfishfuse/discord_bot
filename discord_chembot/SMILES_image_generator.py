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
import requests
import pubchempy as pubchem
from bs4 import BeautifulSoup
from requests.utils import requote_uri
from variables_for_reality import TESTING
from variables_for_reality import API_BASE_URL
from variables_for_reality import search_validate
from variables_for_reality import pubchem_search_types
from variables_for_reality import greenprint,redprint,blueprint,makered
from database_setup import Database_functions,Compound,Composition,TESTING
from variables_for_reality import lookup_input_container, lookup_output_container

class Image_lookup():
    '''
Performs a pubchem or chemspider image lookup
    Image name is saved as:
        filename = temp_file + ".png"

    input_type :str
        Default : iupac_name
    temp_file :str 
        Default : image
    '''
    def __init__(self, record_to_request: str ,input_type = 'iupac_name', temp_file = "image" ):
        filename        = temp_file + ".png"
        self.temp_file  = open(filename, mode = "w+")
        if search_validate(input_type) :#in pubchem_search_types:
            if TESTING == True:
                greenprint("searching for an image : " + record_to_request)
            if input_type  == "iupac_name":
                self.thing_type = "name"
            else :
                self.thing_type = input_type
        self.record_to_request  = record_to_request
        self.request_url        = requote_uri("{}/compound/{}/{}/PNG".format(\
                                    API_BASE_URL,self.thing_type,self.record_to_request))
        blueprint("[+] Requesting: " + makered(self.request_url) + "\n")
        self.request_return     = requests.get(self.request_url)
        blueprint("[-] No Image Available in REST response")
    
    def save_image(self):
        self.temp_file.append()


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