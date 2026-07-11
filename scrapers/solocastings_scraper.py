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

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")

        anuncios = soup.select("td.txtlistados")

        castings = []

        for anuncio in anuncios:

            try:

                enlace = anuncio.find("a")

                if not enlace:
                    continue

                titulo = enlace.get_text(strip=True)
                url = enlace["href"]

                linea2 = anuncio.find("span", class_="linea2")
                linea3 = anuncio.find("span", class_="linea3")

                empresa = ""
                ciudad = ""
                fecha = ""

                if linea2:

                    texto = linea2.get_text(strip=True)

                    if "organizado por" in texto and " en " in texto:
                        texto = texto.replace("organizado por ", "")
                        empresa, ciudad = texto.rsplit(" en ", 1)

                if linea3:
                    fecha = linea3.get_text(strip=True).replace("Publicado el ", "")

                descripcion = ""
                tipo = ""

                try:

                    detalle = requests.get(
                        url,
                        headers=self.HEADERS,
                        timeout=20,
                        allow_redirects=False
                    )

                    if detalle.status_code in (301, 302, 303, 307, 308):
                        continue

                    detalle.raise_for_status()

                    detalle_soup = BeautifulSoup(detalle.text, "lxml")

                    meta = detalle_soup.find(
                        "meta",
                        attrs={"name": "description"}
                    )

                    if meta:
                        contenido = meta.get("content", "").lower()

                        if contenido.startswith("castings para "):
                            tipo = contenido.replace(
                                "castings para ",
                                ""
                            ).capitalize()

                    texto = detalle_soup.find("p", class_="casting_text")

                    if texto:
                        descripcion = texto.get_text(" ", strip=True)

                except requests.exceptions.TooManyRedirects:
                    continue

                except Exception as e:
                    print(f"Error leyendo {url}: {e}")
                    continue

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

            except Exception as e:
                print(f"Error procesando anuncio: {e}")

        return castings