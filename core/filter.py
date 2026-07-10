class CastingFilter:

    KEYWORDS = [
        "60",
        "65",
        "70",
        "senior",
        "padre",
        "abuelo",
        "hombre",
        "actor",
    ]

    def filter(self, castings):

        resultado = []

        for casting in castings:

            texto = (
                casting.titulo + " " +
                casting.descripcion
            ).lower()

            for palabra in self.KEYWORDS:

                if palabra.lower() in texto:
                    resultado.append(casting)
                    break

        return resultado