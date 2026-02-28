# pylint: disable=redefined-outer-name

"""Configuração de fixtures para testes"""

from pathlib import Path
import pytest

from src.sistema_info import coletar_sistema, SistemaInfo


@pytest.fixture(scope="session")
def fake_home(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Cria diretório temporário simulando a home do usuário"""
    return tmp_path_factory.mktemp("home_dir")


@pytest.fixture(params=["Windows", "Linux", "Darwin"])
def sistema_parametrizado(
    request: pytest.FixtureRequest,
    monkeypatch: pytest.MonkeyPatch,
    fake_home: Path,
) -> SistemaInfo:
    """Simula diferentes sistemas operacionais"""

    so: str = request.param

    monkeypatch.setattr("platform.system", lambda: so)
    monkeypatch.setattr("platform.release", lambda: "1.0")
    monkeypatch.setattr("platform.machine", lambda: "x86_64")
    monkeypatch.setattr("platform.node", lambda: "TestMachine")
    monkeypatch.setattr("platform.python_version", lambda: "3.11.0")
    monkeypatch.setattr("pathlib.Path.home", lambda: fake_home)

    if so == "Windows":
        monkeypatch.setenv("USERPROFILE", "C:\\Users\\Test")
        monkeypatch.setenv("HOMEDRIVE", "C:")
        monkeypatch.setenv("HOMEPATH", "\\Users\\Test")

    elif so == "Linux":
        monkeypatch.setattr("os.path.exists", lambda x: True)
        monkeypatch.setattr(
            "platform.freedesktop_os_release",
            lambda: {"PRETTY_NAME": "Ubuntu 22.04"},
        )

    elif so == "Darwin":
        monkeypatch.setattr(
            "platform.mac_ver",
            lambda: ("14.0", ("", "", ""), ""),
        )

    return coletar_sistema()
