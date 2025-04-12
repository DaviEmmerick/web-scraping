FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN ls -la /app

RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["python", "scraper.py"]