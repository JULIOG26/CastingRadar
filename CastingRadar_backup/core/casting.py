from dataclasses import dataclass
from typing import Optional


@dataclass
class Casting:

    titulo: str

    empresa: str = ""

    contacto: str = ""

    email: str = ""

    telefono: str = ""

    ciudad: str = ""

    pais: str = ""

    tipo: str = ""

    perfil: str = ""

    descripcion: str = ""

    fecha_publicacion: str = ""

    fecha_limite: str = ""

    url: str = ""

    fuente: str = ""

    estado: str = "Nuevo"

    fecha_importacion: str = ""

    # Calculados por CastingRadar

    puntuacion: int = 0

    analisis: Optional[dict] = None