"""
Testes para SistemaInfo, coletar_sistema e gerar_relatorio
"""

import json
from pathlib import Path
from src.sistema_info import SistemaInfo, gerar_relatorio


# ======================================================
# Testes de instanciação e atributos básicos
# ======================================================


def test_instancia_criada(sistema_parametrizado: SistemaInfo) -> None:
    """Verifica criação básica da instância"""

    sistema: SistemaInfo = sistema_parametrizado

    assert sistema.nome_sistema in ["Linux", "Windows", "Darwin"]
    assert sistema.nome_computador == "TestMachine"
    assert sistema.python_versao == "3.11.0"
    assert sistema.arquitetura == "x86_64"
    assert sistema.user_admin.exists()


def test_to_dict_nao_tem_none(sistema_parametrizado: SistemaInfo) -> None:
    """Garante que to_dict não retorna valores None"""

    info: dict[str, str | dict[str, str]] = sistema_parametrizado.to_dict()

    for valor in info.values():
        assert valor is not None


# ======================================================
# Testes específicos por sistema operacional
# ======================================================


def test_info_especifica_por_so(sistema_parametrizado: SistemaInfo) -> None:
    """Verifica se campos específicos são preenchidos corretamente"""

    sistema: SistemaInfo = sistema_parametrizado

    if sistema.nome_sistema == "Linux":
        assert sistema.distribuicao == "Ubuntu 22.04"

    elif sistema.nome_sistema == "Windows":
        assert sistema.variaveis_windows is not None
        assert sistema.variaveis_windows["USERPROFILE"] == "C:\\Users\\Test"

    elif sistema.nome_sistema == "Darwin":
        assert sistema.versao_macos == "14.0"


# ======================================================
# Teste de geração de relatório
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

    # Verifica se arquivo foi criado
    arquivos: list[Path] = list(tmp_path.glob("relatorio_*.json"))
    assert len(arquivos) == 1

    # Verifica conteúdo do arquivo
    with open(arquivos[0], encoding="utf-8") as f:
        data: dict[str, str | dict[str, str]] = dict(json.load(f))

    assert data == relatorio
