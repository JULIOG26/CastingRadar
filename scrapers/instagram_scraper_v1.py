from pathlib import Path
import csv

from playwright.sync_api import sync_playwright


class InstagramScraper:

    def scrape(self):

        fichero = Path("data/instagram_accounts.csv")

        with open(fichero, newline="", encoding="utf-8") as f:
            cuentas = list(csv.DictReader(f))

        with sync_playwright() as p:

            context = p.chromium.launch_persistent_context(
                user_data_dir="data/chrome_profile",
                headless=False
            )

            page = context.new_page()

            for cuenta in cuentas[:1]:

                usuario = cuenta["usuario"]

                print(f"\n===== {usuario} =====")

                page.goto(
                    f"https://www.instagram.com/{usuario}/",
                    wait_until="networkidle"
                )

                print("URL:", page.url)
                print("Título:", page.title())

                input("Pulsa ENTER cuando hayas visto la ventana del navegador...")

            context.close()

        return []