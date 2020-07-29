import lxml
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.chrome.options import Options

import platform
OS_NAME = platform.system()

class SoupyWebGetter():
    '''
    Grabs shit from http with bs4/selenium and requests using lxml parser
    '''
    def __init__(self, validated_user_input, container_name = "section_content_id"):
        self.nix_browser_binary_location	     = './bin/chrome_selenium'
        self.win_browser_binary_location    	 = './chromium-browser'
        self.useragent                           = {'User-Agent' : 'Mozilla/5.0 \
            (X11; Linux x86_64; rv:28.0) Gecko/20100101  Firefox/28.0'}
        self.search_url         = "https://pubchem.ncbi.nlm.nih.gov/compound/" +\
            validated_user_input
        self.container_name     = container_name
        self.request_return     = requests.get(self.search_url)
        self.soupyresults       = BeautifulSoup(self.request_return.content , 'lxml')
        self.divs               = self.soupyresults.find(lambda tag:  tag.name =='div' \
                                  and tag.has_key('class') and tag['class'] == self.container_name)

        def selenium_open_browser(url_to_open:str):
            chromeoptions = Options()
            chromeoptions.binary_location = win_browser_binary_location
            headless_browser = webdriver.Chrome(chrome_options=chromeoptions)
            headless_browser.get(wiki_location))

SoupyDescriptionGetter("2519")