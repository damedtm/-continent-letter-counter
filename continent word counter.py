#Program to calculate the most recurring word in the countries of a continent.
#url: https://ontheworldmap.com/countries/by-continents/#

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
anchorAddress = 'https://ontheworldmap.com/countries/by-continents/#'


'''continentsDict = {'Asia' : 'as', 'Europe' : 'eu', 'Africa' : 'af', 'Oceania' : 'au', 'South America' : 'sa',
                  'North America' : 'na', 'Antartica' : 'an'}'''

continentsList =[ 'asia', 'europe', 'africa', 'north america',  
                  'south america', 'australia', 'oceania',  
                  'australia and oceania', 'antartica']
alphabetsList = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 
                 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 
                 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
countriesList = []
normalizedCountriesList =[]
userContinent = []

print('Enter any continent to find out the most recurring letter in its names of its countries')
userContinent.append(input())
if userContinent[0] == 'australia':
        userContinent[0] = 'oceania'

normalizedUserContinent = userContinent[0].lower()

if (len(userContinent[0]) > 1) and userContinent[0] in continentsList:

    headers = get_browser_headers()
    webAddress = anchorAddress + normalizedUserContinent[0].replace(' ', '-') 
    res = requests.get(webAddress, headers = headers)
    res.raise_for_status()
    print(res.status_code)
    soup = BeautifulSoup(res.content, 'lxml')
   
    header = soup.find('h2', string=userContinent[0].title())
    countries = []
    for sibling in header.find_all_next():
        if sibling.name == 'h2':
            break
        if sibling.name == 'ul' and 'ul-reset' in sibling.get('class', []):
            for li in sibling.find_all('li'):
                countries.append(li.get_text())

    print(countries)

else:
    print('Program failed')



