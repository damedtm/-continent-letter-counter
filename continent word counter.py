#Program to calculate the most recurring letters in the countries of a continent.
#url: https://ontheworldmap.com/countries/by-continents/#

import sys
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
antarcticaLetterCount = 'A'
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
if normalizedUserContinent == 'antarctica':
    print(f"The most recurring letter in {normalizedUserContinent.title()} is '{antarcticaLetterCount}', occurring 4 times!")
    print(f"You can follow this link to view interesting facts about the Continents: {natGeoAddress}")
    sys.exit()

        

if normalizedUserContinent == 'australia':
        normalizedUserContinent = 'oceania'

if  normalizedUserContinent in continentsList:
    headers = get_browser_headers()
    webAddress = anchorAddress + normalizedUserContinent.replace(' ', '-') 
    res = requests.get(webAddress, headers = headers)
    res.raise_for_status()
    print(res.status_code)
    soup = BeautifulSoup(res.text, 'lxml')
    

    countries_section = soup.find('section', class_='countries')
    continentHeading = countries_section.find('h2', string=normalizedUserContinent.title())

    for sibling in continentHeading.next_siblings:
        if sibling.name == 'h2':
            break
        if sibling.name == 'div':
            for ul in sibling.find_all('ul', class_='ul-reset'):
                for li in ul.find_all('li'):
                    a = li.find('a')
                    if a:
                        countriesListNormalized.append(a.get_text().replace(" ", ""))
                        countriesList.append(a.get_text())

    countriesNormalizedandJoined = "".join(countriesListNormalized)
    count = Counter(countriesNormalizedandJoined)
    letter = count.most_common(1)
    topLetter, topCount = count.most_common(1)[0]
    total = 0

    print(f"The most recurring letter in {normalizedUserContinent.title()} is '{topLetter.title()}', occurring {topCount} times!\n")
    print(f"You can follow this link to view interesting facts about the Continents: {natGeoAddress}\n")
    for i in countriesList:
        total = total + 1
    
    print(f"Here are the {total} countries included:")
    for i in countriesList:
        print (f"    {i}")

else:
    print(f"Invalid input detected, please enter a continent e.g. 'Africa'")



