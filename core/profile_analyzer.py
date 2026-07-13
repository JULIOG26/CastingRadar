import re

from core.vocabulary import (
    HOMBRE,
    MUJER,
    PROTAGONISTA,
    SECUNDARIO,
    REPARTO,
    PEQUENA_PARTE,
    FEATURED_EXTRA,
    FIGURACION_ESPECIAL,
    FIGURACION,
    PUBLICIDAD,
    FICCION,
    REMUNERADO,
    NO_REMUNERADO,
    DERECHOS_IMAGEN,
    MADRID_NORTE,
    MADRID,
    NACIONAL,
)


class ProfileAnalyzer:

    def analyze(self, texto: str):

        texto = texto.lower()

        resultado = {
            "sexo": None,
            "edad_min": None,
            "edad_max": None,
            "papel": None,
            "produccion": None,
            "remunerado": None,
            "derechos": False,
            "ubicacion": "otras",
        }

        # =====================================================
        # SEXO
        # =====================================================

        hombre = any(p in texto for p in HOMBRE)
        mujer = any(p in texto for p in MUJER)

        if hombre and mujer:
            resultado["sexo"] = "ambos"
        elif hombre:
            resultado["sexo"] = "hombre"
        elif mujer:
            resultado["sexo"] = "mujer"

        # =====================================================
        # EDAD
        # =====================================================

        patrones = [
            r"(\d{2})\s*-\s*(\d{2})",
            r"(\d{2})\s*a\s*(\d{2})",
            r"de\s+(\d{2})\s+a\s+(\d{2})",
            r"entre\s+(\d{2})\s+y\s+(\d{2})",
        ]

        for patron in patrones:

            m = re.search(patron, texto)

            if m:
                resultado["edad_min"] = int(m.group(1))
                resultado["edad_max"] = int(m.group(2))
                break

        if resultado["edad_min"] is None:

            patrones = [
                r"mayor(?:es)?\s+de\s+(\d{2})",
                r"más\s+de\s+(\d{2})",
                r"mas\s+de\s+(\d{2})",
                r"a\s+partir\s+de\s+(\d{2})",
                r"(\d{2})\+",
            ]

            for patron in patrones:

                m = re.search(patron, texto)

                if m:
                    resultado["edad_min"] = int(m.group(1))
                    break

        if resultado["edad_max"] is None:

            patrones = [
                r"hasta\s+(\d{2})",
                r"menor(?:es)?\s+de\s+(\d{2})",
            ]

            for patron in patrones:

                m = re.search(patron, texto)

                if m:
                    resultado["edad_max"] = int(m.group(1))
                    break

        # =====================================================
        # REMUNERACIÓN
        # =====================================================

        if any(p in texto for p in NO_REMUNERADO):
            resultado["remunerado"] = False

        elif any(p in texto for p in REMUNERADO):
            resultado["remunerado"] = True

        # =====================================================
        # DERECHOS DE IMAGEN
        # =====================================================

        resultado["derechos"] = any(
            palabra in texto
            for palabra in DERECHOS_IMAGEN
        )         # =====================================================
        # PRODUCCIÓN
        # =====================================================

        for palabra in PUBLICIDAD:

            if palabra in texto:
                resultado["produccion"] = "publicidad"
                break

        if resultado["produccion"] is None:

            for palabra in FICCION:

                if palabra in texto:
                    resultado["produccion"] = palabra
                    break

        # =====================================================
        # PAPEL
        # =====================================================

        if any(p in texto for p in PROTAGONISTA):
            resultado["papel"] = "protagonista"

        elif any(p in texto for p in SECUNDARIO):
            resultado["papel"] = "secundario"

        elif any(p in texto for p in REPARTO):
            resultado["papel"] = "reparto"

        elif any(p in texto for p in PEQUENA_PARTE):
            resultado["papel"] = "pequena_parte"

        elif any(p in texto for p in FEATURED_EXTRA):
            resultado["papel"] = "featured_extra"

        elif any(p in texto for p in FIGURACION_ESPECIAL):
            resultado["papel"] = "figuracion_especial"

        elif any(p in texto for p in FIGURACION):
            resultado["papel"] = "figuracion"

        # =====================================================
        # UBICACIÓN
        # =====================================================

        if any(p in texto for p in MADRID_NORTE):
            resultado["ubicacion"] = "madrid_norte"

        elif any(p in texto for p in MADRID):
            resultado["ubicacion"] = "madrid"

        elif any(p in texto for p in NACIONAL):
            resultado["ubicacion"] = "nacional"

        else:
            resultado["ubicacion"] = "otras"

        return resultado