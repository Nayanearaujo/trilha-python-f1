# Trilha Python F1 🏎️

Dashboard de **Formula 1** que lista as **5 voltas mais rapidas por circuito**,
consumindo dados em tempo real da [OpenF1 API](https://openf1.org/).

Este e o projeto final da trilha de boas praticas de Python. Ele foi construido
seguindo o `skill.md` (padrao de engenharia) e o `plan.md` (plano de implementacao),
exatamente o fluxo ensinado na trilha: Poetry, codigo modular, ruff, pytest,
MkDocs e CI/CD no GitHub.

## Stack

- **Python 3.12** (ambiente via Poetry)
- **Streamlit** - interface web
- **Pydantic v2** - modelagem/validacao
- **requests** - consumo da OpenF1 API
- **pandas** - normalizacao/transformacao dos dados
- **plotly** - graficos interativos
- **python-dotenv** - isolamento de chaves via `.env`
- **pytest + pytest-cov** - testes (cobertura minima 50%)
- **ruff** - lint, format e organizacao de imports
- **mkdocs-material** - documentacao
- **GitHub Actions** - CI (lint, testes, build e deploy da doc)

## Estrutura

```
src/f1/
  dashboard.py          # app Streamlit (orquestracao)
  ingestion/            # cliente HTTP da OpenF1
  domain/               # models (Pydantic) e services (regra de negocio)
  processing/           # filtro/ordenacao das voltas (funcoes puras)
  utils/                # config e logger
tests/unit/             # testes unitarios (API mockada)
scripts/                # scripts auxiliares (health-check da API)
docs/                   # documentacao (mkdocs-material)
.github/workflows/      # pipeline de CI
```

## Como rodar

```bash
# 1. instalar dependencias
poetry install --with dev

# 2. rodar o dashboard
poetry run streamlit run src/f1/dashboard.py

# 3. rodar os testes com cobertura
poetry run pytest

# 4. lint e format
poetry run ruff check .
poetry run ruff format .

# 5. documentacao
poetry run mkdocs serve        # local
poetry run mkdocs gh-deploy    # publica no GitHub Pages
```

## Boas praticas aplicadas

- Ambiente isolado e gerenciado com **Poetry** (nunca `pip` direto).
- Projeto **modular**: cada camada com uma responsabilidade.
- **ruff** garantindo PEP 8 e imports organizados.
- **pytest** com cobertura e API mockada.
- **.env** fora do versionamento (`.gitignore` + `.env.example`).
- **CI** que barra codigo fora do padrao antes do merge.
- **pre-commit** rodando lint/format antes de cada commit.

## Fluxo de Git usado

Branch `dev` -> commits -> `git push` -> Pull Request -> merge na `main`.

## Licenca

MIT.
