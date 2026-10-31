# Trilha Python F1 🏎️

Dashboard de Formula 1 que lista as **5 voltas mais rapidas por circuito**,
consumindo dados em tempo real da [OpenF1 API](https://openf1.org/).

Projeto final da trilha de boas praticas de Python: ambiente com Poetry,
codigo modular, lint/format com ruff, testes com pytest, documentacao com
MkDocs Material e CI no GitHub Actions.

## Funcionalidades

- Escolha de ano e pais (circuito).
- Lista das 5 (ou N) voltas mais rapidas da sessao.
- Nome do piloto, equipe, numero da volta e tempo formatado (ex.: `1:32.608`).
- Grafico comparando os tempos.

## Requisitos

- Python >= 3.11
- Poetry

## Instalacao

```bash
poetry install --with dev
```

## Rodar o dashboard

```bash
poetry run streamlit run src/f1/dashboard.py
```

## Comandos uteis (tasks do poe)

```bash
poetry run poe lint      # ruff check
poetry run poe format    # ruff format
poetry run poe test      # pytest + cobertura
poetry run poe docs      # mkdocs serve
```

## Arquitetura

| Camada       | Responsabilidade                                  |
|--------------|---------------------------------------------------|
| `ingestion`  | Cliente HTTP da OpenF1.                            |
| `domain`     | Modelos (Pydantic) e regra de negocio.            |
| `processing` | Filtro e ordenacao das voltas (funcoes puras).    |
| `utils`      | Configuracao e logger.                            |
| `dashboard`  | Interface Streamlit (orquestracao).               |

Veja o resumo da API em [API OpenF1](API.md).
