from config.profile import USER_PROFILE


import re

from config.scoring import (
    ROLE_SCORE,
    PRODUCTION_SCORE,
    REMUNERATION_SCORE,
    RIGHTS_SCORE,
    LOCATION_SCORE,
    SEX_SCORE,
    AGE_MATCH_SCORE,
    AGE_UNKNOWN_SCORE,
)

from config.discard_keywords import DISCARD_KEYWORDS
from config.penalty_keywords import PENALTY_KEYWORDS
from config.positive_keywords import POSITIVE_KEYWORDS

from core.profile_analyzer import ProfileAnalyzer


def normalizar_titulo(titulo):

    titulo = titulo.lower()

    titulo = re.sub(r"[\"'.,:;!?()]", "", titulo)

    titulo = re.sub(r"\s+", " ", titulo)

    return titulo.strip()



class CastingFilter:

    def __init__(self):
        self.analyzer = ProfileAnalyzer()

    def filter(self, castings):

        resultado = []

        for casting in castings:

            texto = (
                f"{casting.titulo} "
                f"{casting.descripcion} "
                f"{casting.tipo} "
                f"{casting.ciudad}"
            )

            texto_lower = texto.lower()

            if any(p in texto_lower for p in DISCARD_KEYWORDS):
                continue

            datos = self.analyzer.analyze(texto)

            if datos["sexo"] == "mujer":
                continue

            if (
                datos["edad_max"] is not None
                and datos["edad_max"] < USER_PROFILE["edad"]
            ):
                continue

            if (
                datos["edad_min"] is not None
                and datos["edad_min"] > USER_PROFILE["edad"]
            ):
                continue

            if (
                datos["papel"] == "figuracion"
                and not USER_PROFILE["acepta_figuracion"]
            ):
                continue

            if (
                datos["remunerado"] is False
                and not USER_PROFILE["acepta_no_remunerado"]
            ):
                continue

            produccion = datos["produccion"]

            if produccion == "publicidad" and not USER_PROFILE["acepta_publicidad"]:
                continue

            if produccion == "serie" and not USER_PROFILE["acepta_series"]:
                continue

            if produccion == "largometraje" and not USER_PROFILE["acepta_largometrajes"]:
                continue

            if produccion == "cortometraje" and not USER_PROFILE["acepta_cortometrajes"]:
                continue

            if produccion == "documental" and not USER_PROFILE["acepta_documentales"]:
                continue

            if produccion == "videoclip" and not USER_PROFILE["acepta_videoclips"]:
                continue

            puntuacion = 0
            motivos = []

            puntos = ROLE_SCORE.get(datos["papel"], 0)
            puntuacion += puntos
            if puntos:
                motivos.append(f"Rol: +{puntos}")

            puntos = PRODUCTION_SCORE.get(produccion, 0)
            puntuacion += puntos
            if puntos:
                motivos.append(f"Producción: +{puntos}")

            puntos = REMUNERATION_SCORE.get(datos["remunerado"], 0)
            puntuacion += puntos
            if puntos:
                motivos.append(f"Remuneración: +{puntos}")

            puntos = LOCATION_SCORE.get(datos["ubicacion"], 0)
            puntuacion += puntos
            if puntos:
                motivos.append(f"Ubicación: +{puntos}")

            puntos = SEX_SCORE.get(datos["sexo"], 0)
            puntuacion += puntos
            if puntos:
                motivos.append(f"Sexo: +{puntos}")

            puntos = RIGHTS_SCORE.get(datos["derechos"], 0)
            puntuacion += puntos
            if puntos:
                motivos.append(f"Derechos: +{puntos}")
            if datos["edad_min"] is None and datos["edad_max"] is None:
                puntuacion += AGE_UNKNOWN_SCORE
                motivos.append(f"Edad desconocida: +{AGE_UNKNOWN_SCORE}")
            else:
                puntuacion += AGE_MATCH_SCORE
                motivos.append(f"Edad compatible: +{AGE_MATCH_SCORE}")

            if produccion == "publicidad" and datos["derechos"]:
                puntuacion += 15
                motivos.append("Publicidad + Derechos: +15")

            if datos["papel"] == "featured_extra" and produccion == "publicidad":
                puntuacion += 10
                motivos.append("Featured Extra + Publicidad: +10")

            if datos["ubicacion"] == "madrid_norte" and produccion == "publicidad":
                puntuacion += 5
                motivos.append("Madrid Norte + Publicidad: +5")
                puntuacion += 5  

            for palabra, puntos in PENALTY_KEYWORDS.items():
                if palabra in texto_lower:
                    puntuacion -= puntos
                    motivos.append(f"Penalización ({palabra}): -{puntos}")

            for palabra, puntos in POSITIVE_KEYWORDS.items():
                if palabra in texto_lower:
                    puntuacion += puntos
                    motivos.append(f"Bonus ({palabra}): +{puntos}")

            casting.puntuacion = puntuacion
            casting.analisis = datos
            casting.motivos = motivos
    
            if puntuacion > 0:
                resultado.append(casting)

                # =====================================
        # ELIMINAR DUPLICADOS
        # =====================================

        unicos = {}

        for casting in resultado:

            clave = normalizar_titulo(casting.titulo)

            if (
                clave not in unicos
                or casting.puntuacion > unicos[clave].puntuacion
            ):
                unicos[clave] = casting

        resultado = list(unicos.values())

        resultado.sort(
            key=lambda c: c.puntuacion,
            reverse=True,
        )

        return resultado