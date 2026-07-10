import requests
from bs4 import BeautifulSoup

from core.casting import Casting


class SoloCastingsScraper:

    URL = "https://www.solocastings.es/castings/"

    HEADERS = {
        "User-Agent": "Mozilla/5.0"
    }

    def scrape(self):

        response = requests.get(
            self.URL,
            headers=self.HEADERS,
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

            descripcion = ""
            tipo = ""

            try:

                detalle = requests.get(
                    url,
                    headers=self.HEADERS,
                    timeout=20
                )

                detalle_soup = BeautifulSoup(detalle.text, "lxml")

                meta = detalle_soup.find("meta", attrs={"name": "description"})

                if meta:
                    contenido = meta.get("content", "").lower()

                    if contenido.startswith("castings para "):
                        tipo = contenido.replace("castings para ", "").capitalize()

                texto = detalle_soup.find("p", class_="casting_text")

                if texto:
                    descripcion = texto.get_text(" ", strip=True)

            except Exception as e:
                print(f"Error leyendo {url}: {e}")

            casting = Casting(
                titulo=titulo,
                empresa=empresa,
                ciudad=ciudad,
                tipo=tipo,
                descripcion=descripcion,
                fecha_publicacion=fecha,
                url=url,
                fuente="SoloCastings"
            )

            castings.append(casting)

        return castings