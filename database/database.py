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

    def add_casting(
        self,
        titulo,
        empresa,
        contacto="",
        email="",
        telefono="",
        ciudad="",
        pais="",
        tipo="",
        perfil="",
        descripcion="",
        fecha_publicacion="",
        fecha_limite="",
        url="",
        fuente="",
        estado="Nuevo",
        fecha_importacion=""
    ):
        self.cursor.execute("""
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
        """, (
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
        ))

        self.connection.commit()

    def add(self, casting: Casting):
        self.add_casting(
            titulo=casting.titulo,
            empresa=casting.empresa,
            contacto=casting.contacto,
            email=casting.email,
            telefono=casting.telefono,
            ciudad=casting.ciudad,
            pais=casting.pais,
            tipo=casting.tipo,
            perfil=casting.perfil,
            descripcion=casting.descripcion,
            fecha_publicacion=casting.fecha_publicacion,
            fecha_limite=casting.fecha_limite,
            url=casting.url,
            fuente=casting.fuente,
            estado=casting.estado,
            fecha_importacion=casting.fecha_importacion,
        )

    def get_castings(self):
        self.cursor.execute("SELECT * FROM castings")
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()