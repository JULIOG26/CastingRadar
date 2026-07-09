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
        self.db.add_casting(
            titulo="Casting de prueba",
            empresa="OpenAI Producciones",
            ciudad="Madrid",
            tipo="Publicidad",
            fuente="Prueba"
        )

        print("\nCastings almacenados:\n")

        for casting in self.db.get_castings():
            print(casting)
        print("Sistema iniciado correctamente.")