# Continent Letter Counter

This project started from a simple question I had wondered about for a while:

> What is the most recurring letter across the country names of a continent?

To answer it, I built a Flask web application that scrapes live geography data in real time instead of relying on a static database.

---

## What I Learned

This project helped strengthen my understanding of:

- Web scraping
- HTTP request headers
- HTML parsing
- Python modules and abstraction
- Backend deployment and database integration

Some of the challenges I ran into included:

- My automated requests getting blocked by the source website. Working around this taught me a lot about request headers and how websites detect automated traffic.

- The site returning compressed HTML that interfered with parsing, which led me to force `Accept-Encoding: identity` in my request headers.

- Writing parsing logic capable of efficiently locating and extracting the exact section of HTML I needed.

---

## Technologies Used

- Python
- Flask
- BeautifulSoup
- lxml
- Neon PostgreSQL
- Docker
- Hugging Face Spaces

I used `BeautifulSoup` with the `lxml` parser to extract country data from the source website. I then used Python’s `Counter` collection to determine the most recurring letter across the parsed country names.

---

## Features

- Live scraping on every search
- Visitor counter backed by Neon PostgreSQL
- Animated count-up interaction
- Pulsing live activity indicator
- Responsive UI with custom copy and styling

---

## Deployment

The application is deployed on Hugging Face Spaces using Docker.

Development was primarily done in VS Code and Replit, which handled deployment configuration, environment secrets, and database integration.

---

## Live Demo

Try it here:

https://huggingface.co/spaces/damianohajunwa/continent-word-counter
