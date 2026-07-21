from config.config import VERSION

from database.database import Database

from core.filter import CastingFilter

from export.excel import ExcelExporter

from scrapers.solocastings_scraper import SoloCastingsScraper
from scrapers.clandestino_scraper import ClandestinoScraper
from scrapers.castingcinetv_scraper import CastingCineTVScraper
# from scrapers.instagram_v2.engine import InstagramEngineV2


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
            CastingCineTVScraper()
        ]

        castings = []

        for scraper in scrapers:
            print(f"Ejecutando {scraper.__class__.__name__}...")
            try:
                antes = len(castings)
                castings.extend(scraper.scrape())
                despues = len(castings)
                print(f"  +{despues - antes} castings")
            except Exception as e:
                print(f"ERROR: {e}")

# =====================================
# INSTAGRAM DESACTIVADO TEMPORALMENTE
# =====================================

# print("Ejecutando Instagram V2...")
# try:
#     instagram = InstagramEngineV2()
#     antes = len(castings)
#     castings.extend(instagram.scrape())
#     despues = len(castings)
#     print(f"  +{despues - antes} castings")
# except Exception as e:
#     print(f"ERROR Instagram: {e}")


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
            print(f"{casting.puntuacion:3d}  [{casting.fuente}] {casting.titulo}")

        print("\nProceso finalizado correctamente.")