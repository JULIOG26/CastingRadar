from config.config import VERSION
from database.database import Database
from scrapers.solocastings_scraper import SoloCastingsScraper
from export.excel import ExcelExporter
from core.filter import CastingFilter


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

        # Lista de scrapers
        scrapers = [
            SoloCastingsScraper(),NuevaFuenteScraper(),
        ]

        castings = []

        # Ejecutar todos los scrapers
        for scraper in scrapers:
            castings.extend(scraper.scrape())

        print(f"\nSe han encontrado {len(castings)} castings.")

        # Filtrar resultados
        filtro = CastingFilter()
        castings = filtro.filter(castings)

        print(f"Después del filtro quedan {len(castings)} castings.\n")

        # Guardar en la base de datos
        for casting in castings:
            self.db.add(casting)

        # Exportar a Excel
        exporter = ExcelExporter()
        exporter.export(castings)

        print("\nExcel exportado: exports/castings.xlsx")

        print("\nCastings seleccionados:\n")

        for casting in castings:
            print(f"- {casting.titulo}")

        print("\nSistema iniciado correctamente.")