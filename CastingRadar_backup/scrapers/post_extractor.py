class PostExtractor:

    def __init__(self, browser):

        self.browser = browser

        self.posts = []

        self.browser.context.on("response", self.on_response)

    def on_response(self, response):

        url = response.url.lower()

        if "graphql" in url or "api/graphql" in url:

            print("\n==============================")
            print("STATUS:", response.status)
            print("URL:", response.url)

            try:
                datos = response.json()

                self.posts.append(datos)

                print("JSON recibido")

            except Exception:
                pass

    def extract(self, usuario):

        self.posts = []

        self.browser.page.goto(
            f"https://www.instagram.com/{usuario}/",
            wait_until="domcontentloaded"
        )

        self.browser.page.wait_for_timeout(8000)

        return self.posts