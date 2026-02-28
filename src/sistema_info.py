# pylint: disable=too-many-instance-attributes

"""
Módulo responsável por coletar informações do sistema operacional
e gerar relatórios JSON com base nesses dados.
"""

import json
import os
import platform
from pathlib import Path
from dataclasses import dataclass, asdict, field


# =====================================================
# Modelo
# =====================================================


@dataclass(slots=True)
class SistemaInfo:
    """Armazena informações do sistema operacional e ambiente Python."""

    nome_sistema: str
    versao_sistema: str
    arquitetura: str
    nome_computador: str
    user_admin: Path
    python_versao: str
    distribuicao: str | None = None
    versao_macos: str | None = None
    variaveis_windows: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, str | dict[str, str]]:
        """
        Retorna um dicionário serializável em JSON,
        omitindo valores None.
        """
        data: dict[str, str | dict[str, str]] = asdict(self)

        # Converter Path para string
        for key, value in data.items():
            if isinstance(value, Path):
                data[key] = str(value)

        # Remover valores None
        return {k: v for k, v in data.items() if v is not None}


# =====================================================
# Coleta
# =====================================================


def coletar_sistema() -> SistemaInfo:
    """
    Coleta informações do sistema operacional atual
    e retorna uma instância de SistemaInfo.
    """

    nome: str = platform.system()
    versao: str = platform.release()
    arquitetura: str = platform.machine()
    hostname: str = platform.node()
    home: Path = Path.home()
    python_version: str = platform.python_version()

    distribuicao: str | None = None
    versao_macos: str | None = None
    variaveis_windows: dict[str, str] = {}

    if nome == "Windows":
        variaveis_windows = {
            "USERPROFILE": os.environ.get("USERPROFILE", "Desconhecido"),
            "HOMEDRIVE": os.environ.get("HOMEDRIVE", "Desconhecido"),
            "HOMEPATH": os.environ.get("HOMEPATH", "Desconhecido"),
        }

    elif nome == "Linux":
        try:
            if os.path.exists("/etc/os-release"):
                os_release: dict[str, str] = platform.freedesktop_os_release()
                distribuicao = os_release.get("PRETTY_NAME", "Desconhecido")
            else:
                distribuicao = "Distribuição desconhecida"
        except (ValueError, KeyError, OSError):
            distribuicao = "Não foi possível identificar"

    elif nome == "Darwin":
        mac_ver: tuple[str, tuple[str, str, str], str] = platform.mac_ver()
        versao_macos = mac_ver[0] if mac_ver and mac_ver[0] else "Versão desconhecida"

    return SistemaInfo(
        nome_sistema=nome,
        versao_sistema=versao,
        arquitetura=arquitetura,
        nome_computador=hostname,
        user_admin=home,
        python_versao=python_version,
        distribuicao=distribuicao,
        versao_macos=versao_macos,
        variaveis_windows=variaveis_windows,
    )


# =====================================================
# Relatório
# =====================================================


def gerar_relatorio(
    sistema: SistemaInfo,
    output_dir: Path | None = None,
) -> dict[str, str | dict[str, str]]:
    """
    Gera um relatório JSON com as informações do sistema.

    Args:
        sistema: Instância de SistemaInfo.
        output_dir: Diretório onde salvar o relatório.

    Returns:
        Dicionário com os dados exportados.
    """

    if output_dir is None:
        output_dir = Path.cwd()

    relatorio: dict[str, str | dict[str, str]] = sistema.to_dict()
    filename: Path = output_dir / f"relatorio_{sistema.nome_sistema}.json"

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(relatorio, file, indent=4, ensure_ascii=False)

    return relatorio
