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

        estadisticas = {
    "descartados_keywords": 0,
    "descartados_sexo": 0,
    "descartados_edad": 0,
    "descartados_figuracion": 0,
    "descartados_remuneracion": 0,
    "descartados_produccion": 0,
}

        for casting in castings:

            texto = (
                f"{casting.titulo} "
                f"{casting.descripcion} "
                f"{casting.tipo} "
                f"{casting.ciudad}"
            )

            texto_lower = texto.lower()

            if any(p in texto_lower for p in DISCARD_KEYWORDS):
                estadisticas["descartados_keywords"] += 1
            continue
            # =====================================
            # DESCARTES RÁPIDOS (V1 JULIO)
            # =====================================

            # Ciudades / zonas que no interesan
            if any(x in texto_lower for x in [
                "tenerife",
                "mallorca",
                "sevilla",
                "barcelona",
                "amposta",
                "capellades",
                "caldes d'estrac",
]):
                continue

            # Habilidades que no interesan
            if any(x in texto_lower for x in [
                "pianista",
                "violinista",
                "bailarín",
                "bailarin",
]):
                continue

            # Promoción / representación
            if any(x in texto_lower for x in [
                "manager",
                "representación",
                "representacion",
                "coreograf",
]):
                continue
    
            # =====================================
            # DESCARTES ESPECÍFICOS
            # =====================================

            if "administrativo" in texto_lower:
                continue

            if "coreograf" in texto_lower:
                continue

            if "frases de actores" in texto_lower:
                continue

            if texto_lower.startswith("gran convocatoria internacional"):
                continue

            if texto_lower.startswith("36 likes"):
                continue

            if "nos hace mucha ilusión" in texto_lower:
                continue

            datos = self.analyzer.analyze(texto)

if len(resultado) < 5:
    print("\n==============================")
    print(casting.titulo)
    print(datos)

print("\n----------------")
print(casting.titulo)
print(datos)

if datos["sexo"] == "mujer":
                
                continue

            if (
                datos["edad_max"] is not None
                and datos["edad_max"] < USER_PROFILE["edad"]
            ):
                estadisticas["descartados_edad"] += 1
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
                
                
                es
                continue

            produccion = datos["produccion"]

            if produccion == "publicidad" and not USER_PROFILE["acepta_publicidad"]:
                estadisticas["descartados_produccion"] += 1
                continue

            if produccion == "serie" and not USER_PROFILE["acepta_series"]:
                estadisticas["descartados_produccion"] += 1
                continue

            if produccion == "largometraje" and not USER_PROFILE["acepta_largometrajes"]:
                estadisticas["descartados_produccion"] += 1
                continue

            if produccion == "cortometraje" and not USER_PROFILE["acepta_cortometrajes"]:
                e
                continue

            if produccion == "documental" and not USER_PROFILE["acepta_documentales"]:
                estadisticas["descartados_produccion"] += 1
                continue

            if produccion == "videoclip" and not USER_PROFILE["acepta_videoclips"]:
                estadisticas["descartados_produccion"] += 1
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
            print(f"PUNTOS = {puntuacion}")
            print(motivos)    

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
        print("\n========== ESTADÍSTICAS FILTRO ==========")

        for k, v in estadisticas.items():
            print(f"{k:30} {v}")

        print("=========================================\n")

        return resultado