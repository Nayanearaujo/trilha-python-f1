# Arquitetura

O projeto segue uma arquitetura em **camadas**, cada uma com uma unica
responsabilidade. As camadas de cima dependem das de baixo, nunca o contrario.

```
dashboard (Streamlit / UI)
      |
   services  (regra de negocio)
      |
 repositories (abstrai a fonte de dados)
      |
  openf1_client (endpoints da OpenF1)
      |
   http_client  (transporte HTTP generico)
```

## Camadas

| Camada          | Modulo                         | Responsabilidade                                   |
|-----------------|--------------------------------|----------------------------------------------------|
| Apresentacao    | `dashboard.py`                 | UI em abas, filtros e graficos (Plotly).           |
| Servico         | `domain/services.py`           | Orquestra repositorio + processamento.             |
| Repositorio     | `domain/repositories.py`       | Contrato de acesso a dados (`Protocol`) + OpenF1.  |
| Cliente API     | `ingestion/openf1_client.py`   | Conhece os endpoints da OpenF1.                    |
| Transporte      | `ingestion/http_client.py`     | GET generico com retry/timeout (usa `requests`).   |
| Processamento   | `processing/laps.py`           | Funcoes puras: filtrar, ordenar, agregar.          |
| Modelos         | `domain/models.py`             | Entidades Pydantic (Session, Lap, Driver, ...).    |
| Utilidades      | `utils/config.py`, `logger.py` | Configuracao (via `.env`) e logging.               |

## Por que separar `http_client` de `openf1_client`?

- `http_client` nao sabe nada sobre F1: da para reusar com qualquer API.
- `openf1_client` nao sabe nada sobre HTTP baixo nivel: so monta URLs e valida.
- Testar fica simples: injeta-se uma `Session` falsa no `http_client` e um
  repositorio falso no `services`.

## Fluxo de uma analise

1. Usuario escolhe temporada -> continente -> pais no `dashboard`.
2. `F1Service` pede ao `OpenF1Repository` as `sessions`, `laps` e `drivers`.
3. `processing.laps` filtra voltas validas e agrega por piloto/equipe.
4. `services` monta os modelos de saida (FastestLap, DriverStats, TeamStats).
5. O `dashboard` renderiza tabelas + graficos Plotly em abas.
