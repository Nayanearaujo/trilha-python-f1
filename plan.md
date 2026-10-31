# plan.md - Plano de implementacao

Plano gerado a partir de `docs/API.md` + `skill.md`. Descreve a estrutura de
diretorios, as camadas e os artefatos do projeto.

## Objetivo

Dashboard em Python (Streamlit) que lista as **5 voltas mais rapidas por circuito**,
consumindo dados da **OpenF1 API**, seguindo as boas praticas do `skill.md`.

## Estrutura de diretorios

```
trilha-python-f1/
├── src/f1/
│   ├── __init__.py
│   ├── dashboard.py            # app Streamlit (orquestracao / UI)
│   ├── ingestion/
│   │   ├── __init__.py
│   │   └── openf1_client.py    # cliente HTTP da OpenF1
│   ├── domain/
│   │   ├── __init__.py
│   │   ├── models.py           # modelos Pydantic (Session, Lap, Driver, FastestLap)
│   │   └── services.py         # regra de negocio (5 voltas mais rapidas)
│   ├── processing/
│   │   ├── __init__.py
│   │   └── laps.py             # ordenar / filtrar / selecionar voltas
│   └── utils/
│       ├── __init__.py
│       ├── config.py           # constantes e configuracao
│       └── logger.py           # logger padrao
├── tests/
│   └── unit/
│       ├── __init__.py
│       ├── test_processing.py
│       └── test_services.py
├── scripts/
│   └── verificar_api.py        # health-check da API
├── docs/
│   ├── index.md
│   └── API.md
├── skill.md
├── plan.md
├── mkdocs.yml
├── pyproject.toml
├── .python-version
├── .gitignore
└── README.md
```

## Camadas de responsabilidade

| Camada       | Papel                                               |
|--------------|-----------------------------------------------------|
| `ingestion`  | Fala com a API externa, devolve JSON/bruto.         |
| `domain`     | Modela os dados (Pydantic) e aplica a regra.        |
| `processing` | Funcoes puras de filtro/ordenacao das voltas.       |
| `utils`      | Config e logger.                                    |
| `dashboard`  | So orquestra e apresenta (Streamlit).               |

## Fluxo

1. Usuario escolhe ano + pais no dashboard.
2. `OpenF1Client` busca `sessions`, `laps` e `drivers`.
3. `processing.laps` filtra voltas validas e ordena por duracao.
4. `domain.services` monta as 5 `FastestLap` cruzando com os pilotos.
5. `dashboard` exibe tabela + grafico.

## Qualidade

- `ruff` para lint/format.
- `pytest` com cobertura >= 50% (funcoes de `processing` e `services`, com API mockada).
- `mkdocs-material` para a doc, deploy no GitHub Pages.
