"""Configuracao central do projeto.

As variaveis sao lidas do ambiente. Em desenvolvimento, carregamos um
arquivo `.env` (nunca commitado) com o python-dotenv para isolar valores
sensiveis, como chaves de API. No projeto a OpenF1 e aberta, mas o padrao
fica pronto para APIs que exijam credenciais.
"""

from __future__ import annotations

import os

from dotenv import load_dotenv

# Carrega variaveis do .env (se existir) para o ambiente.
load_dotenv()

# Base URL da OpenF1 (pode ser sobrescrita por variavel de ambiente)
OPENF1_BASE_URL: str = os.getenv("OPENF1_BASE_URL", "https://api.openf1.org/v1")

# Timeout padrao das requisicoes HTTP, em segundos
REQUEST_TIMEOUT: int = int(os.getenv("OPENF1_TIMEOUT", "10"))

# Quantidade de voltas mais rapidas exibidas
TOP_N_LAPS: int = int(os.getenv("F1_TOP_N_LAPS", "5"))

# Exemplo de chave de API isolada via .env (opcional; a OpenF1 publica nao exige)
OPENF1_API_KEY: str | None = os.getenv("OPENF1_API_KEY")
