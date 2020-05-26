import discord
from ionize import *
import datetime
import pubchempy as pubchem
from discord.ext import commands
from discord_chembot.variables_for_reality import *
def size_check_256(txt):
    if txt == None:
        return "iupac name Not Found"
    # print(len(txt))
    if len(txt) < 255:
        return txt
    else:
        short = (str(txt[:100])+ " .....")
        return short

class pubchem_lookup(commands.Cog):

    def __init__(self):
        self.asdf = []
        self.name_lookup_result = None
        print("loaded pubchem_commands")
    
    def pubchem_lookup_by_name_or_CID(compound_id:str or int):
        '''
        expecting either an IUPAC chemical name or integer
        '''
        if isinstance(compound_id, str):
            name_lookup_results_list = pubchem.get_compounds(compound_id,\
                                        'name' , \
                                        list_return='flat')
            result_1 = name_lookup_results_list[0]
            #result_2 = name_lookup_results_list[1]
            #result_3 = name_lookup_results_list[2]

        elif isinstance(compound_id, int):
            self.name_lookup_result = pubchem.Compound.from_cid(compound_id)
            # so now we have stuff.

    def validate_user_input(user_input: str):
        #escape_mentions = lambda user_inputs: discord.utils.escape_mentions(user_inputs)
        pass

    async def send_reply(self, ctx, formatted_reply):
        await message.edit(content="lol", embed=formatted_reply)

    
    async def format_message(self, ctx, lookup_results_object):
        formatted_message = discord.Embed( \
            title=lookup_results_object.synonyms[0],
            #change color option
            colour=discord.Colour(discord_color),  \
            url="",
            description=size_check_256(lookup_results_object.iupac_name),
            timestamp=datetime.datetime.utcfromtimestamp(1580842764))
        #formatted_message.set_image(url="https://cdn.discordapp.com/embed/avatars/0.png")
        formatted_message.set_thumbnail(url="https://pubchem.ncbi.nlm.nih.gov/" + \
                "rest/pug/compound/cid/{1}/PNG?record_type=3d&image_size=small" + \
                "".format(lookup_results_object.cid))
        formatted_message.set_author(
            name="{1} ({2})".format(lookup_results_object.name, lookup_results_object.cid),
            url=f"https://pubchem.ncbi.nlm.nih.gov/compound/{lookup_results_object.cid}", 
            icon_url="https://pubchem.ncbi.nlm.nih.gov/pcfe/logo/PubChem_logo_splash.png"
            )
        formatted_message.add_field(
            name="Molecular Formula",
            value=lookup_results_object.molecular_formula
            )
        formatted_message.add_field(
            name="Molecular Weight",
            value=lookup_results_object.molecular_weight
            )
        formatted_message.add_field(
            name="Charge",
            value=lookup_results_object.charge
            )
        formatted_message.set_footer(
            text="",
            icon_url=""
            )

    @commands.command()
    async def search(self, ctx, arg1, arg2, arg3):
        #this is how you use an escape function
        user_input = self.validate_user_input( arg1, arg2, arg3 )
        lookup = self.pubchem_lookup_by_name_or_CID(user_input)
        #if len(lookup) >= 25:
        #    await message.edit(content="")
        #    return
        results =[pubchem.Compound.from_cid(cid) for cid in cidsRes]
        if len(results) >= 9:
            await message.edit(content=f"Your result is >9 ({len(results)}), trimming...")
            results = results[:9]
        else:
            if len(results) >= 25:
                pass
            await message.edit(content=f"Processing your {len(results)} results...")
        #results = pcp.get_compounds(cmp, 'name')
 
        #if there are no results, print text below
        if not results: 
            await message.edit(content=f"0 results for {cmp}")
            return

        #makes one big string, if there are too many results say that aswell
        results_str = ""
        results_ammount = 0
        for i in results:
            results_ammount += 1
            name = "Synonym not found"
            if len(i.synonyms) > 0:
                name = i.synonyms[0]
            results_str = results_str + f"{discord_numbers.get(results_ammount)} {name} \n"
            if len(results_str) >= 1900:
                await message.edit(content="Cannot show list, reply longer than 1900 characters")
            return
        # edit the message and show results
        await message.edit(content=results_str)
            # cmpdataz = pcp.get_compounds(record_type='3d')
            lookup_results_name = "Synonym not found"
            if len(lookup_results_object.synonyms) > 0 :
                lookup_results_name = .synonyms[0]



