"""
Fixtures compartilhadas para testes
"""

import pytest

from src.sistema_info import SistemaInfo


@pytest.fixture(params=["Windows", "Linux", "Darwin"])
def sistema_parametrizado(
    request: pytest.FixtureRequest, monkeypatch: pytest.MonkeyPatch
) -> SistemaInfo:
    """
    Simula diferentes sistemas operacionais
    de forma controlada.
    """

    so: dict[str, str] = request.param

    # Base comum
    monkeypatch.setattr("platform.system", lambda: so)
    monkeypatch.setattr("platform.release", lambda: "1.0")
    monkeypatch.setattr("platform.machine", lambda: "x86_64")
    monkeypatch.setattr("platform.node", lambda: "TestMachine")
    monkeypatch.setattr("platform.python_version", lambda: "3.11.0")
    monkeypatch.setattr(
        "pathlib.Path.home", lambda: __import__("pathlib").Path("/fake/home")
    )

    # Windows
    if so == "Windows":
        monkeypatch.setenv("USERPROFILE", "C:\\Users\\Test")
        monkeypatch.setenv("HOMEDRIVE", "C:")
        monkeypatch.setenv("HOMEPATH", "\\Users\\Test")

    # Linux
    elif so == "Linux":
        monkeypatch.setattr("os.path.exists", lambda _: True)
        monkeypatch.setattr(
            "platform.freedesktop_os_release",
            lambda: {"PRETTY_NAME": "Ubuntu Test"},
        )

    # macOS
    elif so == "Darwin":
        monkeypatch.setattr(
            "platform.mac_ver",
            lambda: ("14.0", ("", "", ""), ""),
        )

    return SistemaInfo()
