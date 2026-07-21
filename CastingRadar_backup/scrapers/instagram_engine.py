from scrapers.browser import Browser
from scrapers.post_extractor import PostExtractor
from scrapers.account_loader import AccountLoader


class InstagramEngine:

    def scrape(self):

        cuentas = AccountLoader().load()

        print(f"{len(cuentas)} cuentas cargadas")

        browser = Browser()

        browser.start()

        extractor = PostExtractor(browser)

        try:

            for cuenta in cuentas[:1]:

                print(f"\n===== {cuenta['usuario']} =====")

                posts = extractor.extract(cuenta["usuario"])

                print(f"Posts encontrados: {len(posts)}")

        finally:

            browser.stop()

        return []