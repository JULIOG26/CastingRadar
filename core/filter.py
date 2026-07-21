import re


class CastingFilter:

    def __init__(self):

        self.stats = {
            "descartados_keywords": 0,
            "descartados_sexo": 0,
            "descartados_edad": 0,
            "descartados_figuracion": 0,
            "descartados_remuneracion": 0,
            "descartados_produccion": 0,
        }

    # -----------------------------------------------------

    def filter(self, castings):

        resultado = []

        for c in castings:

            texto = (
                f"{c.titulo} "
                f"{c.descripcion}"
            ).lower()

            # -----------------------------------
            # DESCARTES ABSOLUTOS
            # -----------------------------------

            if self.descartar(texto):
                self.stats["descartados_keywords"] += 1
                continue

            # -----------------------------------

            puntuacion = getattr(c, "puntuacion", 0)

            puntuacion += self.puntuar(texto)

            c.puntuacion = puntuacion

            resultado.append(c)

        resultado.sort(
            key=lambda x: x.puntuacion,
            reverse=True,
        )

        print("\n========== ESTADÍSTICAS FILTRO ==========")

        for k, v in self.stats.items():
            print(f"{k:30} {v}")

        print("=========================================\n")

        return resultado

    # -----------------------------------------------------

    def descartar(self, texto):

            basura = [

            "masterclass",
            "workshop",
            "curso",
            "seminario",
            "conferencia",
            "festival",
            "making of",
            "behind the scenes",
            "casting director",
            "director de casting",

            "estreno",
            "trailer",

            "photo dump",

            "gracias",
            "felicidades",
            "enhorabuena",

            "nuevo despacho",
            "new office",

            "premios",
            "award",

        ]

            return any(x in texto for x in basura)

    # -----------------------------------------------------
    def puntuar(self, texto):

        p = 0

# PRODUCCIÓN

        if "netflix" in texto:
            p += 80
        if "amazon" in texto:
            p += 70

        if "prime video" in texto:
            p += 70

        if "disney" in texto:
            p += 70

        if "movistar" in texto:
            p += 60

        if "atresmedia" in texto:
            p += 60

        if "mediaset" in texto:
            p += 60

# TIPO

        if "publicidad" in texto:
            p += 40

        if "campaña" in texto:
            p += 40

        if "serie" in texto:
            p += 30

        if "película" in texto:
            p += 30

        if "largometraje" in texto:
            p += 30

# REMUNERACIÓN

        if "remunerado" in texto:
            p += 30

        if "buyout" in texto:
            p += 25

        if "derechos de imagen" in texto:
            p += 25

# ZONA PREFERENTE

        if "alcobendas" in texto:
            p += 45

        if "san sebastián de los reyes" in texto:
            p += 45

        if "san sebastian de los reyes" in texto:
            p += 45

        if "ssrr" in texto:
            p += 45

        if "tres cantos" in texto:
            p += 30

        if "colmenar viejo" in texto:
            p += 25

        if "madrid norte" in texto:
            p += 25

        if "madrid" in texto:
            p += 20

        # MADRID

        if "madrid" in texto:
            p += 20

        if "comunidad de madrid" in texto:
            p += 20

# PAPEL

        if "actor principal" in texto:
            p += 40


        if "actor secundario" in texto:
            p += 25


# PENALIZACIONES

        if "tfg" in texto:
            p -= 120

        if "universidad" in texto:
            p -= 100

        if "escuela" in texto:
            p -= 100

        if "proyecto de alumnos" in texto:
            p -= 100

        if "sin remuneración" in texto:
            p -= 120

        if "colaboración" in texto:
            p -= 80

        if "videoclip" in texto:
            p -= 40

        return p