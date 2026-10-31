# Trilha Python F1 🏎️

Dashboard interativo para **explorar dados da Formula 1**, consumindo a
[OpenF1 API](https://openf1.org/). Permite analisar temporadas e circuitos com
filtros encadeados (continente, pais) e visualizacoes dinamicas.

## O que o dashboard oferece

- 🏁 **Corridas**: GPs da temporada e distribuicao por continente.
- ⏱️ **Voltas**: as voltas mais rapidas da sessao, com tempos formatados.
- 👤 **Pilotos**: melhor volta e media por piloto.
- 👥 **Equipes**: comparativo de desempenho entre equipes.
- 📊 **Resumo geral**: consistencia x velocidade (dispersao).

## Tecnologias

Python, Streamlit, Plotly, Pandas, Pydantic, requests, python-dotenv, Poetry,
pytest, ruff, MkDocs Material e GitHub Actions (CI/CD).

## Como rodar

```bash
poetry install --with dev
poetry run streamlit run src/f1/dashboard.py
```

## Navegacao

- [Arquitetura](architecture.md) - as camadas do projeto.
- [Desenvolvimento](development.md) - setup, testes e tasks.
- [API OpenF1](API.md) - resumo dos endpoints usados.
