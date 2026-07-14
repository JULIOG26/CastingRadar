from pathlib import Path
from datetime import datetime

from openpyxl import Workbook
from openpyxl.styles import Font


class ExcelExporter:

    def __init__(self):

        self.export_dir = Path("exports")
        self.export_dir.mkdir(exist_ok=True)

    def export(self, castings):

        wb = Workbook()
        ws = wb.active

        ws.title = "CastingRadar"

        cabeceras = [
            "Puntos",
            "Publicación",
            "Límite",
            "Interés",
            "Papel",
            "Producción",
            "Remunerado",
            "Derechos",
            "Ubicación",
            "Sexo",
            "Edad",
            "Título",
            "Empresa",
            "Ciudad",
            "Fuente",
            "URL",

            # Columnas de trabajo de Julio
            "Decisión",
            "Motivo",
            "Comentarios",
            "Revisado",
            "Presentado",
            "Resultado",
        ]

        ws.append(cabeceras)

        for cell in ws[1]:
            cell.font = Font(bold=True)

        for casting in castings:

            analisis = casting.analisis or {}

            edad = ""

            if (
                analisis.get("edad_min") is not None
                or analisis.get("edad_max") is not None
            ):
                edad = (
                    f'{analisis.get("edad_min", "")}'
                    f'-'
                    f'{analisis.get("edad_max", "")}'
                )

            puntos = casting.puntuacion

            if puntos >= 100:
                interes = "★★★★★"
            elif puntos >= 80:
                interes = "★★★★"
            elif puntos >= 60:
                interes = "★★★"
            elif puntos >= 40:
                interes = "★★"
            else:
                interes = "★"

            ws.append([
                puntos,
                casting.fecha_publicacion,
                casting.fecha_limite,
                interes,
                analisis.get("papel", ""),
                analisis.get("produccion", ""),
                analisis.get("remunerado", ""),
                analisis.get("derechos", ""),
                analisis.get("ubicacion", ""),
                analisis.get("sexo", ""),
                edad,
                casting.titulo,
                casting.empresa,
                casting.ciudad,
                casting.fuente,
                casting.url,

                "",   # Decisión
                "",   # Motivo
                "",   # Comentarios
                "",   # Revisado
                "",   # Presentado
                "",   # Resultado
            ])

        nombre = (
            f"CastingRadar_"
            f"{datetime.now():%Y%m%d_%H%M%S}.xlsx"
        )

        fichero = self.export_dir / nombre

        wb.save(fichero)

        return fichero