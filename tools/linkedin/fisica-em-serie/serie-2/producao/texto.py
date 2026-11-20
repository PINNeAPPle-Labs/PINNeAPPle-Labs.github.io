"""Formatação dos documentos gerados.

O material da série é em português, e número em português usa vírgula decimal. Os documentos são
montados com f-strings (que escrevem ponto) e convertidos aqui, num lugar só, para que a regra
não dependa de lembrar dela em cada episódio.
"""

from __future__ import annotations

import re

_DECIMAL = re.compile(r"(?<=\d)\.(?=\d)")


def virgula(texto: str) -> str:
    """Troca o ponto decimal por vírgula, sem tocar em nomes de arquivo nem em versões."""
    return _DECIMAL.sub(",", texto)
