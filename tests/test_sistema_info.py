# test_sistema_info.py

"""Testes para SistemaInfo, coletar_sistema e gerar_relatorio"""

import json
from pathlib import Path

from pytest import MonkeyPatch

from src.sistema_info import SistemaInfo, coletar_sistema, gerar_relatorio


# =====================================================
# Coleta
# =====================================================


def test_sistema_info_e_coleta(
    sistema_parametrizado: SistemaInfo,
) -> None:
    """Testa criação de SistemaInfo e coleta de dados básicos."""

    assert sistema_parametrizado.nome_sistema in ["Linux", "Windows", "Darwin"]

    if sistema_parametrizado.nome_sistema == "Windows":
        variaveis_windows: dict[str, str] | str | None = (
            sistema_parametrizado.variaveis_windows
        )
        assert variaveis_windows["USERPROFILE"] is not None
        assert variaveis_windows["USERPROFILE"] == "C:\\Users\\Test"
        assert variaveis_windows["HOMEDRIVE"] == "C:"
        assert variaveis_windows["HOMEPATH"] == "\\Users\\Test"

    if sistema_parametrizado.nome_sistema == "Linux":
        assert sistema_parametrizado.distribuicao == "Ubuntu 22.04"

    if sistema_parametrizado.nome_sistema == "Darwin":
        assert sistema_parametrizado.versao_macos == "14.0"

    assert sistema_parametrizado.nome_computador == "TestMachine"
    assert sistema_parametrizado.python_versao == "3.11.0"
    assert sistema_parametrizado.arquitetura == "x86_64"
    assert sistema_parametrizado.user_admin.exists()


# ======================================================
# Instanciação
# ======================================================


def test_instancia_criada(
    sistema_parametrizado: SistemaInfo,
) -> None:
    """Verifica criação básica da instância"""

    sistema: SistemaInfo = sistema_parametrizado

    assert sistema.nome_sistema in ["Linux", "Windows", "Darwin"]
    assert sistema.nome_computador == "TestMachine"
    assert sistema.python_versao == "3.11.0"
    assert sistema.arquitetura == "x86_64"
    assert sistema.user_admin.exists()


def test_to_dict_nao_tem_valores_vazios(
    sistema_parametrizado: SistemaInfo,
) -> None:
    """Garante que to_dict não retorna valores vazios"""

    info: dict[str, str | dict[str, str]] = sistema_parametrizado.to_dict()

    for valor in info.values():
        assert valor not in ("", {}, None)


# ======================================================
# Relatório
# ======================================================


def test_gerar_relatorio(
    sistema_parametrizado: SistemaInfo,
    tmp_path: Path,
) -> None:
    """Verifica geração do relatório JSON"""

    relatorio: dict[str, str | dict[str, str]] = gerar_relatorio(
        sistema=sistema_parametrizado,
        output_dir=tmp_path,
    )

    arquivos: list[Path] = list(tmp_path.glob("relatorio_*.json"))
    assert len(arquivos) == 1

    with open(arquivos[0], encoding="utf-8") as f:
        data = json.load(f)

    assert data == relatorio


def test_gerar_relatorio_sem_output_dir(
    sistema_parametrizado: SistemaInfo,
    monkeypatch: MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Testa geração usando Path.cwd()"""

    monkeypatch.setattr("pathlib.Path.cwd", lambda: tmp_path)

    gerar_relatorio(sistema_parametrizado)

    arquivos: list[Path] = list(tmp_path.glob("relatorio_*.json"))
    assert len(arquivos) == 1


# ======================================================
# Casos específicos extras (branches)
# ======================================================


def test_linux_sem_os_release(
    monkeypatch: MonkeyPatch,
    fake_home: Path,
) -> None:
    """Linux sem arquivo /etc/os-release"""

    monkeypatch.setattr("platform.system", lambda: "Linux")
    monkeypatch.setattr("platform.release", lambda: "1.0")
    monkeypatch.setattr("platform.machine", lambda: "x86_64")
    monkeypatch.setattr("platform.node", lambda: "TestMachine")
    monkeypatch.setattr("platform.python_version", lambda: "3.11.0")
    monkeypatch.setattr("pathlib.Path.home", lambda: fake_home)

    monkeypatch.setattr("os.path.exists", lambda x: False)

    sistema: SistemaInfo = coletar_sistema()

    assert sistema.distribuicao == "Distribuição desconhecida"


def test_macos_sem_versao(
    monkeypatch: MonkeyPatch,
    fake_home: Path,
) -> None:
    """macOS sem versão retornada"""

    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr("platform.release", lambda: "1.0")
    monkeypatch.setattr("platform.machine", lambda: "x86_64")
    monkeypatch.setattr("platform.node", lambda: "TestMachine")
    monkeypatch.setattr("platform.python_version", lambda: "3.11.0")
    monkeypatch.setattr("pathlib.Path.home", lambda: fake_home)

    monkeypatch.setattr("platform.mac_ver", lambda: ("", ("", "", ""), ""))

    sistema: SistemaInfo = coletar_sistema()

    assert sistema.versao_macos == "Versão desconhecida"
