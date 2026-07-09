from core.casting import Casting
from scrapers.base_scraper import BaseScraper


class TestScraper(BaseScraper):
    def __init__(self):
        super().__init__("Test")

    def scrape(self):
        return [
            Casting(
                titulo="Actor 60-70 años",
                empresa="Productora Alfa",
                ciudad="Madrid",
                tipo="Serie",
                fuente="Test"
            ),
            Casting(
                titulo="Publicidad banco",
                empresa="Agencia Beta",
                ciudad="Barcelona",
                tipo="Publicidad",
                fuente="Test"
            ),
            Casting(
                titulo="Cortometraje independiente",
                empresa="Escuela de Cine",
                ciudad="Valencia",
                tipo="Cine",
                fuente="Test"
            )
        ]