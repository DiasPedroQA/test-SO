# pylint: disable=C0413
#!/usr/bin/env python3

"""
Módulo para gerar relatórios de teste multi-SO.
Este script coleta informações do sistema e gera um relatório JSON.
"""

# Import relativo do pacote src
import sys
from pathlib import Path
from typing import Any
import platform
import os
import json

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.sistema_info import SistemaInfo


# CORREÇÃO 1: Adiciona o path ANTES de importar
# O path precisa ser inserido antes do import
SRC_PATH = str(Path(__file__).parent.parent / "src")
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

# CORREÇÃO 2: Importa a classe correta (não a função identificar_sistema)


def gerar_relatorio() -> dict[str, Any]:
    """
    Gera relatório com informações do sistema para testes.

    Returns:
        dict[str, Any]: Dicionário com todas as informações do relatório
    """
    # CORREÇÃO 3: Usa o método correto da classe
    info = SistemaInfo.get_info_completa()

    # CORREÇÃO 4: Usa as chaves corretas do dicionário info
    # O info retorna: 'sistema', 'home_path', 'arquitetura', etc.
    # Não retorna: 'detalhes', 'home', 'usuario'

    sistema_atual = platform.system()

    relatorio = {
        "so": sistema_atual,
        "so_detalhes": info.get("distribuicao")
        or info.get("versao_macos")
        or "Detalhes não disponíveis",
        "hostname": info["hostname"],
        "python": info["python_versao"],
        "testes": {
            "sistema_identificado": info["sistema"],
            "home_path": info["home_path"],  # CORREÇÃO: era 'home', agora é 'home_path'
            "home_existe": str(
                SistemaInfo.validar_home_path()
            ),  # CORREÇÃO: usa o método da classe
            "arquitetura": info["arquitetura"],
            "usuario": _get_usuario_from_info(
                info
            ),  # CORREÇÃO: função auxiliar para pegar usuário
        },
        "status": "PASSOU" if info["sistema"] == sistema_atual else "FALHOU",
    }

    # Adiciona informações específicas do SO se existirem
    if "variaveis_windows" in info:
        relatorio["variaveis_windows"] = info["variaveis_windows"]

    # CORREÇÃO 5: Especifica o encoding UTF-8
    # Importante para Windows e caracteres especiais
    with open(f"relatorio_{sistema_atual}.json", "w", encoding="utf-8") as f:
        json.dump(relatorio, f, indent=2, ensure_ascii=False)

    print(f"📊 Relatório gerado: relatorio_{sistema_atual}.json")
    return relatorio


def _get_usuario_from_info(info: dict[str, Any]) -> str:
    """
    Função auxiliar para extrair nome do usuário das informações disponíveis.

    Args:
        info: Dicionário com informações do sistema

    Returns:
        str: Nome do usuário ou 'desconhecido'
    """
    # Tenta diferentes formas de obter o usuário
    if "usuario" in info:
        return info["usuario"]

    # Tenta via variáveis de ambiente
    return os.environ.get("USER") or os.environ.get("USERNAME") or "desconhecido"


def main() -> int:
    """
    Função principal.

    Returns:
        int: Código de saída (0 para sucesso)
    """
    try:
        relatorio = gerar_relatorio()
        print("\n📋 CONTEÚDO DO RELATÓRIO:")
        print(json.dumps(relatorio, indent=2, ensure_ascii=False))
        return 0
    except (ValueError, TypeError, KeyError) as e:
        print(f"❌ Erro ao gerar relatório: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
