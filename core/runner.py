from config.config import VERSION

from database.database import Database

from scrapers.solocastings_scraper import SoloCastingsScraper
from scrapers.clandestino_scraper import ClandestinoScraper
from scrapers.castingcinetv_scraper import CastingCineTVScraper
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

        scrapers = [

    SoloCastingsScraper(),

    ClandestinoScraper(),

    CastingCineTVScraper(),

]

    

        castings = []

        for scraper in scrapers:

            print(f"Ejecutando {scraper.__class__.__name__}...")

            try:

                castings.extend(scraper.scrape())

            except Exception as e:

                print(f"ERROR: {e}")

        print(f"\nCastings encontrados: {len(castings)}")

        filtro = CastingFilter()

        castings = filtro.filter(castings)

        print(f"Castings seleccionados: {len(castings)}")

        for casting in castings:

            self.db.add(casting)

        exporter = ExcelExporter()

        fichero = exporter.export(castings)

        print(f"\nExcel generado:\n{fichero}")

        print("\nRanking:\n")

        for casting in castings:

            print(

                f"{casting.puntuacion:3d}  "

                f"{casting.titulo}"

            )

        print("\nProceso finalizado correctamente.")