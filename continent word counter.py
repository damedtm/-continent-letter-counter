#Program to calculate the most recurring letters in the countries of a continent.
#url: https://ontheworldmap.com/countries/by-continents/#

import webbrowser
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from collections import Counter

natGeoAddress = 'https://education.nationalgeographic.org/resource/Continent/'
anchorAddress = 'https://ontheworldmap.com/countries/by-continents/#'
continentsList =[ 'asia', 'europe', 'africa', 'north america',  
                  'south america', 'australia', 'oceania',  
                  'australia and oceania', 'antartica']
countriesListNormalized = []
countriesNormalizedandJoined =[]
countriesList = []

def get_browser_headers():
    ua = UserAgent()
    return {
        'User-Agent': ua.random,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'identity',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Cache-Control': 'max-age=0',
    }

print("Enter any continent to find out the most recurring letter in its names of its countries")
userContinent = input()
normalizedUserContinent = userContinent.lower()

if normalizedUserContinent == 'australia':
        normalizedUserContinent = 'oceania'

if  normalizedUserContinent in continentsList:
    headers = get_browser_headers()
    webAddress = anchorAddress + normalizedUserContinent.replace(' ', '-') 
    res = requests.get(webAddress, headers = headers)
    res.raise_for_status()
    print(res.status_code)
    soup = BeautifulSoup(res.text, 'lxml')
    
    continentHeading = soup.find('h2', string = normalizedUserContinent.title())
    for sibling in continentHeading.find_all_next():
        if sibling.name == 'h2':
            break
        if sibling.name == 'ul' and 'ul-reset' in sibling.get('class', []):
            for li in sibling.find_all('li'):
                countriesListNormalized.append(li.find('a').get_text().replace(" ",""))
                countriesList.append(li.find('a').get_text())
    
    countriesNormalizedandJoined = "".join(countriesListNormalized).lower()
    count = Counter(countriesNormalizedandJoined)
    letter = count.most_common(1)
    topLetter, topCount = count.most_common(1)[0]

    print(f"The most recurring letter in {normalizedUserContinent.title()} is '{topLetter}', occurring {topCount} times!")
    print(f"You can follow this link to view interesting facts about the Continents: {natGeoAddress}")

else:
    print(f"Invalid input detected, please enter a continent e.g. 'Africa'")



