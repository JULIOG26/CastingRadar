import sqlite3
from pathlib import Path

from config.config import DATABASE_FILE
from database.models import CASTINGS_TABLE
from core.casting import Casting


class Database:
    def __init__(self):
        Path(DATABASE_FILE).parent.mkdir(parents=True, exist_ok=True)

        self.connection = sqlite3.connect(DATABASE_FILE)
        self.cursor = self.connection.cursor()

    def initialize(self):
        self.cursor.execute(CASTINGS_TABLE)
        self.connection.commit()

    def exists(self, casting: Casting):
        self.cursor.execute(
            """
            SELECT id
            FROM castings
            WHERE titulo = ?
              AND empresa = ?
              AND fuente = ?
            """,
            (
                casting.titulo,
                casting.empresa,
                casting.fuente,
            ),
        )

        return self.cursor.fetchone() is not None

    def add(self, casting: Casting):
        if self.exists(casting):
            return False

        self.cursor.execute(
            """
            INSERT INTO castings (
                titulo,
                empresa,
                contacto,
                email,
                telefono,
                ciudad,
                pais,
                tipo,
                perfil,
                descripcion,
                fecha_publicacion,
                fecha_limite,
                url,
                fuente,
                estado,
                fecha_importacion
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                casting.titulo,
                casting.empresa,
                casting.contacto,
                casting.email,
                casting.telefono,
                casting.ciudad,
                casting.pais,
                casting.tipo,
                casting.perfil,
                casting.descripcion,
                casting.fecha_publicacion,
                casting.fecha_limite,
                casting.url,
                casting.fuente,
                casting.estado,
                casting.fecha_importacion,
            ),
        )

        self.connection.commit()
        return True

    def get_castings(self):
        self.cursor.execute("SELECT * FROM castings")
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()