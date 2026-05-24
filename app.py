from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from collections import Counter

app = Flask(__name__)

ANCHOR_ADDRESS = 'https://ontheworldmap.com/countries/by-continents/#'
NAT_GEO_ADDRESS = 'https://education.nationalgeographic.org/resource/Continent/'
CONTINENTS_LIST = [
    'asia', 'europe', 'africa', 'north america',
    'south america', 'australia', 'oceania',
    'australia and oceania', 'antartica'
]


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


def get_top_letter(continent):
    normalized = continent.strip().lower()
    if normalized == 'australia':
        normalized = 'oceania'

    if normalized not in CONTINENTS_LIST:
        return None, None, None, "Invalid continent. Please enter one of: Africa, Asia, Europe, North America, South America, Australia, Oceania, Antarctica."

    headers = get_browser_headers()
    web_address = ANCHOR_ADDRESS + normalized.replace(' ', '-')
    res = requests.get(web_address, headers=headers, timeout=15)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, 'lxml')
    continent_heading = soup.find('h2', string=normalized.title())
    if not continent_heading:
        return None, None, None, "Could not find continent data on the source page. Try again."

    countries = []
    for sibling in continent_heading.find_all_next():
        if sibling.name == 'h2':
            break
        if sibling.name == 'ul' and 'ul-reset' in sibling.get('class', []):
            for li in sibling.find_all('li'):
                anchor = li.find('a')
                if anchor:
                    countries.append(anchor.get_text())

    if not countries:
        return None, None, None, "No countries found for that continent."

    joined = "".join(c.replace(" ", "") for c in countries).lower()
    count = Counter(joined)
    top_letter, top_count = count.most_common(1)[0]

    return top_letter, top_count, countries, None


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None
    continent = ''
    countries = []

    if request.method == 'POST':
        continent = request.form.get('continent', '').strip()
        if continent:
            top_letter, top_count, countries, error = get_top_letter(continent)
            if not error:
                result = {
                    'letter': top_letter,
                    'count': top_count,
                    'continent': continent.title(),
                    'nat_geo_url': NAT_GEO_ADDRESS,
                }

    return render_template('index.html', result=result, error=error, continent=continent, countries=countries)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
