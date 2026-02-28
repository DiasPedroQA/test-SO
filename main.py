"""Módulo principal do sistema de identificação de sistema operacional."""

# =====================================================
# CLI
# =====================================================


import sys

from src.sistema_info import SistemaInfo, coletar_sistema, gerar_relatorio


def main() -> int:
    """Ponto de entrada do script."""

    sistema: SistemaInfo = coletar_sistema()
    relatorio: dict[str, str | dict[str, str]] = gerar_relatorio(sistema)

    print("=" * 60)
    print("🔍 IDENTIFICADOR DE SISTEMA OPERACIONAL")
    print("=" * 60)

    for chave, valor in relatorio.items():
        print(f"• {chave}: {valor}")

    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
