from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    context = p.chromium.launch_persistent_context(
        user_data_dir="data/chrome_profile",
        headless=False
    )

    page = context.new_page()

    page.goto("https://www.instagram.com")

    print("Tómate todo el tiempo que necesites...")
    input("Cuando ya estés conectado a Instagram, pulsa ENTER aquí.")

    context.close()