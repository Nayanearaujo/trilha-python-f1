"""Logger padrao do projeto."""

from __future__ import annotations

import logging


def get_logger(name: str = "f1") -> logging.Logger:
    """Retorna um logger configurado com saida no console.

    Evita adicionar handlers duplicados quando chamado varias vezes.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
