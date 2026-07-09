import sqlite3
from pathlib import Path

from config.config import DATABASE_FILE
from database.models import CASTINGS_TABLE


class Database:
    def __init__(self):
        # Crear la carpeta "data" si no existe
        Path(DATABASE_FILE).parent.mkdir(parents=True, exist_ok=True)

        self.connection = sqlite3.connect(DATABASE_FILE)
        self.cursor = self.connection.cursor()

    def initialize(self):
        """Crea las tablas principales si no existen."""
        self.cursor.execute(CASTINGS_TABLE)
        self.connection.commit()

    def close(self):
        self.connection.close()