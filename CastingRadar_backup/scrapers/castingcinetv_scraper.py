import requests

from core.casting import Casting

from core.utils.date_parser import parse_date
class CastingCineTVScraper:

    URL = "https://castingscinetv.com/feeds/posts/default/-/Espa%C3%B1a?alt=json&max-results=30"

    def scrape(self):

        response = requests.get(
            self.URL,
            timeout=20
        )

        response.raise_for_status()

        data = response.json()

        castings = []

        entries = data.get("feed", {}).get("entry", [])

        for entry in entries:

            titulo = entry["title"]["$t"]

            fecha = entry["published"]["$t"][:10]

            url = ""

            for link in entry["link"]:

                if link["rel"] == "alternate":
                    url = link["href"]
                    break

            casting = Casting(
                titulo=titulo,
                
                url=url,
                fuente="CastingCineTV",
            )

            castings.append(casting)

        return castings