import requests

url = "https://www.solocastings.es/casting/37225/actor-18-40-anos-alto-y-muy-musculado-at-isa-moran/"

html = requests.get(
    url,
    headers={"User-Agent": "Mozilla/5.0"}
).text

with open("detalle.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Detalle guardado.")