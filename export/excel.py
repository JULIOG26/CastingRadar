from pathlib import Path

from openpyxl import Workbook


class ExcelExporter:

    def export(self, castings, filename="exports/castings.xlsx"):

        Path("exports").mkdir(exist_ok=True)

        wb = Workbook()
        ws = wb.active
        ws.title = "Castings"

        ws.append([
            "Título",
            "Empresa",
            "Ciudad",
            "Tipo",
            "Fecha",
            "Fuente",
            "URL"
        ])

        for casting in castings:
            ws.append([
                casting.titulo,
                casting.empresa,
                casting.ciudad,
                casting.tipo,
                casting.fecha_publicacion,
                casting.fuente,
                casting.url
            ])

        wb.save(filename)

        