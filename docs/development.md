# Desenvolvimento

## Setup

```bash
poetry install --with dev
poetry run pre-commit install   # opcional: roda ruff antes de cada commit
```

## Comandos (tasks do poe)

```bash
poetry run poe lint        # ruff check
poetry run poe format      # ruff format
poetry run poe test        # pytest + cobertura (minimo 50%)
poetry run poe docs        # mkdocs serve (doc local)
poetry run poe dashboard   # streamlit run
```

## Testes

- **Unitarios** (`tests/unit/`): rodam sempre, com a API mockada.
- **Integracao** (`tests/integration/`): batem na OpenF1 de verdade; so rodam
  com `RUN_INTEGRATION=1`:

```bash
RUN_INTEGRATION=1 poetry run pytest tests/integration
```

## Qualidade

- `ruff` cuida de lint, format e organizacao de imports (PEP 8).
- Cobertura minima de 50% imposta pelo `--cov-fail-under=50`.
- O CI (GitHub Actions) roda lint + testes + build/deploy da doc a cada push.

## Variaveis de ambiente

Copie `.env.example` para `.env` e ajuste se necessario (a OpenF1 publica nao
exige chave). O `.env` nunca e commitado.
