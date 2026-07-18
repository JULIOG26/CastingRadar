from pathlib import Path
import csv


class AccountLoader:

    def __init__(self, csv_file="data/instagram_accounts.csv"):
        self.csv_file = Path(csv_file)

    def load(self):

        with open(self.csv_file, newline="", encoding="utf-8") as f:

            return list(csv.DictReader(f))