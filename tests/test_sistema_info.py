"""Módulo de teste para a classe SistemaInfo"""

from src.sistema_info import SistemaInfo


def test_instancia_criada() -> None:
    """Teste para verificar a criação da instância e atributos básicos"""
    sistema = SistemaInfo()
    assert sistema.nome_sistema in ["Linux", "Windows", "Darwin"]


def test_home_existe() -> None:
    """Teste para verificar se o caminho do usuário existe e é um diretório válido"""
    sistema = SistemaInfo()
    assert sistema.user_admin.exists()
    assert sistema.user_admin.is_dir()


def test_python_version_format() -> None:
    """Teste para verificar se a versão do Python está no formato esperado (X.Y.Z)"""
    sistema = SistemaInfo()
    assert sistema.python_versao.count(".") == 2


def test_to_dict_nao_tem_none() -> None:
    """Teste para verificar se o método to_dict não retorna valores None"""
    sistema = SistemaInfo()
    info: dict[str, str | bool | dict[str, str] | None] = sistema.to_dict()
    for valor in info.values():
        assert valor is not None
