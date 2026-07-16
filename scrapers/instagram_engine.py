from pathlib import Path
import csv

from scrapers.browser import Browser
from scrapers.post_extractor import PostExtractor


class InstagramEngine:

    def scrape(self):

        fichero = Path("data/instagram_accounts.csv")

        with open(fichero, newline="", encoding="utf-8") as f:
            cuentas = list(csv.DictReader(f))

        navegador = Browser()

        navegador.start()

        print(f"{len(cuentas)} cuentas cargadas")

        usuario = cuentas[0]["usuario"]

        print(f"Abriendo {usuario}")

        navegador.page.goto(
            f"https://www.instagram.com/{usuario}/"
        )

        extractor = PostExtractor(navegador.page)

        extractor.get_posts()

        input("Pulsa ENTER para cerrar...")

        navegador.stop()

        return []