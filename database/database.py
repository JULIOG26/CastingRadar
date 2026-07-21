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

        # Si hay URL, es el mejor identificador
        if casting.url:

            self.cursor.execute(
                """
                SELECT id
                FROM castings
                WHERE url = ?
                """,
                (casting.url,),
            )

            if self.cursor.fetchone():
                return True

        # Si no hay URL, usar el título
        self.cursor.execute(
            """
            SELECT id
            FROM castings
            WHERE titulo = ?
            """,
            (casting.titulo,),
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

        self.cursor.execute(
            """
            SELECT
                titulo,
                empresa,
                ciudad,
                descripcion,
                fecha_publicacion,
                fecha_limite,
                email,
                telefono,
                url,
                fuente
            FROM castings
            """
        )

        filas = self.cursor.fetchall()

        resultado = []

        for fila in filas:

            resultado.append(
                Casting(
                    titulo=fila[0],
                    empresa=fila[1],
                    ciudad=fila[2],
                    descripcion=fila[3],
                    fecha_publicacion=fila[4],
                    fecha_limite=fila[5],
                    email=fila[6],
                    telefono=fila[7],
                    url=fila[8],
                    fuente=fila[9],
                )
            )

        return resultado

    def close(self):
        self.connection.close()