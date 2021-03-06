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
PubChemPy caching wrapper

Caching extension to the Python interface for the PubChem PUG REST service.

https://github.com/mcs07/PubChemPy

"""
import os
import re
import lxml
import base64
import requests
from PIL import Image
from io import BytesIO
import pubchempy as pubchem
from bs4 import BeautifulSoup
from requests.utils import requote_uri
from variables_for_reality import TESTING
from variables_for_reality import API_BASE_URL
from variables_for_reality import search_validate
from variables_for_reality import yellow_bold_print
from variables_for_reality import pubchem_search_types
from variables_for_reality import greenprint,redprint,blueprint,makered
from database_setup import Database_functions,Compound,Composition,TESTING
from variables_for_reality import lookup_input_container, lookup_output_container

from variables_for_reality import SAVE_BASE64

__author__ = 'Adam Galindo'
__email__ = 'null@null.com'
__version__ = '1'
__license__ = 'GPLv3'

#import platform
#OS_NAME = platform.system()


###############################################################################
class pubchemREST_Description_Request():
    # hey it rhymes
    '''
    This class is to be used only with validated information
    Returns the description field using the XML return from the REST service
    Does Compounds ONLY!, Needs a second class or modifications to this one 
    To return a Substance type

    results are stored in :
        pubchemREST_Description_Request.parsed_results

    the url of the API call is stored in :
        pubchemREST_Description_Request.request_url
    '''
    def __init__(self, record_to_request: str ,input_type = 'iupac_name' ):
        if search_validate(input_type) :#in pubchem_search_types:
            if TESTING           == True:
                greenprint("searching for a Description : " + record_to_request)
            if input_type        == "iupac_name":
                self.thing_type  = "name"
            else :
                self.thing_type  = input_type
        self.record_to_request   = record_to_request
        self.request_url         = requote_uri("{}/compound/{}/{}/description/XML".format(\
                                    API_BASE_URL,self.thing_type,self.record_to_request))
        blueprint("[+] Requesting: " + makered(self.request_url) + "\n")
        self.request_return      = requests.get(self.request_url)
        self.soupyresults        = BeautifulSoup(self.request_return.text , features='lxml').contents[1]
        self.parsed_result       = self.soupyresults.find_all(lambda tag:  tag.name =='description')
        if self.parsed_result    != [] :
            self.parsed_result   = str(self.parsed_result[0].contents[0])
            greenprint("[+] Description Found!")
            print(self.parsed_result)
        elif self.parsed_result  == [] or NoneType:
            blueprint("[-] No Description Available in XML REST response")
            self.parsed_result   = "No Description Available in XML REST response"
###############################################################################
class Image_lookup():
    '''
    https://stackoverflow.com/questions/7877282/how-to-send-image-generated-by-pil-to-browser
Performs a pubchem or chemspider image lookup
    Image name is saved as:
        filename = temp_file + ".png"
    Set image_as_base64 to TRUE to save image as base64 in the DB

INPUT:
    input_type :str
        Default : name ( can be fed "iupac_name" from the rest of the app)
    image_as_base64 :bool
        Default = True
    temp_file :str 
        Default : image

OUTPUT:
    self.rest_request
        - Response from remote server
    self.image_storage
        Either a Base64 Encoded string of the raw response 
        or a PIL Image

    '''
    def __init__(self, record_to_request: str , image_as_base64 = True , input_type = "name" , temp_file = "image"):
        #############################
        if search_validate(input_type) :#in pubchem_search_types:
            greenprint("searching for an image : " + record_to_request)
            # fixes local code/context to work with url/remote context
            if input_type  == "iupac_name":
                self.input_type = "name"
            else :
                self.input_type = input_type
            self.request_url        = requote_uri("{}/compound/{}/{}/PNG".format(\
                                            API_BASE_URL,self.input_type,record_to_request))
            blueprint("[+] Requesting: " + makered(self.request_url))
            self.rest_request = requests.get(self.request_url)
            if self.was_there_was_an_error() == False:
            # request good
                # Store image
            # we want an image file
                if image_as_base64 == False:
                    try:
                        self.filename    = temp_file + ".png"
                        greenprint("[+] Saving image as {}".format(self.filename))
                        self.image_storage = Image.open(BytesIO(self.rest_request.content))
                        self.image_storage.save(self.filename, format = "png")                       
                        self.image_storage.close()
                    except Exception as derp:
                        redprint("[-] Exception when opening or writing image file")
                        print(derp)
            # we want a base64 string
                elif image_as_base64 == True :
                    self.image_storage = self.encode_image_to_base64(self.image_storage)
                else:
                    redprint("[-] Error with Class Variable self.base64_save")
        else:
            redprint("[-] Input type was wrong for Image Search")
            return None
     
    def encode_image_to_base64(self, image, image_format = "png"):
        '''
    stack overflow post
    https://stackoverflow.com/questions/52411503/convert-image-to-base64-using-python-pil   

        '''
        greenprint("[+] Encoding Image as Base64")
        buff = BytesIO()
        image.save(buff, format=image_format)
        img_str = base64.b64encode(buff.getvalue())
        return img_str

    # Convert Base64 to Image
    def decode_image_from_base64(self, data):
        buff = BytesIO(base64.b64decode(data))
        return Image.open(buff)
    
    def save_image(self, PIL_image, name, image_format):
        '''
    Saves image
        '''
        greenprint("[+] Saving image as {}".format(name))
        PIL_image.save(self.filename, format=image_format)

    def decode_and_save(self, base64_image, name, image_format):
        '''
Decodes a base64 string to an image and saves that
This helps display images in discord because they suck
and dont allow base64 as a uri anymore
        '''
        greenprint("[+] Decoding and Saving image as {}".format(name))
        decoded_image = self.decode_image_from_base64(base64_image) 
        decoded_image.save(name, format=image_format)


    def was_there_was_an_error(self):
        '''
Returns False if no error
        '''
        # server side error]
        set1 = [404,504,503,500]
        set2 = [400,405,501]
        set3 = [500]
        if self.rest_request.status_code in set1 :
            blueprint("[-] Server side error - No Image Available in REST response")
            yellow_bold_print("Error Code {}".format(self.rest_request.status_code))
            return True # "[-] Server side error - No Image Available in REST response"
        if self.rest_request.status_code in set2:
            redprint("[-] User error in Image Request")
            yellow_bold_print("Error Code {}".format(self.rest_request.status_code))
            return True # "[-] User error in Image Request"
        if self.rest_request.status_code in set3:
            #unknown error
            blueprint("[-] Unknown Server Error - No Image Available in REST response")
            yellow_bold_print("Error Code {}".format(self.rest_request.status_code))
            return True # "[-] Unknown Server Error - No Image Available in REST response"
        # no error!
        if self.rest_request.status_code == 200:
            return False
###############################################################################
class Pubchem_lookup():
    '''
Class to perform lookups on CID's and IUPAC names

OUTPUTS:
    self.lookup_object
        - The SQLAlchemy or PubChem.Compound Object
        - Attemps local SQLAlchemy object first
    self.local_output_container
        - The Human Readable Representation of the Data
    self.image
        -   image data

NOTE: to grab a description requires a seperate REST request.
    '''
    def __init__(self, user_input, type_of_input):
        self.internal_lookup_bool   = bool
        self.user_input             = user_input
        self.type_of_input          = type_of_input
        self.grab_description       = True
        self.grab_image             = True
        if TESTING == True:
            self.local_output_container = {} # {"test" : "sample text"} # uncomment to supress linter errors
                                                                        # in the IDE
        else: 
            self.local_output_container = {}
        #do the thing 
        self.validate_user_input(self.user_input , self.type_of_input)
        #say the thing
        self.reply_to_query()


    def help_message():
        return """
input CID/CAS or IUPAC name or synonym
Provide a search term and "term type", term types are "cas" , "iupac_name" , "cid"
Example 1 : .pubchem_lookup methanol iupac_name
Example 2 : .pubchem_lookup 3520 cid
Example 3 : .pubchem_lookup 113-00-8 cas
"""
###############################################################################
    def reply_to_query(self):
        '''    
        oh wow nothing to document?
        This is the end of the line for this stream of operations!
        Now that its in the global output container, You can use your 
        Interface of choice with an easily parsed block of something!
        ''' 
        temp_array = []
        global lookup_output_container
        lookup_output_container.clear()
        temp_array.append(self.lookup_object)
        temp_array.append(self.lookup_description)
        lookup_output_container.append(temp_array)
        #redprint("=============================================")
        #greenprint("[+] Sending the following reply via Local output container")
        #blueprint(str(lookup_output_container))
        #redprint("=============================================")
        # clean up just in case
        #self.local_output_container.clear()


    def user_input_was_wrong(self , type_of_pebkac_failure : str, bad_string = ""):
        """
        You can put something funny here!
            This is something the creator of the bot needs to modify to suit
            Thier community.
        """
        derp = {"bad_CAS" :"Bad CAS input"                     ,\
                "bad_CID" : "Input given was " + bad_string    ,\
                "lookup_function" : bad_string                 ,\
                "input_id" : 'bloop'                            }
        # clear the container for cleanliness
        self.local_output_container.clear()
        self.local_output_container[type_of_pebkac_failure] = derp.get(type_of_pebkac_failure) + bad_string + "\n"

    def do_lookup(self, user_input, type_of_input):
        '''
        after validation, the user input is used in 
        Pubchem_lookup.pubchem_lookup_by_name_or_CID() 
        pubchemREST_Description_Request(user_input, type_of_input)
        Image_lookup()
        '''
        try:
            internal_lookup = Database_functions.internal_local_database_lookup(user_input, type_of_input)
            # if internal lookup is false, we do a remote lookup and then store the result
            if internal_lookup == None or False:
                redprint("[-] Internal Lookup returned false")
                self.internal_lookup_bool = False
                # we grab things in the proper order
                # description first
                try:
                    description_lookup      = pubchemREST_Description_Request(user_input, type_of_input)
                except Exception as derp:
                    redprint("[-] Description Lookup Failed")
                    print(derp)
                    self.lookup_description = "Description Lookup Failed"
                #then image
                try:
                    #if (SAVE_BASE64 == True) :
                    image_lookup            = Image_lookup(user_input               ,\
                                                            image_as_base64 = True     ,\
                                                            input_type      = type_of_input ,\
                                                            temp_file       = user_input      )
                except Exception as derp:
                    redprint("[-] Image Lookup Failed")
                    print(derp)    
                    image_lookup = None
            # no image
                if image_lookup == None:
                    self.image              = "No Image Available"
            # image as base64
                elif (image_lookup!= None) and (DISPLAY_FROM_BASE64 == True):
                    self.image              = str(image_lookup.image_storage)
            # image as file    
                elif (image_lookup!= None) and (DISPLAY_FROM_BASE64 == False):
                    self.image              = image_lookup.image_storage
                    self.image_filename     = image_lookup.filename
                else:
                    redprint("[-] Something wierd happened in do_lookup")
                # Now pubchem
                self.lookup_description     = description_lookup.parsed_result
                self.lookup_object          = self.pubchem_lookup_by_name_or_CID(user_input, type_of_input)
            # we return the internal lookup if the entry is already in the DB
            # for some reason, asking if it's true doesn't work here so we use a NOT instead of an Equals.
            elif internal_lookup != None or False:
                greenprint("[+] Internal Lookup returned TRUE")
                self.internal_lookup_bool = True
                self.lookup_description   = internal_lookup.description
                self.lookup_object        = internal_lookup
                self.image                = internal_lookup.image
                #redprint("==BEGINNING==return query for DB lookup===========")
                #greenprint(str(internal_lookup))
                #redprint("=====END=====return query for DB lookup===========")
        # its in dire need of proper exception handling              
        except Exception as derp:
            redprint('[-] Something happened in the try/except block for the function do_lookup')
            print(derp)

    def validate_user_input(self, user_input: str, type_of_input:str):
        """
User Input is expected to be the proper identifier.
    type of input is one of the following: cid , iupac_name , cas

Ater validation, the user input is used in :
    Pubchem_lookup.do_lookup()
        Pubchem_lookup.pubchem_lookup_by_name_or_CID()
        
        """
        import re
        cas_regex = re.compile('[1-9]{1}[0-9]{1,5}-\d{2}-\d')
        if search_validate(type_of_input) :#in pubchem_search_types:
            greenprint("user supplied a : " + type_of_input)
            try:
                if type_of_input == "cas":
                    greenprint("[+} trying to match regular expression for CAS")
                    if re.match(cas_regex,user_input):
                        greenprint("[+] Good CAS Number")
                        self.do_lookup(user_input, type_of_input)
                    else:
                        redprint("[-] Bad CAS Number")
                        self.user_input_was_wrong("bad_CAS", user_input)
                elif type_of_input == "cid" or "iupac_name":
                    self.do_lookup(user_input, type_of_input)
                else:
                    redprint("[-] Something really wierd happened inside the validation flow")
            except Exception as derp:
                redprint("[-] reached the exception ")
                print(derp)
        else:
            self.user_input_was_wrong("input_type" , type_of_input)  

    def pubchem_lookup_by_name_or_CID(self , compound_id, type_of_data:str):
        '''
        Provide a search term and record type
        requests can be CAS,CID,IUPAC NAME/SYNONYM

        outputs in the following order:
        CID, CAS, SMILES, Formula, Name

        Stores lookup in database if lookup is valid
        '''
        return_relationships = []
        # you get multiple records returned from a pubchem search VERY often
        # so you have to choose the best one to store, This needs to be 
        # presented as an option to the user,and not programmatically 
        # return_index is the result to return, 0 is the first one
        return_index = 0
        data = ["iupac_name","cid","cas"]
        if type_of_data in data:
        # different methods are used depending on the type of input
        # one way
            if type_of_data == ("iupac_name" or "cas"):                     
                try:
                    greenprint("[+] Performing Pubchem Query")
                    lookup_results = pubchem.get_compounds(compound_id,'name')
                except Exception :# pubchem.PubChemPyError:
                    redprint("[-] Error in pubchem_lookup_by_name_or_CID : NAME exception")
                    self.user_input_was_wrong("pubchem_lookup_by_name_or_CID")
        # CID requires another way
            elif type_of_data == "cid":
                try:
                    greenprint("[+] Performing Pubchem Query")
                    lookup_results = pubchem.Compound.from_cid(compound_id)
                except Exception :# pubchem.PubChemPyError:
                    redprint("lookup by NAME/CAS exception - name")
                    self.user_input_was_wrong("pubchem_lookup_by_name_or_CID")
        # once we have the lookup results, do something
            if isinstance(lookup_results, list):# and len(lookup_results) > 1 :
                greenprint("[+] Multiple results returned ")
                for each in lookup_results:
                    query_appendix = [{'cid' : each.cid                                 ,\
                            #'cas'                     : each.cas                       ,\
                            'smiles'                   : each.isomeric_smiles           ,\
                            'formula'                  : each.molecular_formula         ,\
                            'molweight'                : each.molecular_weight          ,\
                            'charge'                   : each.charge                    ,\
                            'bond_stereo_count'        : each.bond_stereo_count         ,\
                            'bonds'                    : each.bonds                     ,\
                            'rotatable_bond_count'     : each.rotatable_bond_count      ,\
                            'multipoles_3d'            : each.multipoles_3d             ,\
                            'mmff94_energy_3d'         : each.mmff94_energy_3d          ,\
                            'mmff94_partial_charges_3d': each.mmff94_partial_charges_3d ,\
                            'atom_stereo_count'        : each.atom_stereo_count         ,\
                            'h_bond_acceptor_count'    : each.h_bond_acceptor_count     ,\
                            'feature_selfoverlap_3d'   : each.feature_selfoverlap_3d    ,\
                            'cactvs_fingerprint'       : each.cactvs_fingerprint        ,\
                            'iupac_name'               : each.iupac_name                ,\
                            'description'              : self.lookup_description        ,\
                            'image'                    : self.image                     }]
                    return_relationships.append(query_appendix)
                    # Right here we need to find a way to store multiple records
                    # and determine the best record to store as the main entry
                    #compound_to_database() TAKES A LIST!!! First element of first element
                    #[ [this thing here] , [not this one] ]
                    #print(return_relationships[return_index])
                    Database_functions.compound_to_database(return_relationships[return_index])
            
            # if there was only one result or the user supplied a CID for a single chemical
            elif isinstance(lookup_results, pubchem.Compound) :#\
              #or (len(lookup_results) == 1 and isinstance(lookup_results, list)) :
                greenprint("[+] One Result Returned!")
                query_appendix = [{'cid'               : lookup_results.cid                 ,\
                            #'cas'                     : lookup_results.cas                 ,\
                            'smiles'                   : lookup_results.isomeric_smiles     ,\
                            'formula'                  : lookup_results.molecular_formula   ,\
                            'molweight'                : lookup_results.molecular_weight    ,\
                            'charge'                   : lookup_results.charge              ,\
                            'bond_stereo_count'        : each.bond_stereo_count             ,\
                            'bonds'                    : each.bonds                         ,\
                            'rotatable_bond_count'     : each.rotatable_bond_count          ,\
                            'multipoles_3d'            : each.multipoles_3d                 ,\
                            'mmff94_energy_3d'         : each.mmff94_energy_3d              ,\
                            'mmff94_partial_charges_3d': each.mmff94_partial_charges_3d     ,\
                            'atom_stereo_count'        : each.atom_stereo_count             ,\
                            'h_bond_acceptor_count'    : each.h_bond_acceptor_count         ,\
                            'feature_selfoverlap_3d'   : each.feature_selfoverlap_3d        ,\
                            'cactvs_fingerprint'       : each.cactvs_fingerprint            ,\
                            'iupac_name'               : each.iupac_name                    ,\
                            'description'              : self.lookup_description            ,\
                            'iupac_name'  : lookup_results.iupac_name                       ,\
                            # Local stuff
                            'description' : self.lookup_description                         ,\
                            'image'       : self.image                                      }]
                return_relationships.append(query_appendix)
                #print(query_appendix)
                Database_functions.compound_to_database(return_relationships[return_index])
            else:
                redprint("PUBCHEM LOOKUP BY CID : ELSE AT THE END")
    #after storing the lookup to the local database, retrive the local entry
    #This returns an SQLALchemy object
        return_query = return_relationships[return_index]
        query_cid    = return_query[0].get('cid')
        local_query  = Compound.query.filter_by(cid = query_cid).first()
        return local_query
    # OR return the remote lookup entry, either way, the information was stored
    # and you get a common "api" to draw data from.


###############################################################################
# TODO: Testing procedure requires bad data craft a list of shitty things a 
# user can attempt. Be malicious and stupid with it
# break shit
greenprint("[+] Loaded Pubchem Lookup")

try:
    if __name__ == '__main__':
        if TESTING == True:
            import time
            #craft a list of queries to test with
            test_query_list = [["420","cid"],\
                ["methanol","iupac_name"],\
                ["phenol","iupac_name"],\
                ["methylene chloride","iupac_name"] ,\
                ["6623","cid"],\
                ["5462309","cid"],\
                ["24823","cid"],\
                ["water","iupac_name"]]
    ###################################################################
    # First we do some lookups to pull data and populate the database
    #add more tests
    ###################################################################
        for each in test_query_list:
            time.sleep(5)
            Pubchem_lookup(each[0],each[1])
    ###################################################################
    # then we test the "is it stored locally?" function
    # doesnt need a timer, not gonna ban myself from my own service
    ###################################################################
        for each in test_query_list:
            Pubchem_lookup(each[0],each[1])
except Exception as derp :
    print(derp)
    redprint("[-] Cannot run file for some reason")

