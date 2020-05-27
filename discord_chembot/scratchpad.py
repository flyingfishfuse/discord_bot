import math, cmath
from ionize import *
from pprint import pprint
import chempy
from chempy import *
import pubchempy as pubchem
import discord_chembot.database_setup
from discord_chembot.database_setup import *
from discord_chembot.variables_for_reality import *
################################################################################

def Compound_by_id(cid_of_compound):
    """
    Returns a compound from the local DB
    """
    return Compound.query.all.filter_by(id = cid_of_compound).first()
################################################################################

def add_to_db(thingie):
    """
    Takes SQLAchemy Class_model Objects 
    For updating changes to Class_model.Attribute using the form:
    Class_model.Attribute = some_var 
    """
    database.session.add(thingie)
    database.session.commit
################################################################################

def update_db():
    """
    DUH
    """
    database.session.commit()

################################################################################

def parse_lookup_to_chempy(pubchem_lookup : list):
    '''
    creates a chempy something or other based on what you feed it
    like cookie monster
    '''
    lookup_cid       = pubchem_lookup[0].get('cid')
    lookup_formula   = pubchem_lookup[1].get('formula')
    lookup_name      = pubchem_lookup[2].get('name')
    return chempy.Substance.from_formula(lookup_formula)
################################################################################

def compound_to_database(lookup_list: list):
    """
    Puts a pubchem lookup to the database
    """
    lookup_cid       = lookup_list[0].get('cid')
    lookup_formula   = lookup_list[1].get('formula')
    lookup_name      = lookup_list[2].get('name')
    add_to_db(Compound(cid     = lookup_cid,      \
                       formula = lookup_formula,  \
                       name = lookup_name         ))

def composition_to_database(comp_name: str, units_used :str, \
                            formula_list : list , info : str):
    """
    The composition is a relation between multiple Compounds
    Each Composition entry will have required a pubchem_lookup on each
    Compound in the Formula field. 
    the formula is a CSV LIST WHERE: 
     ...str_compound,int_amount,.. REPEATING (floats allowed)

    """
    new_comp = Composition(name       = comp_name,               \
                           units      = units_used,              \
                           compounds  = formula_list,            \
                           notes      = info                     )
    add_to_db(new_comp)

################################################################################

def local_database_lookup(cid_or_formula : str):
    # CID spec says 10-char max? Is that right?
    if cid_or_formula.isnumeric() and  0 < len(cid_or_formula) > 10 :
        database.Query(cid_or_formula).all().first()
################################################################################

#example from docs
################################################################################

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
    reactants, products = chempy.balance_stoichiometry(react,prod)
    #pprint(dict(reac))
    #{'Al': 10, 'NH4ClO4': 6}
    #pprint(dict(prod))
    #{'Al2O3': 5, 'H2O': 9, 'HCl': 6, 'N2': 3}
    for fractions in map(mass_fractions, [react, prod]):
        pprint({k: '{0:.3g} wt%'.format(v*100) for k, v in fractions.items()})
    pprint([dict(_) for _ in balance_stoichiometry({'C', 'O2'}, {'CO2', 'CO'})])  # doctest: +SKIP
    #[{'C': x1 + 2, 'O2': x1 + 1}, {'CO': 2, 'CO2': x1}]

react =  {'NH4ClO4', 'Al'}
prod  =  {'Al2O3', 'HCl', 'H2O', 'N2'}
#user input 
user_input_reactants = "NH4ClO4,Al"
user_input_products  = "Al2O3,HCl,H2O,N2"

for each in user_input_reactants:
    local_db_query = local_database_lookup(each, "formula")
    if local_db_query == True:
        return local_db_query
    elif local_db_query ==False:
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

