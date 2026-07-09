from config.config import VERSION
from database.database import Database


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

        print("Sistema iniciado correctamente.")