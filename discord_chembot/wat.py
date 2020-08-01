import lxml
import requests
from bs4 import BeautifulSoup
from requests.utils import requote_uri

# Filter None values from kwargs
#kwargs = dict((k, v) for k, v in kwargs.items() if v is not None)

#################################################################################
# Color Printing 
#################################################################################
import colorama
from colorama import init
init()
from colorama import Fore, Back, Style
#Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
#Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
#Style: DIM, NORMAL, BRIGHT, RESET_ALL

#make them global scope for testing purposes
blueprint = lambda text: print(Fore.BLUE + ' ' +  text + ' ' + Style.RESET_ALL)
greenprint = lambda text: print(Fore.GREEN + ' ' +  text + ' ' + Style.RESET_ALL)
redprint = lambda text: print(Fore.RED + ' ' +  text + ' ' + Style.RESET_ALL)

################################################################################
## TESTING VARS
################################################################################

TESTING = True
#TESTING = False
#The sqlite :memory: identifier is the default if no filepath is present. 
# Specify sqlite:// and nothing else:
#e = create_engine('sqlite://')
TEST_DB = 'sqlite://'

################################################################################
################################################################################

# pubchem REST API service
pubchem_search_types = ["iupac_name", "cid", "cas"]
API_BASE_URL         = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug'

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
        self.request_url        = requote_uri("{}/compound/{}/{}/description/XML".format(\
                                    API_BASE_URL,self.thing_type,self.record_to_request))
        blueprint("[+] Requesting: ")
        redprint(self.request_url)
        #make the request
        self.request_return     = requests.get(self.request_url)
        print(self.request_return)
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

if TESTING == True:
    #pubchemREST_Description_Request("methanol","iupac_name")
    #pubchemREST_Description_Request("caffeine","iupac_name")
    #pubchemREST_Description_Request("water","iupac_name")
    pubchemREST_Description_Request("methylene chloride","iupac_name")
    #ozone
    #pubchemREST_Description_Request("24823","cid")
    # phosphorus
    #pubchemREST_Description_Request("5462309","cid")
    # bisphenol-a
    pubchemREST_Description_Request("6623","cid")

