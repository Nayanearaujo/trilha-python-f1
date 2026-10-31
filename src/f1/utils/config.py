"""Configuracao central do projeto."""

from __future__ import annotations

import os

# Base URL da OpenF1 (pode ser sobrescrita por variavel de ambiente)
OPENF1_BASE_URL: str = os.getenv("OPENF1_BASE_URL", "https://api.openf1.org/v1")

# Timeout padrao das requisicoes HTTP, em segundos
REQUEST_TIMEOUT: int = int(os.getenv("OPENF1_TIMEOUT", "10"))

# Quantidade de voltas mais rapidas exibidas
TOP_N_LAPS: int = int(os.getenv("F1_TOP_N_LAPS", "5"))
