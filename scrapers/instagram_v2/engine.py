from .browser import Browser
from .account_loader import AccountLoader
from .post_parser import PostParser


class InstagramEngineV2:

    def __init__(self):
        self.browser = None
        self.parser = PostParser()
        self.resultados = []

    def scrape(self, max_cuentas=None, usuario=None):

        cuentas = AccountLoader().load()

        print(f"\n{len(cuentas)} cuentas cargadas")

        if usuario:
            cuentas = [
                c for c in cuentas
                if c["usuario"].lower() == usuario.lower()
            ]

        elif max_cuentas:
            cuentas = cuentas[:max_cuentas]

        if not cuentas:
            print("No hay cuentas para revisar")
            return []

        self.browser = Browser()
        self.browser.start()

        try:

            total = len(cuentas)

            for indice, cuenta in enumerate(cuentas, start=1):

                usuario_actual = cuenta["usuario"]

                print("\n" + "=" * 70)
                print(f"[{indice}/{total}] {usuario_actual}")
                print("=" * 70)

                try:

                    castings = self._procesar_cuenta(usuario_actual)

                    self.resultados.extend(castings)

                    print(f"Castings encontrados: {len(castings)}")

                except Exception as e:

                    print(f"ERROR en {usuario_actual}: {e}")

            print("\n" + "=" * 70)
            print(f"TOTAL CASTINGS: {len(self.resultados)}")
            print("=" * 70)

            return self.resultados

        finally:

            self.browser.stop()

    def _procesar_cuenta(self, usuario):

        pagina = self.browser.page

        pagina.goto(
            f"https://www.instagram.com/{usuario}/",
            wait_until="domcontentloaded"
        )

        pagina.wait_for_load_state("networkidle")
        pagina.wait_for_timeout(2000)

        try:

            pagina.wait_for_selector(
                "a[href*='/p/']",
                timeout=8000
            )

        except Exception:

            print("Sin publicaciones visibles")
            return []

        enlaces = pagina.locator("a[href*='/p/']")

        total_posts = enlaces.count()

        print(f"Posts encontrados: {total_posts}")

        urls = []

        for i in range(min(total_posts, 5)):

            href = enlaces.nth(i).get_attribute("href")

            if href:
                urls.append(
                    "https://www.instagram.com" + href
                )

        resultados = []

        for url in urls:

            casting = self._leer_post(usuario, url)

            if casting is None:
                continue

            resultados.append(casting)

            print(
                f"✓ {casting.empresa} | "
                f"{casting.ciudad} | "
                f"{casting.titulo}"
            )

        return resultados

    def _leer_post(self, usuario, url):

        pagina = self.browser.page

        pagina.goto(
            url,
            wait_until="domcontentloaded"
        )

        pagina.wait_for_load_state("networkidle")
        pagina.wait_for_timeout(1500)

        descripcion = (
            pagina.locator(
                'meta[property="og:description"]'
            )
            .first
            .get_attribute("content")
        )

        if not descripcion:
            return None

        try:

            casting = self.parser.parse(
                usuario,
                url,
                descripcion
            )

            return casting

        except Exception as e:

            print(f"Error parseando publicación: {e}")
            return None
        