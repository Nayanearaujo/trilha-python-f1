# Trilha Python F1 🏎️📊

Dashboard interativo para **explorar dados da Formula 1**, consumindo a
[OpenF1 API](https://openf1.org/). Analise temporadas e circuitos com filtros
encadeados (continente → pais) e visualizacoes dinamicas em Plotly.

Projeto final da trilha de boas praticas de Python, construido seguindo o
`skill.md` (padrao de engenharia) e o `plan.md` (plano): Poetry, codigo modular
em camadas, ruff, pytest, MkDocs e CI/CD no GitHub.

## ✨ Funcionalidades

- 🏁 **Corridas** — GPs da temporada e distribuicao por continente (grafico de pizza).
- ⏱️ **Voltas** — as 5 (ou N) voltas mais rapidas, com tempos formatados (`1:32.608`).
- 👤 **Pilotos** — melhor volta e media por piloto (grafico de barras horizontal).
- 👥 **Equipes** — comparativo de desempenho entre equipes.
- 📊 **Resumo geral** — dispersao consistencia × velocidade por piloto.
- 🔎 **Filtros encadeados** na barra lateral: temporada → continente → pais/circuito.

## 🛠️ Stack

| Camada | Ferramentas |
|---|---|
| Interface | Streamlit + Plotly |
| Dados | requests, Pydantic v2, Pandas |
| Config/segredos | python-dotenv (`.env`) |
| Qualidade | ruff (lint/format), pytest + pytest-cov |
| Docs | mkdocs-material (GitHub Pages) |
| Infra | Poetry, GitHub Actions (CI/CD), pre-commit |

## 🏗️ Arquitetura (em camadas)

```
dashboard  ->  services  ->  repositories  ->  openf1_client  ->  http_client
   (UI)       (regra)        (fonte dados)      (endpoints)       (HTTP generico)
```

```
src/f1/
  dashboard.py            # app Streamlit (abas + filtros + graficos)
  ingestion/
    http_client.py        # GET generico com retry/timeout
    openf1_client.py      # endpoints da OpenF1
  domain/
    models.py             # entidades Pydantic
    repositories.py       # contrato (Protocol) + OpenF1Repository
    services.py           # regra de negocio
  processing/
    laps.py               # funcoes puras: filtrar/ordenar/agregar
  utils/
    config.py, logger.py
tests/
  unit/                   # testes com API mockada
  integration/            # teste real opt-in (RUN_INTEGRATION=1)
docs/                     # architecture, development, API, index
.github/workflows/        # pipeline de CI/CD
```

## 🚀 Como rodar

```bash
poetry install --with dev
poetry run streamlit run src/f1/dashboard.py   # dashboard
poetry run pytest                              # testes + cobertura
poetry run ruff check . && poetry run ruff format .
poetry run mkdocs serve                        # doc local
poetry run mkdocs gh-deploy                    # publica no GitHub Pages
```

Atalhos (poe): `poetry run poe lint | format | test | docs | dashboard`.

## 🧪 Testes

- Unitarios rodam sempre (API mockada, repositorio fake).
- Integracao real so com `RUN_INTEGRATION=1 poetry run pytest tests/integration`.

## 📄 Documentacao

Publicada via GitHub Pages: **https://nayanearaujo.github.io/trilha-python-f1/**

## 🙏 Creditos

Projeto da trilha de Python (EmpregaDados / Anhanguera, instrutor Carlos Oliveira).
Evolucao do dashboard inspirada em funcionalidades vistas em projetos de colegas
da turma; todo o codigo deste repositorio e autoral.

## Licenca

MIT.
