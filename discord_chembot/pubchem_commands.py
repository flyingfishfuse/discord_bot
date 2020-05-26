def size_check_256(txt):
    if txt == None:
        return "iupac name Not Found"
    # print(len(txt))
    elif len(txt) < 255:
        return txt
    else:
        short = (str(txt[:100])+ " .....")
        return short
##############################################################################

class Pubchem_lookup(commands.Cog):
    '''
Class to perform lookups on CID's and IUPAC names
Also does chempy translation to feed data to the calculation engine
    '''
    def __init__(self):
        self.asdf                 = []
        self,lookup_result        = []
        self.name_lookup_result   = None
        name_lookup_results_list  = [] 
        print("loaded pubchem_commands")

    def pubchem_lookup_by_name_or_CID(self, compound_id:str or int):
        if isinstance(compound_id, str):
            name_lookup_results_list = pubchem.get_compounds(compound_id,\
                                        'name' , \
                                        list_return='flat')
        elif isinstance(compound_id, int):
            self.name_lookup_result = pubchem.Compound.from_cid(compound_id)

    def parse_lookup_to_chempy(self, pubchem_lookup : list):
        '''
        creates a chempy something or other based on what you feed it
        like cookie monster
        '''
        lookup_cid     = pubchem_lookup[0].get('cid')
        lookup_formula = pubchem_lookup[1].get('formula')
        lookup_name    = pubchem_lookup[2].get('name')
        return chempy.Substance.from_formula(lookup_formula)

    def pubchem_lookup_by_name_or_CID(self,compound_id:str or int):
        '''
        wakka wakka wakka
        '''
        return_relationships = list
        if isinstance(compound_id, str):
            lookup_results = pubchem.get_compounds(compound_id,'name',\
                                                list_return='flat')
            if isinstance(lookup_results, list):
                for each in lookup_results:
                    return_relationships.append([                   \
                    {'cid'     : each.cid}                         ,\
                    {'formula' : each.molecular_formula}           ,\
                    {'name'    : each.iupac_name}                  ])
            #TODO: fix this shit to make the above format
            else:
                return_relationships.append([                       \
                    {'cid'     : lookup_results.cid               },\
                    {'formula' : lookup_results.molecular_formula },\
                    {'name'    : lookup_results.iupac_name        }])

            return return_relationships
        elif isinstance(compound_id, int):
            lookup_results = pubchem.Compound.from_cid(compound_id)
            return_relationships.append([                          \
                {'cid'     : lookup_results.cid}                  ,\
                {'formula' : lookup_results.molecular_formula}    ,\
                {'name'    : lookup_results.iupac_name}           ])
            return return_relationships

##############################################################################

def parse_lookup_to_chempy(pubchem_lookup : list):
    '''
    creates a chempy something or other based on what you feed it
    like cookie monster
    '''
    lookup_cid     = pubchem_lookup[0].get('cid')
    lookup_formula = pubchem_lookup[1].get('formula')
    lookup_name    = pubchem_lookup[2].get('name')
    return chempy.Substance.from_formula(lookup_formula)

def balance_simple_equation(react, prod):
    react =  {'NH4ClO4', 'Al'}
    prod  =  {'Al2O3', 'HCl', 'H2O', 'N2'}
    reactants, products = chempy.balance_stoichiometry(react,prod)
    #pprint(dict(reac))
    #{'Al': 10, 'NH4ClO4': 6}
    #pprint(dict(prod))
    #{'Al2O3': 5, 'H2O': 9, 'HCl': 6, 'N2': 3}
    for fractions in map(mass_fractions, [reac, prod]):
        pprint({k: '{0:.3g} wt%'.format(v*100) for k, v in fractions.items()})
    pass

def pubchem_lookup_by_name_or_CID(compound_id:str or int):
    '''
    wakka wakka wakka
    '''
    return_relationships = list
    if isinstance(compound_id, str):
        lookup_results = pubchem.get_compounds(compound_id,'name',)
        if isinstance(lookup_results, list):
            for each in lookup_results:
                return_relationships.append([                      \
                    {'cid'     : each.cid                        },\
                    {'formula' : each.molecular_formula          },\
                    {'name'    : each.iupac_name                 }])
        #TODO: fix this shit to make the above format
        else:
            return_relationships.append([                          \
                    {'cid'     : lookup_results.cid              },\
                    {'formula' : lookup_results.molecular_formula},\
                    {'name'    : lookup_results.iupac_name       }])

        return return_relationships
    elif isinstance(compound_id, int):
        lookup_results = pubchem.Compound.from_cid(compound_id)
        return_relationships.append([                            \
            {'cid'     : lookup_results.cid}                    ,\
            {'formula' : lookup_results.molecular_formula}      ,\
            {'name'    : lookup_results.iupac_name}             ])
        return return_relationships
##############################################################################

    def validate_user_input(user_input: str):
        # haha I made a joke!
        # this function is going to be fucking complicated and I am not
        # looking forward to it! PLEASE HELP!
        lambda hard = True : hard ; pass  
##############################################################################

    async def send_reply(self, ctx, formatted_reply):
        await message.edit(content="lol", embed=formatted_reply)
##############################################################################

    
    async def format_message(self, ctx, lookup_results_object):
        formatted_message = discord.Embed( \
            title=lookup_results_object.synonyms[0],
            #change color option
            colour=discord.Colour(discord_color),  \
            url="",
            description=size_check_256(lookup_results_object.iupac_name),
            timestamp=datetime.datetime.utcfromtimestamp(1580842764))
        #formatted_message.set_image(url="https://cdn.discordapp.com/embed/avatars/0.png")
        formatted_message.set_thumbnail(    \
            url="https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{}" + \
                "/PNG?record_type=3d&image_size=small" + \
                "".format(lookup_results_object.cid))
        formatted_message.set_author(
            name="{1} ({2})".format(lookup_results_object.name,\
                                    lookup_results_object.cid),\
            url=f"https://pubchem.ncbi.nlm.nih.gov/compound/{}" + \
                "".format(lookup_results_object.cid), 
            icon_url="https://pubchem.ncbi.nlm.nih.gov/pcfe/logo/" + \
                "PubChem_logo_splash.png")
        formatted_message.add_field(
            name="Molecular Formula",
            value=lookup_results_object.molecular_formula)
        formatted_message.add_field(
            name="Molecular Weight",
            value=lookup_results_object.molecular_weight)
        formatted_message.add_field(
            name="Charge",
            value=lookup_results_object.charge)
        formatted_message.set_footer(
            text="",
            icon_url="")
##############################################################################

    @commands.command()
    async def pubsearch(self, ctx, arg1, arg2, arg3):
        user_input = self.validate_user_input( arg1, arg2, arg3 )
        lookup = self.pubchem_lookup_by_name_or_CID(user_input)