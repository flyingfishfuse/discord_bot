from variables_for_reality import function_message
from variables_for_reality import greenprint,redprint,blueprint
from variables_for_reality import lookup_input_container, lookup_output_container
from database_setup import Database_functions,Compound,Composition,TESTING
import pubchempy as pubchem
import re

###############################################################################
class Pubchem_lookup():
    '''
Class to perform lookups on CID's and IUPAC names
Also does chempy translation to feed data to the calculation engine
    '''
    def __init__(self, user_input, type_of_input):
        self.user_input     = user_input
        self.type_of_input  = type_of_input
        self.validate_user_input(self.user_input , self.type_of_input)

    def help_message():
        return """
input CID/CAS or IUPAC name or synonym
Provide a search term and "term type", term types are "cas" , "iupac_name" , "cid"
Example 1 : .pubchem_lookup methanol iupac_name
Example 2 : .pubchem_lookup 3520 cid
Example 3 : .pubchem_lookup 113-00-8 cas
"""
###############################################################################
    def reply_to_query(message_object):
        '''    
        Just accepts an object of your choice, then you import the 
        lookup_output_container to your main file and work in that file

        The commented out code is for turning everything to a string
        from a list or string
        ''' 
        #list_to_string = lambda list_to_convert: ''.join(list_to_convert)
        #if isinstance(message,list):
        #    message = list_to_string(message) 
        #temp_array = [message]
        global lookup_output_container
        lookup_output_container.append(message_object)
        if TESTING == True:
            blueprint("=============================================")
            greenprint("[+] Sending the following reply to output container")
            print(lookup_output_container)
            blueprint("=============================================")

###############################################################################
    #def parse_lookup_to_chempy(self, pubchem_lookup : list):
    #    '''
    #    creates a chempy something or other based on what you feed it
    #    like cookie monster
    #    '''
        #lookup_cid       = pubchem_lookup[0].get('cid')
    #    lookup_formula    = pubchem_lookup[1].get('formula')
        #lookup_name      = pubchem_lookup[2].get('name')
        #try:
        #    greenprint(chempy.Substance.from_formula(lookup_formula))
        #except Exception:
        #    function_message("asdf", "blue")
###############################################################################

    def user_input_was_wrong(type_of_pebkac_failure : str, bad_string = ""):
        """
        You can put something funny here!
            This is something the creator of the bot needs to modify to suit
            Thier community.
        """
        user_is_a_doofus_CID_message        = 'Stop being a doofus! Accepted types are "iupac_name","cas" or "cid" '
        user_is_a_doofus_input_id_message   = 'bloop '
        user_is_a_doofus_formula_message    = "Stop being a doofus and feed me a good formula!"
        user_is_a_doofus_form_react_message = "the following input was invalid: " + bad_string 
        user_is_a_doofus_form_prod_message  = "the following input was invalid: " + bad_string
        #user_is_a_doofus_form_gen_message  = "the following input was invalid: " + bad_string
        if type_of_pebkac_failure   == "pubchem_lookup_by_name_or_CID":
            Pubchem_lookup.reply_to_query(user_is_a_doofus_CID_message)
        elif type_of_pebkac_failure == "specifics":
            Pubchem_lookup.reply_to_query(user_is_a_doofus_formula_message)
        elif type_of_pebkac_failure == "formula_reactants":
            Pubchem_lookup.reply_to_query(user_is_a_doofus_form_react_message)
        elif type_of_pebkac_failure == "formula_products":
            Pubchem_lookup.reply_to_query(user_is_a_doofus_form_prod_message)
        elif type_of_pebkac_failure == "user_input_identification":
            Pubchem_lookup.reply_to_query(user_is_a_doofus_input_id_message)
        else:
            #change this to sonething reasonable
            Pubchem_lookup.reply_to_query(type_of_pebkac_failure)

    def lookup_failure(type_of_failure: str):
        """
        does what it says on the label, called when a lookup is failed
        """
        #TODO: find sqlalchemy exception object
        # why cant I find the type of object I need fuck me
        if type_of_failure == "SQL":
            global lookup_output_container
            lookup_output_container = ["SQL QUERY FAILURE"]
        elif type_of_failure == pubchem.PubChemPyError:
            ##global lookup_output_container
            lookup_output_container = ["chempy failure"]
        pass

    def validate_user_input(user_input: str, type_of_input:str):
        """
    User Input is expected to be the proper identifier.
        type of input is one of the following:
        cid , iupac_name , cas
    
        """
        import re
        cas_regex = re.compile('[1-9]{1}[0-9]{1,5}-\d{2}-\d')
        # seriously, 
        # if type_of_input in pubchem_search_types:
        # didnt work.
        # no idea why.
        pubchem_search_types = ["iupac_name", "cid", "cas"]
        fuck_this = lambda fuck: fuck in pubchem_search_types 
        if fuck_this(type_of_input) :#in pubchem_search_types:
            greenprint("user supplied a : " + type_of_input)
            try:
                if type_of_input == "cas":
                    try:
                        greenprint("[+} trying to match regular expression for CAS")
                        if re.match(cas_regex,user_input):
                            greenprint("[+] Good CAS Number")
                            internal_lookup = Database_functions.internal_local_database_lookup(user_input, type_of_input)
                            # if internal lookup is false, we do a remote lookup and then store the result
                            if internal_lookup == None or False:
                                redprint("[-] Internal Lookup returned false")
                                lookup_object = Pubchem_lookup.pubchem_lookup_by_name_or_CID(user_input, type_of_input)
                                Pubchem_lookup.reply_to_query(lookup_object)
                            # we return the internal lookup if the entry is already in the DB
                            # for some reason, asking if it's true doesn't work here
                            # so we use a NOT instead of an Equals.
                            elif internal_lookup != None or False:
                                greenprint("[+] Internal Lookup returned TRUE")
                                Pubchem_lookup.reply_to_query(internal_lookup)
                        else:
                            function_message("[-] Bad CAS Number validation CAS lookup checks", "red")                    
                    except Exception:
                        function_message('[-] Something happened in the try/except block for cas numbers', 'red')
                else:
                    try:
                        internal_lookup = Database_functions.internal_local_database_lookup(user_input, type_of_input)
                        if internal_lookup == None or False:
                            redprint("[-] Internal Lookup returned false")
                            lookup_object = Pubchem_lookup.pubchem_lookup_by_name_or_CID(user_input, type_of_input)
                            Pubchem_lookup.reply_to_query(lookup_object)
                        elif internal_lookup != None or False:
                            greenprint("[+] Internal Lookup returned TRUE")
                            Pubchem_lookup.reply_to_query(internal_lookup)
                        else:
                            function_message("[-] Something is wrong with the database", "red")
                    except Exception:
                        function_message("reached exception : name/cid lookup - control flow", "red")
            except Exception:
                function_message("reached the exception : input_type was wrong somehow" , "red")

        else:
            Pubchem_lookup.user_input_was_wrong("user_input_identification", user_input + " : " + type_of_input)  

    def pubchem_lookup_by_name_or_CID(compound_id, type_of_data:str):
        '''
        Provide a search term and record type
        requests can be CAS,CID,IUPAC NAME/SYNONYM

        outputs in the following order:
        CID, CAS, SMILES, Formula, Name

        Stores lookup in database if lookup is valid
        I know it looks like it can be refactored into a smaller block 
        but they actually require slightly different code for each lookup
        and making a special function to do that would be just as long probably
        I'll look at it
        TODO: SEARCH LOCAL BY CAS!!!!
        '''
        #make a thing
        return_relationships = []
        # you get multiple records returned from a pubchem search VERY often
        # so you have to choose the best one to store, This needs to be 
        # presented as an option to the user,and not programmatically 
        return_index = 0
        data = ["iupac_name","cid","cas"]
        if type_of_data in data:
            if type_of_data == ("iupac_name" or "cas"):                     
                try:
                    greenprint("[+] Performing Pubchem Query")
                    lookup_results = pubchem.get_compounds(compound_id,'name')
                except Exception :# pubchem.PubChemPyError:
                    function_message("lookup by NAME/CAS exception - name", "red")
                    Pubchem_lookup.user_input_was_wrong("pubchem_lookup_by_name_or_CID")
            elif type_of_data == "cid":
                try:
                    greenprint("[+] Performing Pubchem Query")
                    lookup_results = pubchem.Compound.from_cid(compound_id)
                except Exception :# pubchem.PubChemPyError:
                    function_message("lookup by NAME/CAS exception - name", "red")
                    Pubchem_lookup.user_input_was_wrong("pubchem_lookup_by_name_or_CID")
                #once we have the lookup results, do something
            if isinstance(lookup_results, list):# and len(lookup_results) > 1 :
                greenprint("[+] Multiple results returned ")
                for each in lookup_results:
                    redprint(each.molecular_formula)
                    query_appendix = [{'cid' : each.cid                 ,\
                            #dis bitch dont have a CAS NUMBER!
                            #'cas'       : each.cas                 ,\
                            'smiles'     : each.isomeric_smiles     ,\
                            'formula'    : each.molecular_formula   ,\
                            'molweight'  : each.molecular_weight    ,\
                            'charge'     : each.charge              ,\
                            'iupac_name' : each.iupac_name          }]
                    return_relationships.append(query_appendix)
                    ####################################################
                    #Right here we need to find a way to store multiple records
                    # and determine the best record to store as the main entry
                    ####################################################
                    #Database_functions.compound_to_database() TAKES A LIST
                    # first element of first element
                    #[ [this thing here] , [not this one] ]
                    redprint("=========RETURN RELATIONSHIPS=======multiple")
                    blueprint(str(return_relationships[return_index]))
                    redprint("=========RETURN RELATIONSHIPS=======multiple")
                    Database_functions.compound_to_database(return_relationships[return_index])
            
            # if there was only one result or the user supplied a CID for a single chemical
            elif isinstance(lookup_results, pubchem.Compound) :#\
              #or (len(lookup_results) == 1 and isinstance(lookup_results, list)) :
                greenprint("[+] One Result Returned!")
                query_appendix = [{'cid' : lookup_results.cid                 ,\
                            #'cas'       : lookup_results.cas                 ,\
                            'smiles'     : lookup_results.isomeric_smiles     ,\
                            'formula'    : lookup_results.molecular_formula   ,\
                            'molweight'  : lookup_results.molecular_weight    ,\
                            'charge'     : lookup_results.charge              ,\
                            'iupac_name' : lookup_results.iupac_name          }]
                return_relationships.append(query_appendix)
                redprint("=========RETURN RELATIONSHIPS=======")
                blueprint(str(return_relationships[return_index]))
                redprint("=========RETURN RELATIONSHIPS=======")
                Database_functions.compound_to_database(return_relationships[return_index])
            else:
                function_message("PUBCHEM LOOKUP BY CID : ELSE AT THE END", "red")
        #and then, once all that is done return the LOCAL database entry to
        # the calling function so this is just an API to the db code
        return_query = return_relationships[return_index]
        redprint("==BEGINNING==return query for pubchem/local lookup===========")
        query_cid    = return_query[0].get('cid')
        local_query  = Compound.query.filter_by(cid = query_cid).first()
        # you can itterate over the database query
        print(local_query)
        redprint("=====END=====return query for pubchem/local lookup===========")
        #after storing the lookup to the local database, retrive the local entry
        #This returns an SQLALchemy object
        return local_query
        # OR return the remote lookup entry, either way, the information was stored.

#testing stuff
if TESTING == True:
    ###################################################################
    # First we do some lookups to pull data and populate the database]
    #add more tests
    ###################################################################
    Pubchem_lookup("420","cid")
    Pubchem_lookup("methanol","iupac_name")
    Pubchem_lookup("phenol","iupac_name")
    ###################################################################
    # then we test the "is it stored locally?" function
    ###################################################################
    Pubchem_lookup("420","cid")
    Pubchem_lookup("methanol","iupac_name")
    Pubchem_lookup("phenol","iupac_name")

