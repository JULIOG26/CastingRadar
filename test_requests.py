import requests

url = "https://www.solocastings.es/castings/"

response = requests.get(
    url,
    headers={"User-Agent": "Mozilla/5.0"},
    timeout=20
)

with open("pagina.html", "w", encoding="utf-8") as f:
    f.write(response.text)

print("HTML guardado correctamente.")