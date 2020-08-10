import os
import re
import lxml
import base64
import shutil
import requests
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

class Image_lookup():
    '''
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
    self.image_db_entry
        Either a Base64 Encoded string of the raw response 
        or a file object opened in binary mode

    '''
    def __init__(self, record_to_request: str ,input_type = "name" , image_as_base64 = True, temp_file = "image"):
        #############################
        #if its running as the discord app or was implicitly called with it set to true
        # greenprint("[+] Running as Discord Attachment")
        # greenprint("[+] Not running as Discord Attachment")
        #print(str(os.environ['DISCORDAPP']))
        if image_as_base64 == True:
            self.base64_save = True
            greenprint("[+] Encoding Image as Base64")
        # running standalone
        elif image_as_base64 == False :
            self.base64_save = False
            self.filename    = temp_file + ".png"
            greenprint("[+] Saving image as {}".format(self.filename))
        if search_validate(input_type) :#in pubchem_search_types:
            greenprint("searching for an image : " + record_to_request)
            # fixes local code/context to work with url/remote context
            if input_type  == "iupac_name":
                self.thing_type = "name"
            
            else :
                self.thing_type = input_type
                self.record_to_request  = record_to_request
                self.request_url        = requote_uri("{}/compound/{}/{}/PNG".format(\
                                            API_BASE_URL,self.thing_type,self.record_to_request))
            blueprint("[+] Requesting: " + makered(self.request_url))
            try:
                self.rest_request = requests.get(self.request_url)
            except :
                redprint("[-] Request failure at local level")
            #check for errors, haha its backwards
            # True means no error
            if self.was_there_was_an_error() == True:
            # request good
                if self.base64_save == False :
                    try:
                        #write temp image to file
                        with open(self.filename, "wb") as temp_file:
                            temp_file.decode_content = True
                            shutil.copyfileobj(self.rest_request.raw, temp_file)
                        # open file in read only for the fileobject
                        self.image_storage = open(temp_file, "rb")
                    except:
                        redprint("[-] Exception when opening or writing image temp file")
                elif self.base64_save == True:
                    print(self.rest_request.content)
                    self.image_storage = base64.b64encode(self.rest_request.content)
                else:
                    redprint("[-] Error with Class Variable self.base64_save")
        else:
            redprint("[-] Input type was wrong for Image Search")
            return None

    def was_there_was_an_error(self):
        '''
Returns True if no error
        '''
        # server side error]
        set1 = [404,504,503,500]
        set2 = [400,405,501]
        set3 = [500]
        if self.rest_request.status_code in set1 :
            blueprint("[-] Server side error - No Image Available in REST response")
            return False # "[-] Server side error - No Image Available in REST response"
        if self.rest_request.status_code in set2:
            redprint("[-] User error in Image Request")
            return False # "[-] User error in Image Request"
        if self.rest_request.status_code in set3:
            #unknown error
            blueprint("[-] Unknown Server Error - No Image Available in REST response")
            return False # "[-] Unknown Server Error - No Image Available in REST response"
        # no error!
        if self.rest_request.status_code == 200:
            return True

TESTING = True

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
    Image_lookup(each[0],each[1] , image_as_base64=False,temp_file=each[0])
    ###################################################################
    # then we test the "is it stored locally?" function
    # doesnt need a timer, not gonna ban myself from my own service
    ###################################################################
#for each in test_query_list:
#    Image_lookup(each[0],each[1])

