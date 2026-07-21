import re

from core.casting import Casting


class PostParser:

    PALABRAS_DESCARTAR = [

        "casting cerrado",
        "cast cerrado",
        "casting finalizado",
        "closed",
        "casting director",
        "castingdirector",
        "director de casting",
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
        "desde la creatividad",
        "masterclass",
        "curso",
        "ponencia",
        "charla",
        "workshop",
        "nos hace muy felices",
        "gracias",
        "siempre es un placer",
        "hemos formado parte",
        "creatividad",
        "conferencia",
        "masterclass",
                "casting de",
        "casting por",
        "casting realizado",
        "dirección de casting",
        "direccion de casting",
        "equipo de casting",
        "nos encargamos del casting",
        "ya podéis ver",
        "ya podeis ver",
        "os presentamos",
        "muy felices",
        "ha sido un placer",
        "encaja perfectamente",
        "todo el reparto",
        "director de casting",
        "castingdirector",
        "app.sondecasting.com",
        "regístrate",
        "registrate",
        
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

        if (
    "casting" in texto_l
    and (
        "se busca" in texto_l
        or "se buscan" in texto_l
        or "buscamos" in texto_l
        or any(p in texto_l for p in self.PALABRAS_ACTORES)
    )
):
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

        titulo = self.buscar_titulo(texto)

        if titulo is None:
            return None

        if titulo.startswith("@"):
            return None

        if titulo.count("@") >= 1 and len(titulo) < 40:
            return None

        ciudad = self.buscar_ciudad(texto)
    
        return Casting(
            titulo=titulo,
            empresa=usuario,
            ciudad=ciudad,
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

        mejor = None
        mejor_puntuacion = -999

    for linea in texto.splitlines():

        linea = linea.strip()

        if len(linea) < 8:
            continue

        l = linea.lower()

        puntos = 0

        # -------------------------
        # POSITIVOS
        # -------------------------

        if "casting" in l:
            puntos += 100

        if "se busca" in l or "se buscan" in l:
            puntos += 80

        if "buscamos" in l:
            puntos += 70

        if "actor" in l:
            puntos += 50

        if "actriz" in l:
            puntos += 50

        if "actores" in l:
            puntos += 50

        if "actrices" in l:
            puntos += 50

        if "figurante" in l:
            puntos += 40

        if "extra" in l:
            puntos += 40

        if "publicidad" in l:
            puntos += 30

        if "rodaje" in l:
            puntos += 30

        if "reparto" in l:
            puntos += 20

        # -------------------------
        # NEGATIVOS
        # -------------------------

        if l.startswith("@"):
            puntos -= 300

        if l.count("@") >= 1:
            puntos -= 150

        if "casting director" in l:
            puntos -= 300

        if "director de casting" in l:
            puntos -= 300

        if "gracias" in l:
            puntos -= 200

        if "felices" in l:
            puntos -= 200

        if "placer" in l:
            puntos -= 150

        if "making of" in l:
            puntos -= 300

        if "behind the scenes" in l:
            puntos -= 300

        if "estreno" in l:
            puntos -= 250

        if "premio" in l:
            puntos -= 250

        if "masterclass" in l:
            puntos -= 300

        if "curso" in l:
            puntos -= 300

        if "workshop" in l:
            puntos -= 300

        if puntos > mejor_puntuacion:
            mejor_puntuacion = puntos
            mejor = linea

    if mejor_puntuacion < 60:
        return None

    return mejor
       

    # -----------------------------------------------------

    # -----------------------------------------------------

    def buscar_ciudad(self, texto):
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