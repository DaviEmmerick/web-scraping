import requests
from bs4 import BeautifulSoup
import sqlite3
import os

def fetch_news():
    url = 'https://g1.globo.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    headlines = soup.find_all('a', class_='feed-post-link')

    db_folder = "/app/data"  
    os.makedirs(db_folder, exist_ok=True)  
    db_path = os.path.join(db_folder, "news.db") 

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS news (title TEXT, link TEXT)')

    for h in headlines:
        title = h.get_text(strip=True)
        link = h['href']
        c.execute('INSERT INTO news (title, link) VALUES (?, ?)', (title, link))

    conn.commit()
    conn.close()
    print(f"{len(headlines)} notícias salvas com sucesso em {db_path}")

if __name__ == "__main__":
    fetch_news()