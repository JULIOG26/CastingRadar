class PostExtractor:

    def __init__(self, page):
        self.page = page

    def get_posts(self):

        enlaces = self.page.locator("a[href*='/p/']").all()

        print(f"Posts encontrados: {len(enlaces)}")

        return enlaces