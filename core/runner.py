from config.config import VERSION
from database.database import Database
from scrapers.test_scraper import TestScraper


class CastingRadar:
    def __init__(self):
        self.version = VERSION
        self.db = Database()

    def run(self):
        print("=" * 50)
        print("CastingRadar")
        print(f"Versión: {self.version}")
        print("=" * 50)

        print("Inicializando base de datos...")
        self.db.initialize()

        scraper = TestScraper()
        castings = scraper.scrape()

        print(f"\nSe han encontrado {len(castings)} castings.\n")

        for casting in castings:
            self.db.add(casting)

        print("Castings almacenados:\n")

        for casting in self.db.get_castings():
            print(casting)

        print("\nSistema iniciado correctamente.")