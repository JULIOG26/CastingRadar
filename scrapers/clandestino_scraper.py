import requests
from bs4 import BeautifulSoup

from core.casting import Casting


class ClandestinoScraper:

    URL = "https://clandestinocastings.com/castings/todos-los-anuncios"

    def scrape(self):

        response = requests.get(
            self.URL,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=20
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")

        anuncios = soup.select("div.listing-summary")

        castings = []

        for anuncio in anuncios:

            try:

                # ---------- Título ----------
                enlace = anuncio.select_one("h3.summary-title a")

                if not enlace:
                    continue

                titulo = enlace.get_text(strip=True)

                href = enlace.get("href", "")

                if href.startswith("/"):
                    url = "https://clandestinocastings.com" + href
                else:
                    url = href

                # ---------- Fecha ----------
                fecha = ""

                tiempo = anuncio.find("time")

                if tiempo:
                    fecha = tiempo.get_text(strip=True)

                # ---------- Descripción ----------
                descripcion = ""

                p = anuncio.select_one("p.summary-description")

                if p:
                    descripcion = p.get_text(" ", strip=True)

                # ---------- Tipo ----------
                tipo = ""

                tag = anuncio.select_one("span.tag-proyecto a")

                if tag:
                    tipo = tag.get_text(strip=True)

                # ---------- Ciudad ----------
                ciudad = ""

                provincia = anuncio.select_one("span.tag-provincia a")

                if provincia:
                    ciudad = provincia.get_text(strip=True)

                # ---------- Perfil ----------
                perfil = ""

                edad = anuncio.select_one("span.tag-edad")

                if edad:
                    perfil = edad.get_text(" ", strip=True)

                casting = Casting(
                    titulo=titulo,
                    ciudad=ciudad,
                    tipo=tipo,
                    perfil=perfil,
                    descripcion=descripcion,
                    fecha_publicacion=fecha,
                    url=url,
                    fuente="Clandestino"
                )

                castings.append(casting)

            except Exception as e:
                print("Error:", e)

        return castings