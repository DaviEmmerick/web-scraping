import requests
from bs4 import BeautifulSoup
import sqlite3
import os
from flask import Flask, render_template, request

app = Flask(__name__)

DB_PATH = "/app/data/news.db"

TIMES = {
    "Flamengo": "flamengo",
    "Vasco": "vasco",
    "Botafogo": "botafogo",
    "Fluminense": "fluminense",
    "Palmeiras": "palmeiras",
    "Corinthians": "corinthians",
    "São Paulo": "sao-paulo",
    "Santos": "santos",
    "Grêmio": "gremio",
    "Internacional": "internacional",
    "Atlético-MG": "atletico-mg",
    "Cruzeiro": "cruzeiro"
}

def fetch_news_by_team(team_slug):
    url = f'https://ge.globo.com/futebol/times/{team_slug}/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    headlines = soup.find_all('a', class_='feed-post-link')

    os.makedirs("/app/data", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS news (title TEXT, link TEXT)')
    c.execute('DELETE FROM news')

    for h in headlines:
        if 'href' in h.attrs:
            title = h.get_text(strip=True)
            link = h['href']
            c.execute('INSERT INTO news (title, link) VALUES (?, ?)', (title, link))

    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def index():
    noticias = []
    time_selecionado = ""

    if request.method == "POST":
        time_selecionado = request.form.get("time")
        if time_selecionado in TIMES.values():
            fetch_news_by_team(time_selecionado)

            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("SELECT title, link FROM news")
            noticias = c.fetchall()
            conn.close()

    return render_template("index.html", noticias=noticias, time_selecionado=time_selecionado, times=TIMES)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)