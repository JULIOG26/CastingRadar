from datetime import datetime

MESES = {
    "ene": 1,
    "feb": 2,
    "mar": 3,
    "abr": 4,
    "may": 5,
    "jun": 6,
    "jul": 7,
    "ago": 8,
    "sep": 9,
    "oct": 10,
    "nov": 11,
    "dic": 12,
}


def parse_date(texto):

    if not texto:
        return ""

    texto = texto.strip().lower()

    formatos = (
        "%Y-%m-%d",
        "%d-%m-%Y",
        "%d/%m/%Y",
    )

    for formato in formatos:
        try:
            return datetime.strptime(texto, formato).strftime("%Y-%m-%d")
        except ValueError:
            pass

    if " de " in texto:
        partes = texto.split()

        # 14 de jul de 2026
        if len(partes) >= 5:

            dia = int(partes[0])
            mes = MESES.get(partes[2][:3], 0)
            anio = int(partes[4])

            if mes:
                return datetime(anio, mes, dia).strftime("%Y-%m-%d")

    return texto