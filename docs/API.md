# OpenF1 API - Resumo

Documentacao resumida da [OpenF1 API](https://openf1.org/) gerada para orientar o
desenvolvimento do projeto. A OpenF1 fornece dados de Formula 1 (sessoes, pilotos,
voltas, tempos) em formato JSON.

## Autenticacao

- **Dados historicos / endpoints publicos**: nao exigem autenticacao.
- **Acesso em tempo real (streaming)**: requer assinatura paga.
- Para este projeto usamos apenas endpoints publicos, sem chave de API.

## Limites de uso

- 3 requests por segundo.
- ~30 requests por minuto.
- Mais do que suficiente para o dashboard.

## Base URL

```
https://api.openf1.org/v1
```

## Endpoints usados no projeto

### `GET /sessions`
Lista as sessoes (corrida, qualifying, treinos) de um ano/pais.

Parametros uteis:
- `year` (ex.: `2024`)
- `country_name` (ex.: `Brazil`)
- `session_name` (ex.: `Race`, `Qualifying`)

Campos relevantes: `session_key`, `session_name`, `country_name`,
`circuit_short_name`, `year`, `date_start`.

### `GET /laps`
Retorna as voltas de uma sessao.

Parametros uteis:
- `session_key` (obrigatorio na pratica)
- `driver_number` (opcional, filtra por piloto)

Campos relevantes: `driver_number`, `lap_number`, `lap_duration`,
`date_start`, `is_pit_out_lap`.

### `GET /drivers`
Retorna os pilotos de uma sessao (para cruzar `driver_number` -> nome).

Parametros uteis:
- `session_key`

Campos relevantes: `driver_number`, `full_name`, `name_acronym`, `team_name`.

## Regra de negocio do projeto

Dado um ano + pais (circuito):
1. buscar a `session_key` da sessao escolhida;
2. buscar as `laps` daquela sessao;
3. descartar voltas invalidas (`lap_duration` nula ou volta de pit out);
4. ordenar por `lap_duration` e pegar as 5 mais rapidas;
5. cruzar com `drivers` para exibir o nome do piloto.
