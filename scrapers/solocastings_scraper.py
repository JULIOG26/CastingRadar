import requests
from bs4 import BeautifulSoup

from core.casting import Casting


class SoloCastingsScraper:

    URL = "https://www.solocastings.es/castings/"

    def scrape(self):

        response = requests.get(
            self.URL,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=20
        )

        soup = BeautifulSoup(response.text, "lxml")

        anuncios = soup.select("td.txtlistados")

        castings = []

        for anuncio in anuncios:

            enlace = anuncio.find("a")

            titulo = enlace.get_text(strip=True)
            url = enlace["href"]

            linea2 = anuncio.find("span", class_="linea2").get_text(strip=True)
            linea3 = anuncio.find("span", class_="linea3").get_text(strip=True)

            empresa = ""
            ciudad = ""

            if "organizado por" in linea2 and " en " in linea2:
                texto = linea2.replace("organizado por ", "")
                empresa, ciudad = texto.rsplit(" en ", 1)

            fecha = linea3.replace("Publicado el ", "")

            casting = Casting(
                titulo=titulo,
                empresa=empresa,
                ciudad=ciudad,
                fecha_publicacion=fecha,
                url=url,
                fuente="SoloCastings"
            )

            castings.append(casting)

        return castings