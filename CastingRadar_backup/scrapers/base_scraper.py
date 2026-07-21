from playwright.sync_api import sync_playwright


class Browser:

    def __init__(self):
        self.playwright = None
        self.context = None
        self.page = None

    def start(self):

        self.playwright = sync_playwright().start()

        self.context = self.playwright.chromium.launch_persistent_context(
            user_data_dir="data/chrome_profile",
            headless=False
        )

        self.page = self.context.new_page()

        
        self.page.on("request", lambda r: print("REQ:", r.url))
        self.page.on("response", lambda r: print("RES:", r.status, r.url))

    def _on_response(self, response):

        if "graphql" in response.url:
            print("\n========================")
            print(response.status)
            print(response.url)

    def stop(self):

        self.context.close()
        self.playwright.stop()