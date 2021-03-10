from bs4 import BeautifulSoup
import requests
import os
import pandas
from std_imports import greenprint,redprint,blueprint

fulltable = {}
sections_to_grab = ['Vegetables', 'Fruit', 'Herbs', 'Flowers', 'Other']
thing_to_get = 'https://en.wikipedia.org/wiki/List_of_companion_plants'
wikipage1 = requests.get(thing_to_get)

class ScrapeWikipediaTableForData:
    def __init__(self,url):
        self.dataframes  = pandas.read_html(url)
        self.full_entry  = {}
        for dataframe in self.dataframes:
            self.full_entry.update({:dataframe.to_sql})




tables_of_plant_data = ScrapeWikipediaTableForData(thing_to_get)
