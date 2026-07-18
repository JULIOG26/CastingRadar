import re

from core.casting import Casting


class PostParser:

    PALABRAS_DESCARTAR = [

        "casting cerrado",
        "cast cerrado",
        "casting finalizado",
        "closed",

        "new office",
        "nueva oficina",

        "premios",
        "award",
        "awards",

        "estreno",
        "trailer",
        "teaser",

        "festival",

        "making of",
        "behind the scenes",
        "backstage",

        "felicidades",
        "enhorabuena",

        "photo dump",

        "hace un año",
        "aniversario",
    ]

    PALABRAS_ACTORES = [

        "actor",
        "actriz",
        "actores",
        "actrices",

        "figurante",
        "figurantes",

        "extra",
        "extras",

        "reparto",

        "featured extra",
        "figuración",
        "figuracion",

    ]

    def parse(self, usuario, url, texto):

        texto_l = texto.lower()

        # -----------------------------------
        # DESCARTES
        # -----------------------------------

        if any(p in texto_l for p in self.PALABRAS_DESCARTAR):
            return None

        acepta = False

        # -----------------------------------
        # CASTING
        # -----------------------------------

        if "casting" in texto_l:
            acepta = True

        # -----------------------------------
        # SE BUSCA
        # -----------------------------------

        elif (
            "se busca" in texto_l
            or "se buscan" in texto_l
        ):

            if any(
                p in texto_l
                for p in self.PALABRAS_ACTORES
            ):
                acepta = True

        # -----------------------------------
        # RODAJE
        # -----------------------------------

        elif "rodaje" in texto_l:

            if any(
                p in texto_l
                for p in self.PALABRAS_ACTORES
            ):
                acepta = True

        # -----------------------------------
        # PUBLICIDAD
        # -----------------------------------

        elif "publicidad" in texto_l:

            if any(
                p in texto_l
                for p in self.PALABRAS_ACTORES
            ):
                acepta = True

        # -----------------------------------
        # DERECHOS
        # -----------------------------------

        elif (
            "buyout" in texto_l
            or "derechos de imagen" in texto_l
        ):
            acepta = True

        if not acepta:
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

        for linea in texto.splitlines():

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

            m = re.search(
                patron,
                texto,
                re.IGNORECASE,
            )

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