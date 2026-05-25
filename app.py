from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from collections import Counter
import os
import psycopg2
from psycopg2 import sql

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-prod')

ANCHOR_ADDRESS = 'https://ontheworldmap.com/countries/by-continents/#'
NAT_GEO_ADDRESS = 'https://education.nationalgeographic.org/resource/Continent/'
CONTINENTS_LIST = [
    'asia', 'europe', 'africa', 'north america',
    'south america', 'australia', 'oceania',
    'australia and oceania', 'antartica', 'antarctica'
]

ANTARCTICA_LETTER = 'a'
ANTARCTICA_COUNT = 4


def get_db():
    url = os.environ.get('NEON_DATABASE_URL')
    if not url:
        return None
    try:
        conn = psycopg2.connect(url)
        return conn
    except Exception:
        return None


def init_db():
    conn = get_db()
    if not conn:
        return
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS stats (
                    id SERIAL PRIMARY KEY,
                    total_searches INTEGER DEFAULT 0
                );

                INSERT INTO stats (id, total_searches)
                SELECT 1, 0
                WHERE NOT EXISTS (
                    SELECT 1 FROM stats WHERE id = 1
                );
            """)
            conn.commit()
    except Exception:
        pass
    finally:
        conn.close()


def get_search_count():
    conn = get_db()
    if not conn:
        return 0

    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT total_searches
                FROM stats
                WHERE id = 1;
            """)
            row = cur.fetchone()
            return row[0] if row else 0
    except Exception:
        return 0
    finally:
        conn.close()


def increment_search_count():
    conn = get_db()
    if not conn:
        return

    try:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE stats
                SET total_searches = total_searches + 1
                WHERE id = 1;
            """)
            conn.commit()
    except Exception:
        pass
    finally:
        conn.close()


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

    if normalized == 'antarctica':
        return ANTARCTICA_LETTER, ANTARCTICA_COUNT, ['Antarctica'], None

    if normalized == 'australia':
        normalized = 'oceania'

    if normalized not in CONTINENTS_LIST:
        return (
            None,
            None,
            None,
            "Invalid continent. Please enter one of: "
            "Africa, Asia, Europe, North America, "
            "South America, Australia, Oceania, Antarctica."
        )

    headers = get_browser_headers()
    web_address = ANCHOR_ADDRESS + normalized.replace(' ', '-')

    res = requests.get(web_address, headers=headers, timeout=15)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, 'lxml')

    countries_section = soup.find('section', class_='countries')

    continent_heading = (
        countries_section.find('h2', string=normalized.title())
        if countries_section
        else soup.find('h2', string=normalized.title())
    )

    if not continent_heading:
        return (
            None,
            None,
            None,
            "Could not find continent data on the source page. Try again."
        )

    countries = []

    for sibling in continent_heading.next_siblings:
        if sibling.name == 'h2':
            break

        if sibling.name == 'div':
            for ul in sibling.find_all('ul', class_='ul-reset'):
                for li in ul.find_all('li'):
                    anchor = li.find('a')

                    if anchor:
                        countries.append(anchor.get_text())

    if not countries:
        return None, None, None, "No countries found for that continent."

    joined = "".join(c.replace(" ", "") for c in countries).lower()

    count = Counter(joined)

    top_letter, top_count = count.most_common(1)[0]

    return top_letter, top_count, countries, None


@app.route('/count', methods=['POST'])
def count():
    increment_search_count()
    return jsonify({'ok': True})


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None
    continent = ''
    countries = []

    search_count = get_search_count()

    if request.method == 'POST':
        continent = request.form.get('continent', '').strip()

        if continent:
            top_letter, top_count, countries, error = get_top_letter(continent)

            if not error:
                search_count = get_search_count()

                result = {
                    'letter': top_letter,
                    'count': top_count,
                    'continent': continent.title(),
                    'nat_geo_url': NAT_GEO_ADDRESS,
                }

    return render_template(
        'index.html',
        result=result,
        error=error,
        continent=continent,
        countries=countries,
        search_count=search_count
    )


init_db()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
