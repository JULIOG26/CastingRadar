import csv
from pathlib import Path


class SourceManager:

    def __init__(self):

        self.resources = (
            Path(__file__).resolve().parent.parent
            / "resources"
        )

    def load_instagram_accounts(self):

        filename = self.resources / "instagram_accounts.csv"

        accounts = []

        if not filename.exists():
            return accounts

        with open(filename, newline="", encoding="utf-8") as file:

            reader = csv.DictReader(file)

            for row in reader:

                if row["activo"] != "1":
                    continue

                accounts.append(row)

        return accounts