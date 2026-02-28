"""Módulo de teste para verificar as informações específicas de cada sistema operacional"""

import platform
from src.sistema_info import SistemaInfo


def test_info_especifica_por_so() -> None:
    """Teste para verificar se as informações específicas,
    de cada sistema operacional são carregadas corretamente"""
    sistema = SistemaInfo()
    so: str = platform.system()

    if so == "Linux":
        assert sistema.distribuicao is not None

    elif so == "Windows":
        assert sistema.variaveis_windows is not None

    elif so == "Darwin":
        assert sistema.versao_macos is not None
