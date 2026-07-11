import requests
from bs4 import BeautifulSoup

url = "https://clandestinocastings.com/castings/todos-los-anuncios"

response = requests.get(
    url,
    headers={"User-Agent": "Mozilla/5.0"},
    timeout=20,
)

soup = BeautifulSoup(response.text, "lxml")

anuncios = soup.select("div.listing-summary")

print("Anuncios encontrados:", len(anuncios))

for anuncio in anuncios[:5]:
    titulo = anuncio.select_one("h3.summary-title span")
    print("-", titulo.get_text(strip=True))