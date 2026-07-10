from config.preferences import (
    KEYWORDS_POSITIVE,
    KEYWORDS_NEGATIVE,
)


class CastingFilter:

    def filter(self, castings):

        resultado = []

        for casting in castings:

            texto = (
                casting.titulo + " " +
                casting.descripcion
            ).lower()

            # Descartar si contiene palabras negativas
            descartar = False

            for palabra in KEYWORDS_NEGATIVE:
                if palabra.lower() in texto:
                    descartar = True
                    break

            if descartar:
                continue

            # Aceptar si contiene palabras positivas
            for palabra in KEYWORDS_POSITIVE:
                if palabra.lower() in texto:
                    resultado.append(casting)
                    break

        return resultado