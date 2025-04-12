# 📌 Web Scraping com Python

Este projeto é um scraper em Python que coleta notícias do site G1 Globo e armazena os dados extraídos em um banco de dados SQLite. O script utiliza a biblioteca BeautifulSoup para fazer o parsing do HTML da página, a biblioteca requests para realizar as requisições HTTP e sqlite3 para interagir com o banco de dados local.

O scraper extrai os seguintes dados das notícias:

Título: O título da notícia.

Link: O URL da notícia.

Esses dados são então salvos em um banco de dados SQLite, armazenado no diretório /app/data dentro do contêiner Docker.

# 🛠️ Funcionalidades

• Extração de notícias: O scraper coleta os links e títulos das notícias mais recentes do site G1.

• Armazenamento em banco de dados SQLite: Os dados são armazenados em uma tabela chamada news dentro do banco de dados news.db.

• Ambiente Dockerizado: O projeto está configurado para rodar em um contêiner Docker, com volumes que permitem persistência dos dados no host.

# ✏️ Tecnologias Utilizadas

• Python: Linguagem principal do projeto.

• Requests: Para realizar as requisições HTTP.

• BeautifulSoup: Para fazer o parsing do HTML e extrair os dados.

• SQLite: Para armazenar os dados extraídos.

• Docker: Para facilitar a execução do projeto em um ambiente isolado.

## 🚀 Como Rodar o Projeto

1️⃣ Clone o repositório:

```bash
git clone <URL_DO_REPOSITORIO>
cd <DIRETORIO_DO_REPOSITORIO>
```

2️⃣ Construa e execute o contêiner Docker:

```bash

docker-compose up --build
```
3️⃣ O scraper irá rodar automaticamente e armazenar os dados em /app/data/news.db dentro do contêiner.

# Estrutura do Projeto

• scraping/: Contém o código do scraper.

• data/: Pasta onde o banco de dados news.db será armazenado.

• docker-compose.yml: Configuração do Docker Compose para rodar o contêiner.

• scraper.py: Script principal que executa o scraping e salva as notícias no banco de dados.

# ✨ Implementações Futuras

-> Provavelmente eu vou tentar automatizar esse processe de alguma forma diferente, talvez com Prefect ou Airflow. 
-> Caso eu faça isso, vou migrar o banco de dados para o PostgreSQL.

# 📄 Liçenca

Este projeto está sob a licença MIT. Consulte o arquivo LICENSE para mais detalhes.