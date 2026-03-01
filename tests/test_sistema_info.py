"""
Testes para SistemaInfo
"""

import json
from pathlib import Path

import pytest

from src.sistema_info import SistemaInfo

# =====================================
# 🔹 Teste básico de instância real
# =====================================


def test_instancia_real() -> None:
    """Deve instanciar sem erro no ambiente real."""
    sistema = SistemaInfo()

    assert isinstance(sistema.to_dict(), dict)
    assert "nome_sistema" in sistema.to_dict()


# =====================================
# 🔹 Teste de geração de relatório
# =====================================


def test_gerar_relatorio(tmp_path: Path) -> None:
    """Deve gerar um arquivo JSON válido."""
    sistema = SistemaInfo()

    arquivo: Path = sistema.gerar_relatorio(tmp_path)

    assert arquivo.exists()

    conteudo: dict[str, str] = json.loads(arquivo.read_text(encoding="utf-8"))

    assert conteudo["nome_sistema"] == sistema.to_dict()["nome_sistema"]


# =====================================
# 🔹 Teste parametrizado simulando SO
# =====================================


def test_simulando_sistemas(sistema_parametrizado: SistemaInfo) -> None:
    """Deve estruturar corretamente os blocos específicos."""
    dados: dict[str, str] = sistema_parametrizado.to_dict()
    nome_sistema: str = dados["nome_sistema"]

    assert "nome_sistema" in dados

    if dados["nome_sistema"] == "Windows":
        assert nome_sistema == "Windows"

    elif dados["nome_sistema"] == "Linux":
        assert nome_sistema == "Linux"

    elif dados["nome_sistema"] == "Darwin":
        assert nome_sistema == "Darwin"


def test_sistema_nao_suportado(monkeypatch: pytest.MonkeyPatch) -> None:
    """Teste para sistema operacional não suportado."""
    monkeypatch.setattr("platform.system", lambda: "Solaris")

    with pytest.raises(RuntimeError):
        SistemaInfo()


def test_linux_sem_os_release(monkeypatch: pytest.MonkeyPatch) -> None:
    """Teste para Linux sem /etc/os-release ou com falha na leitura."""
    monkeypatch.setattr("platform.system", lambda: "Linux")
    monkeypatch.setattr("platform.release", lambda: "1.0")
    monkeypatch.setattr("platform.machine", lambda: "x86_64")
    monkeypatch.setattr("platform.node", lambda: "TestMachine")
    monkeypatch.setattr("platform.python_version", lambda: "3.11.0")
    monkeypatch.setattr(
        "pathlib.Path.home", lambda: __import__("pathlib").Path("/fake/home")
    )

    monkeypatch.setattr("os.path.exists", lambda _: False)

    sistema = SistemaInfo()

    dados: dict[str, str] = sistema.to_dict()

    assert dados["linux_distribuicao"] == "Distribuição desconhecida"


def test_linux_excecao_os_release(monkeypatch: pytest.MonkeyPatch) -> None:
    """Teste para simular falha na leitura do /etc/os-release."""
    monkeypatch.setattr("platform.system", lambda: "Linux")
    monkeypatch.setattr("platform.release", lambda: "1.0")
    monkeypatch.setattr("platform.machine", lambda: "x86_64")
    monkeypatch.setattr("platform.node", lambda: "TestMachine")
    monkeypatch.setattr("platform.python_version", lambda: "3.11.0")
    monkeypatch.setattr(
        "pathlib.Path.home", lambda: __import__("pathlib").Path("/fake/home")
    )

    monkeypatch.setattr("os.path.exists", lambda _: True)
    monkeypatch.setattr(
        "platform.freedesktop_os_release",
        lambda: (_ for _ in ()).throw(ValueError()),
    )

    sistema = SistemaInfo()

    dados: dict[str, str] = sistema.to_dict()

    assert dados["linux_distribuicao"] == "Não identificado"
