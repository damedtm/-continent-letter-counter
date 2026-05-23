#Program to calculate the most recurring word in the countries of a continent.
#url: https://www.countries-ofthe-world.com/

import webbrowser
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

def get_browser_headers():
    ua = UserAgent()
    return {
        'User-Agent': ua.random,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Cache-Control': 'max-age=0',
    }
anchorAddress = 'https://www.countries-ofthe-world.com/countries-of-'
tailAddress = '.html'

continentsList =[ 'asia', 'europe', 'africa', 'north america',  
                 'south america', 'australia', 'oceania',  
                 'australia and oceania']
alphabetsList = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 
                 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
countriesList = []
normalizedCountriesList = []
emptyContainer = 0

print('Enter any continent to find out the most recurring letter in its names of its countries')
userContinent = input()
normalizedContinent = userContinent.lower()
urlHalfList = [normalizedContinent, tailAddress]

if (len(normalizedContinent) > 1) and normalizedContinent in continentsList:  
    headers = get_browser_headers()

    webAddress = anchorAddress + ''. join(urlHalfList)
    res = requests.get(webAddress, headers = headers)
    print(res.status_code)
    soup = BeautifulSoup(res.text, 'lxml')




