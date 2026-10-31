"""Script auxiliar: verifica se a OpenF1 API esta online.

Rode com:  poetry run python scripts/verificar_api.py
"""

from __future__ import annotations

import requests

URL = "https://api.openf1.org/v1/sessions?year=2024"


def verificar_api() -> None:
    """Faz uma requisicao simples e reporta o status da API."""
    try:
        response = requests.get(URL, timeout=5)
        response.raise_for_status()
    except requests.Timeout:
        print("API offline: tempo de resposta excedido (timeout).")
    except requests.RequestException as exc:
        print(f"API deu falha na conexao: {exc}")
    else:
        print(f"API esta online - Status: {response.status_code}")


if __name__ == "__main__":
    verificar_api()
