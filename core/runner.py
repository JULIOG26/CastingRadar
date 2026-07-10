from config.config import VERSION
from database.database import Database
from scrapers.solocastings_scraper import SoloCastingsScraper
from core.filter import CastingFilter
from export.excel import ExcelExporter


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

        # Obtener castings
        scraper = SoloCastingsScraper()
        castings = scraper.scrape()

        print(f"\nSe han encontrado {len(castings)} castings.")

        # Aplicar filtro
        filtro = CastingFilter()
        castings = filtro.filter(castings)

        print(f"Después del filtro quedan {len(castings)} castings.\n")

        # Guardar en la base de datos
        for casting in castings:
            self.db.add(casting)

        # Exportar a Excel
        exporter = ExcelExporter()
        exporter.export(castings)

        # Mostrar los castings seleccionados
        print("Castings seleccionados:\n")

        for casting in castings:
            print(f"- {casting.titulo}")

        print("\nSistema iniciado correctamente.")