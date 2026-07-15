import csv
from pathlib import Path


class InstagramScraper:

    def __init__(self):
        self.accounts = []

    def scrape(self):

        fichero = Path("data/instagram_accounts.csv")

        with open(fichero, newline="", encoding="utf-8") as f:

            reader = csv.DictReader(f)

            for fila in reader:
                self.accounts.append(fila)

        return self.accounts