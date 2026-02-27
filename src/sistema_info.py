# pylint: disable=C0413
#!/usr/bin/env python3

"""
Módulo para identificar informações do sistema operacional
e caminho da home directory do usuário.
"""

import os
import platform
import sys
from pathlib import Path
from typing import Dict, Any


class SistemaInfo:
    """Classe para obter informações do sistema operacional"""

    @staticmethod
    def get_nome_sistema() -> str:
        """
        Retorna o nome do sistema operacional.

        Returns:
            str: Nome do SO (Linux, Windows, Darwin, etc.)
        """
        return platform.system()

    @staticmethod
    def get_home_path() -> str:
        """
        Retorna o caminho absoluto da home directory do usuário.

        Returns:
            str: Caminho da home directory
        """
        return str(Path.home())

    @staticmethod
    def get_info_completa() -> Dict[str, Any]:
        """
        Retorna um dicionário com todas as informações do sistema.

        Returns:
            dict: Informações completas do sistema
        """
        sistema = platform.system()

        info: dict[str, str | dict[str, str]] = {
            "sistema": sistema,
            "sistema_versao": platform.release(),
            "arquitetura": platform.machine(),
            "hostname": platform.node(),
            "home_path": SistemaInfo.get_home_path(),
            "metodo_home": "Path.home()",
            "python_versao": platform.python_version(),
        }

        # CORREÇÃO 1: Adiciona informações específicas por SO
        # Em vez de usar update() com dicionário aninhado, adiciona as chaves diretamente
        if sistema == "Windows":
            # CORREÇÃO: Adiciona cada chave individualmente, não um dicionário aninhado
            info["USERPROFILE"] = os.environ.get("USERPROFILE", "")
            info["HOMEDRIVE"] = os.environ.get("HOMEDRIVE", "")
            info["HOMEPATH"] = os.environ.get("HOMEPATH", "")

            # Opcional: manter o dicionário agrupado se preferir
            info["variaveis_windows"] = {
                "USERPROFILE": os.environ.get("USERPROFILE", ""),
                "HOMEDRIVE": os.environ.get("HOMEDRIVE", ""),
                "HOMEPATH": os.environ.get("HOMEPATH", ""),
            }

        elif sistema == "Linux":
            # CORREÇÃO: Tratamento seguro para freedesktop_os_release()
            try:
                # Verifica se o arquivo existe antes de tentar ler
                if os.path.exists("/etc/os-release"):
                    os_release = platform.freedesktop_os_release()
                    distribuicao = os_release.get("PRETTY_NAME", "Desconhecido")
                else:
                    distribuicao = "Distribuição desconhecida"
            except (FileNotFoundError, AttributeError, KeyError):
                distribuicao = "Não foi possível identificar"

            info["distribuicao"] = distribuicao
            info["kernel"] = platform.release()

        elif sistema == "Darwin":  # macOS
            # CORREÇÃO: Tratamento seguro para mac_ver()
            mac_ver = platform.mac_ver()
            versao = mac_ver[0] if mac_ver and mac_ver[0] else "Versão desconhecida"
            info["versao_macos"] = versao

        return info

    @staticmethod
    def validar_home_path() -> bool:
        """
        Valida se o caminho da home directory existe e é acessível.

        Returns:
            bool: True se válido, False caso contrário
        """
        home = Path.home()
        return home.exists() and home.is_dir()


def main():
    """Função principal para demonstração"""
    print("=" * 60)
    print("🔍 IDENTIFICADOR DE SISTEMA OPERACIONAL")
    print("=" * 60)

    info = SistemaInfo.get_info_completa()

    print("\n📋 INFORMAÇÕES DO SISTEMA:")
    print(f"  • Sistema: {info['sistema']}")
    print(f"  • Versão: {info['sistema_versao']}")
    print(f"  • Arquitetura: {info['arquitetura']}")
    print(f"  • Hostname: {info['hostname']}")

    print("\n🏠 HOME DIRECTORY:")
    print(f"  • Caminho: {info['home_path']}")
    print(f"  • Método: {info['metodo_home']}")
    print(f"  • Válido: {'✅ Sim' if SistemaInfo.validar_home_path() else '❌ Não'}")

    # CORREÇÃO 3: Ajusta a exibição das informações específicas
    if "distribuicao" in info:
        print("\n🐧 LINUX:")
        print(f"  • Distribuição: {info['distribuicao']}")

    if "versao_macos" in info:
        print("\n🍎 MACOS:")
        print(f"  • Versão: {info['versao_macos']}")

    # CORREÇÃO: Verifica se o dicionário aninhado existe antes de iterar
    if "variaveis_windows" in info:
        print("\n🪟 WINDOWS (agrupado):")
        for var, valor in info["variaveis_windows"].items():
            print(f"  • {var}: {valor}")

    # Também mostra as variáveis individuais se existirem
    variaveis_individuais = ["USERPROFILE", "HOMEDRIVE", "HOMEPATH"]
    if any(var in info for var in variaveis_individuais):
        print("\n🪟 WINDOWS (variáveis individuais):")
        for var in variaveis_individuais:
            if var in info:
                print(f"  • {var}: {info[var]}")

    print("\n" + "=" * 60)

    # CORREÇÃO 4: Usa sys.exit em vez de exit() (resolve o aviso do Pylint)
    return 0


if __name__ == "__main__":
    # CORREÇÃO: Usa sys.exit em vez de exit()
    sys.exit(main())
