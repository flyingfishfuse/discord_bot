import math, cmath
from ionize import *
from pprint import pprint
import chempy
from chempy import *
import pubchempy as pubchem

def parse_lookup_to_chempy(pubchem_lookup : list):
    '''
    creates a chempy something or other based on what you feed it
    like cookie monster
    '''
    lookup_cid     = pubchem_lookup[0].get('cid')
    lookup_formula = pubchem_lookup[1].get('formula')
    lookup_name    = pubchem_lookup[2].get('name')
    return chempy.Substance.from_formula(lookup_formula)

react =  {'NH4ClO4', 'Al'}
prod  =  {'Al2O3', 'HCl', 'H2O', 'N2'}
#user input 
user_input_reactants = "NH4ClO4,Al"
user_input_products = "Al2O3,HCl,H2O,N2"
#example from docs

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

