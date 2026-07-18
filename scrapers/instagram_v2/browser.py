from playwright.sync_api import sync_playwright


class Browser:

    def __init__(self):

        self.playwright = None
        self.context = None
        self.page = None

    def start(self):

        self.playwright = sync_playwright().start()

        self.context = self.playwright.chromium.launch_persistent_context(
            user_data_dir="data/chrome_profile_v2",
            headless=False,
            viewport={"width": 1400, "height": 1000},
        )

        pages = self.context.pages

        if pages:
            self.page = pages[0]
        else:
            self.page = self.context.new_page()

        self.page.set_default_timeout(30000)

    def stop(self):

        if self.context:
            self.context.close()

        if self.playwright:
            self.playwright.stop()