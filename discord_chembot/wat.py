import lxml
import requests
from bs4 import BeautifulSoup
from variables_for_reality import TESTING
from variables_for_reality import API_BASE_URL, pubchem_search_types
from variables_for_reality import greenprint, redprint, blueprint
#just the usual linter errors
###############################################################################
# Additional REST request required, regrettably, return 
# values lack the description field
class pubchemREST_Description_Request():
    # hey it rhymes
    '''
    This class is to be used only with validated information
    Returns the description field using the XML return from the REST service
    Does Compounds ONLY!, Needs a second clas or modifications to this one 
    To return a Substance type
    '''
    def __init__(self, record_to_request: str ,input_type = 'iupac_name' ):
        # it doesnt work the other way elsewhere in the script, I dont know why
        # to avoid that issue im just using it for everything
        fuck_this = lambda fuck: fuck in pubchem_search_types 
        if fuck_this(input_type) :#in pubchem_search_types:
            if TESTING == True:
                greenprint("searching for a Description : " + input_type)
            if input_type  == "iupac_name":
                self.thing_type = "name"
            else :
                self.thing_type = input_type
        self.record_to_request  = record_to_request
        #do the thing
        self.do_the_thing()

    def do_the_thing(self):
        #finalized URL        
        self.request_url        = API_BASE_URL + "compound/" + self.thing_type + "/" +\
                                  self.record_to_request + "/description/XML"
        #make the request
        self.request_return     = requests.get(self.request_url)
        #make some soup
        self.soupyresults       = BeautifulSoup(self.request_return.content , 'lxml')
        #serve up the Descriptions
        self.descriptions       = self.soupyresults.find_all("Description")
        if self.descriptions != None:
            return self.descriptions
            greenprint(self.descriptions)
        else:
            return "No Description Available in XML REST response"
            #lambda tag:  tag.name =='Description' and tag.has_key('class') and tag['class'] == self.container_name)
