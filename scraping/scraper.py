import requests
from bs4 import BeautifulSoup
import sqlite3
import os
from flask import Flask, render_template_string

app = Flask(__name__)

DB_PATH = "/app/data/news.db"

def fetch_news():
    url = 'https://g1.globo.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    headlines = soup.find_all('a', class_='feed-post-link')

    os.makedirs("/app/data", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS news (title TEXT, link TEXT)')
    c.execute('DELETE FROM news')  # limpa os dados antigos

    for h in headlines:
        title = h.get_text(strip=True)
        link = h['href']
        c.execute('INSERT INTO news (title, link) VALUES (?, ?)', (title, link))

    conn.commit()
    conn.close()
    print(f"{len(headlines)} notícias salvas com sucesso!")

# roda o scraping ao iniciar
fetch_news()

@app.route("/")
def index():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT title, link FROM news")
    noticias = c.fetchall()
    conn.close()

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Notícias do G1</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; background-color: #f5f5f5; }
            h1 { color: #d80000; }
            ul { list-style-type: none; padding: 0; }
            li { margin-bottom: 10px; }
            a { text-decoration: none; color: #0044cc; }
        </style>
    </head>
    <body>
        <h1>📰 Últimas Notícias do G1</h1>
        <ul>
            {% for title, link in noticias %}
            <li><a href="{{ link }}" target="_blank">{{ title }}</a></li>
            {% endfor %}
        </ul>
    </body>
    </html>
    """
    return render_template_string(html, noticias=noticias)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)