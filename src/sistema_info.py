# pylint: disable=C0413, R0902
#!/usr/bin/env python3

"""
Módulo para identificar informações do sistema operacional
e caminho da home directory do usuário.
"""

import os
import platform
import sys
from pathlib import Path


class SistemaInfo:
    """Classe para obter informações do sistema operacional"""

    def __init__(self) -> None:
        self.nome_sistema: str = platform.system()
        self.versao_sistema: str = platform.release()
        self.arquitetura: str = platform.machine()
        self.nome_computador: str = platform.node()
        self.user_admin: Path = Path.home()
        self.python_versao: str = platform.python_version()

        # Inicializa atributos opcionais
        self.distribuicao: str | None = None
        self.versao_macos: str | None = None
        self.variaveis_windows: dict[str, str] | None = None

        self._carregar_detalhes_especificos()

    # -------------------------
    # Métodos internos privados
    # -------------------------

    def _carregar_detalhes_especificos(self) -> None:
        if self.nome_sistema == "Windows":
            self.variaveis_windows = {
                "USERPROFILE": os.environ.get("USERPROFILE", "Desconhecido"),
                "HOMEDRIVE": os.environ.get("HOMEDRIVE", "Desconhecido"),
                "HOMEPATH": os.environ.get("HOMEPATH", "Desconhecido"),
            }

        elif self.nome_sistema == "Linux":
            try:
                if os.path.exists("/etc/os-release"):
                    os_release: dict[str, str] = platform.freedesktop_os_release()
                    self.distribuicao = os_release.get("PRETTY_NAME", "Desconhecido")
                else:
                    self.distribuicao = "Distribuição desconhecida"
            except (ValueError, KeyError, OSError):
                self.distribuicao = "Não foi possível identificar"

        elif self.nome_sistema == "Darwin":
            mac_ver: tuple[str, tuple[str, str, str], str] = platform.mac_ver()
            self.versao_macos = (
                mac_ver[0] if mac_ver and mac_ver[0] else "Versão desconhecida"
            )

    # -------------------------
    # Métodos públicos
    # -------------------------

    def to_dict(self) -> dict[str, str | bool | dict[str, str] | None]:
        """Retorna todas as informações como dicionário"""
        return {
            chave: valor for chave, valor in self.__dict__.items() if valor is not None
        }

    def exibir_detalhes(self) -> None:
        """Exibe automaticamente todos os atributos"""
        print("=" * 60)
        print("🔍 IDENTIFICADOR DE SISTEMA OPERACIONAL")
        print("=" * 60)

        for chave, valor in self.to_dict().items():
            print(f"• {chave}: {valor}")

        print("=" * 60)


def test_sistema_info_instancia() -> None:
    """Teste para verificar a criação da instância e atributos básicos"""
    sistema: SistemaInfo = SistemaInfo()
    assert sistema.nome_sistema in ["Windows", "Linux", "Darwin"]
    assert sistema.user_admin.exists() and sistema.user_admin.is_dir()
    assert sistema.python_versao.count(".") == 2
    assert len(sistema.versao_sistema.split(".")) >= 3
    assert int(sistema.arquitetura.split("_")[1]) > 0
    assert sistema.nome_computador is not None
    assert len(str(sistema.distribuicao).split(" ")[1]) > 0


def main() -> int:
    """Função principal para execução do módulo"""
    sistema = SistemaInfo()
    sistema.exibir_detalhes()
    return 0


if __name__ == "__main__":
    sys.exit(main())
