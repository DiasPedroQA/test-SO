"""Módulo de teste para a função gerar_relatorio"""

import json
from pathlib import Path
from src.relatorio import gerar_relatorio


def test_gerar_relatorio(tmp_path: Path) -> None:
    """Teste para verificar se o relatório é gerado corretamente e o arquivo JSON é criado"""
    relatorio: dict[str, str | dict[str, str]] = gerar_relatorio(output_dir=tmp_path)

    assert "so" in relatorio
    assert "hostname" in relatorio
    assert "status" in relatorio

    # Verifica se arquivo foi criado
    arquivos: list[Path] = list(tmp_path.glob("relatorio_*.json"))
    assert len(arquivos) == 1

    # Valida conteúdo JSON
    with open(arquivos[0], encoding="utf-8") as f:
        data: dict[str, str | dict[str, str]] = dict(json.load(f))

    assert data["status"] in ["PASSOU", "FALHOU"]
