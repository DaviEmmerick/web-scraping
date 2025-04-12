import requests
from bs4 import BeautifulSoup
import sqlite3
import os
from flask import Flask, render_template_string, request

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

    time_selecionado = "flamengo"
    if request.method == "POST":
        time_selecionado = request.form.get("time", "flamengo")

    if time_selecionado in TIMES.values():
        fetch_news_by_team(time_selecionado)

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT title, link FROM news")
        noticias = c.fetchall()
        conn.close()

    html = """
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <title>Notícias de Futebol</title>
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
        <style>
            body {
                font-family: 'Roboto', sans-serif;
                padding: 40px;
                background: linear-gradient(to right, #ffe6e6, #ffffff);
                color: #333;
                text-align: center;
            }
            h1 {
                color: #b30000;
                margin-bottom: 20px;
            }
            form {
                margin-bottom: 40px;
            }
            select, button {
                font-size: 18px;
                padding: 10px;
                margin-top: 10px;
                border-radius: 8px;
                border: 1px solid #ccc;
            }
            ul {
                list-style-type: none;
                padding: 0;
                max-width: 800px;
                margin: auto;
            }
            li {
                background-color: #fff;
                margin-bottom: 20px;
                padding: 20px;
                border-radius: 12px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                transition: transform 0.2s, box-shadow 0.2s;
            }
            li:hover {
                transform: scale(1.02);
                box-shadow: 0 6px 16px rgba(0,0,0,0.15);
            }
            a {
                text-decoration: none;
                color: #b30000;
                font-size: 18px;
                font-weight: bold;
            }
            a:hover {
                color: #e60000;
            }
        </style>
    </head>
    <body>
        <h1>📰 Veja as últimas notícias do seu time</h1>
        <form method="post">
            <label for="time" style="font-size: 20px; font-weight: bold;">Escolha seu time:</label><br>
            <div style="margin-top: 10px;">
                <select name="time" id="time" style="
                    font-size: 18px;
                    padding: 12px 16px;
                    border-radius: 10px;
                    border: 1px solid #ccc;
                    background-color: #fff;
                    color: #333;
                    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
                    transition: all 0.3s ease;
                ">
                    {% for nome, slug in times.items() %}
                        <option value="{{ slug }}" {% if time_selecionado == slug %}selected{% endif %}>{{ nome }}</option>
                    {% endfor %}
                </select>
                <button type="submit" style="
                    font-size: 18px;
                    padding: 12px 24px;
                    margin-left: 10px;
                    background-color: #b30000;
                    color: white;
                    border: none;
                    border-radius: 10px;
                    cursor: pointer;
                    transition: background-color 0.3s ease;
                " onmouseover="this.style.backgroundColor='#e60000'" onmouseout="this.style.backgroundColor='#b30000'">
                    Ver Notícias
                </button>
            </div>
        </form>

        {% if noticias %}
        <h2>Últimas notícias do {{ time_selecionado.replace("-", " ").title() }}</h2>
        <ul>
            {% for title, link in noticias %}
            <li><a href="{{ link }}" target="_blank">{{ title }}</a></li>
            {% endfor %}
        </ul>
        {% endif %}
    </body>
    </html>
    """

    return render_template_string(html, noticias=noticias, time_selecionado=time_selecionado, times=TIMES)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)