"""Módulo principal do sistema de identificação de sistema operacional."""

# =====================================================
# CLI
# =====================================================

import sys
from pathlib import Path

from src.sistema_info import SistemaInfo


def main() -> int:
    """Ponto de entrada do script."""

    # Instancia automaticamente e coleta os dados
    sistema = SistemaInfo()

    # Gera relatório
    caminho_arquivo: Path = sistema.gerar_relatorio()

    print("=" * 60)
    print("🔍 IDENTIFICADOR DE SISTEMA OPERACIONAL")
    print("=" * 60)

    # Exibe dados no terminal
    for chave, valor in sistema.to_dict().items():
        print(f"• {chave}: {valor}")

    print("=" * 60)
    print(f"\n📁 Relatório salvo em: {caminho_arquivo}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
