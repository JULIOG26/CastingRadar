import re

from core.casting import Casting


class PostParser:

    PALABRAS_CASTING = [
        "casting",
        "actor",
        "actriz",
        "actores",
        "actrices",
        "figurante",
        "figurantes",
        "extra",
        "extras",
        "reparto",
        "publicidad",
        "rodaje",
        "ficción",
        "ficcion",
    ]

    PALABRAS_DESCARTAR = [
        "casting cerrado",
        "cast cerrado",
        "casting finalizado",
        "closed",
        "enhorabuena",
        "premios",
        "estreno",
        "trailer",
        "festival",
        "making of",
        "behind the scenes",
    ]

    def parse(self, usuario, url, texto):

        texto_l = texto.lower()

        # Debe contener palabras relacionadas con casting
        if not any(p in texto_l for p in self.PALABRAS_CASTING):
            return None

        # Descartar publicaciones que no son oportunidades
        if any(p in texto_l for p in self.PALABRAS_DESCARTAR):
            return None

        return Casting(
            titulo=self.buscar_titulo(texto),
            empresa=usuario,
            ciudad=self.buscar_ciudad(texto),
            descripcion=texto,
            fecha_publicacion=self.buscar_fecha(texto),
            email=self.buscar_email(texto),
            url=url,
            fuente="Instagram",
        )

    # -----------------------------------------------------

    def buscar_titulo(self, texto):

        texto = re.sub(
            r'^\d+\s+likes?,?\s*\d*\s*comments?\s*-\s*.*?:\s*"?',
            "",
            texto,
            flags=re.IGNORECASE,
        )

        lineas = texto.splitlines()

        for linea in lineas:

            linea = linea.strip()

            if not linea:
                continue

            if "casting" in linea.lower():
                return linea

        return "Casting Instagram"

    # -----------------------------------------------------

    def buscar_ciudad(self, texto):

        patrones = [
            r"📍\s*([^\n]+)",
            r"Provincia\s+([^\n]+)",
            r"Comunidad\s+([^\n]+)",
        ]

        for patron in patrones:

            m = re.search(patron, texto, re.IGNORECASE)

            if m:
                return m.group(1).strip()

        return ""

    # -----------------------------------------------------

    def buscar_fecha(self, texto):

        m = re.search(
            r"el\s+([A-Za-z]+\s+\d{1,2},\s+\d{4})",
            texto,
        )

        if m:
            return m.group(1)

        return ""

    # -----------------------------------------------------

    def buscar_email(self, texto):

        m = re.search(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            texto,
        )

        if m:
            return m.group(0)

        return ""