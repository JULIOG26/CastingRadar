from scrapers.instagram_engine import InstagramEngine


class InstagramScraper:

    def scrape(self):
        engine = InstagramEngine()
        return engine.scrape()