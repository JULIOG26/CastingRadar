from .engine import InstagramEngineV2


def main():

    print()
    print("=" * 60)
    print("TEST INSTAGRAM V2")
    print("=" * 60)

    usuario = input(
        "Usuario Instagram (ENTER = todas): "
    ).strip()

    engine = InstagramEngineV2()

    if usuario:

        resultados = engine.scrape(usuario=usuario)

    else:

        resultados = engine.scrape()

    print()
    print("=" * 60)
    print(f"CASTINGS EXTRAÍDOS: {len(resultados)}")
    print("=" * 60)


if __name__ == "__main__":
    main()