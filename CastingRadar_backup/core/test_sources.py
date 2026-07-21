from core.source_manager import SourceManager

manager = SourceManager()

accounts = manager.load_instagram_accounts()

print(f"{len(accounts)} cuentas cargadas\n")

for account in accounts:
    print(
        f'{account["usuario"]} | '
        f'{account["categoria"]} | '
        f'Prioridad {account["prioridad"]} | '
        f'Senior {account["senior"]}'
    )