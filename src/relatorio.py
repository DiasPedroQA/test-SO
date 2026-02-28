"""
Módulo responsável por gerar relatório JSON do sistema.
"""

import json
import platform
from pathlib import Path

from src.sistema_info import SistemaInfo


def gerar_relatorio(output_dir: Path | None = None) -> dict[str, str | dict[str, str]]:
    """
    Gera relatório do sistema e salva em JSON.

    Args:
        output_dir: Diretório onde o arquivo será salvo (opcional)

    Returns:
        dict com dados do relatório
    """

    sistema = SistemaInfo()
    # info: dict = sistema.to_dict()
    sistema_atual: str = platform.system()

    relatorio: dict[str, str | dict[str, str]] = {
        "so": sistema_atual,
        "hostname": sistema.nome_computador,
        "python": sistema.python_versao,
        "arquitetura": sistema.arquitetura,
        "home_path": str(sistema.user_admin),
        "status": "PASSOU" if sistema.nome_sistema == sistema_atual else "FALHOU",
    }

    if sistema.distribuicao:
        relatorio["distribuicao"] = sistema.distribuicao

    if sistema.versao_macos:
        relatorio["versao_macos"] = sistema.versao_macos

    if sistema.variaveis_windows:
        relatorio["variaveis_windows"] = sistema.variaveis_windows

    # Diretório padrão = atual
    if output_dir is None:
        output_dir = Path.cwd()

    filename: Path = output_dir / f"relatorio_{sistema_atual}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(relatorio, f, indent=2, ensure_ascii=False)

    return relatorio
