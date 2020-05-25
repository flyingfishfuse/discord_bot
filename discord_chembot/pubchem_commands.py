import discord
from ionize import *
import pubchempy as pubchem
from discord.ext import commands

def size_check_256(txt):
    if txt is None:
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
        print("loaded pubchem_commands")
    
    def pubchem_lookup_by_name_or_CID(compound_id:str or int):
        '''
        expecting either an IUPAC chemical name or integer
        '''
        from variables_for_reality import compound_name_formula_cache
        if isinstance(compound_id, str):
            name_lookup_results_list = pubchem.get_compounds(compound_id,\
                                        'name' , \
                                        list_return='flat')
            result_1 = name_lookup_results_list[0]
            #result_2 = name_lookup_results_list[1]
            #result_3 = name_lookup_results_list[2]

        elif isinstance(compound_id, int):
            name_lookup_result = pubchem.Compound.from_cid(compound_id)
            # so now we have stuff.
    def validate_user_input(user_input: str):
        escape_mentions = lambda user_inputs: discord.utils.escape_mentions(user_inputs)

    @commands.command()
    async def search(self, ctx, arg1, arg2, arg3):
        #this is how you use an escape function
        self.pubchem_lookup_by_name_or_CID()
        if len(cidsRes) >= 25:
            await message.edit(content=f"cannot process results. \
                Be more specific with your search !")
            return
        results =[pcp.Compound.from_cid(cid) for cid in cidsRes]
        if len(results) >= 9:
            await message.edit(content=f"Your result is >9 ({len(results)}), trimming...")
            results = results[:9]
        else:
            if len(results) >= 25:
                pass
            await message.edit(content=f"Processing your {len(results)} results...")
        #results = pcp.get_compounds(cmp, 'name')
 
        # ! if there are no results, print text below
        if not results: 
            await message.edit(content=f"0 results for {cmp} 😟")
            return

        # ! makes one big string, if there are too many results say that aswell
        results_str = ""
        results_ammount = 0
        for i in results:
            results_ammount += 1
            name = "Synonym not found"
            if len(i.synonyms) is not 0:
                name = i.synonyms[0]

            results_str = results_str + f"{discord_numbers.get(results_ammount)} {name} \n"
            # print(i)
        # print(results_str)

        if len(results_str) >= 1900:
            await message.edit(content="Can't show the list, it's bigger than 1900 characters !")
            return

        # print(results)
        # await message.edit(content="newcontent")

        # ! edit the message and show results
        await message.edit(content=results_str)

            # ! gives 3d shit
            # ! gives 3d shit
            # ! gives 3d shit
            # cmpdataz = pcp.get_compounds('Aspirin', 'name', record_type='3d')

        
            selected_cmp_name = "Synonym not found"
            if len(selected_cmp.synonyms) is not 0:
                selected_cmp_name = selected_cmp.synonyms[0]

            embed = discord.Embed(
            # title=selected_cmp.synonyms[0],
            colour=discord.Colour(0x3b12ef),
            # url="https://discordapp.com/",
            description=size_check_256(selected_cmp.iupac_name),
            # timestamp=datetime.datetime.utcfromtimestamp(1580842764) # or any other datetime type format.
            )
            # ! embed.set_image(url="https://cdn.discordapp.com/embed/avatars/0.png")
            embed.set_thumbnail(url=f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{selected_cmp.cid}/PNG?record_type=3d&image_size=small")
            embed.set_author(
                name=f"{selected_cmp_name} ({selected_cmp.cid})",
                url=f"https://pubchem.ncbi.nlm.nih.gov/compound/{selected_cmp.cid}", 
                icon_url="https://pubchem.ncbi.nlm.nih.gov/pcfe/logo/PubChem_logo_splash.png"
                )
            embed.set_footer(
                text="Made by this will be a list",
                icon_url="http://media.thechemicalworkshop.com/TCW/logo_main/TCW_logo_space_alpha_mid_q_864x864.png"
                )

            embed.add_field(
                name="Molecular Formula",
                value=selected_cmp.molecular_formula
                )
            embed.add_field(
                name="Molecular Weight",
                value=selected_cmp.molecular_weight
                )
            embed.add_field(
                name="Charge",
                value=selected_cmp.charge
                )
            # embed.add_field(
            #     name="another field title",
            #     value="try exceeding some of them! (coz idk them)"
            #     )
            # embed.add_field(
            #     name=":thinking: this supports emotes! (and custom ones too)",
            #     value="if you exceed them, the error will tell you which value exceeds it."
            #     )

            # embed.add_field(
            #     name="Inline",
            #     value="these last two fields",
            #     inline=True
            #     )
            # embed.add_field(
            #     name="Fields",
            #     value="are inline fields",
            #     inline=True
            #     )

            await message.edit(content="", embed=embed)
            # await message.channel.send(
            #     # content="This is a normal message to be sent alongside the embed",
            #     embed=embed
            #     )









        

def setup(bot):
    bot.add_cog(pubchem_commands(bot))
