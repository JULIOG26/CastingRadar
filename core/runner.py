from config.config import VERSION
from core.casting import Casting
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

        casting = Casting(
            titulo="Casting de prueba",
            empresa="OpenAI Producciones",
            ciudad="Madrid",
            tipo="Publicidad",
            fuente="Prueba"
        )

        self.db.add(casting)

        print("\nCastings almacenados:\n")

        for casting in self.db.get_castings():
            print(casting)

        print("Sistema iniciado correctamente.")