"""
Módulo responsável por:

- Detectar automaticamente o sistema operacional
- Coletar informações relevantes
- Gerar relatório JSON estruturado

Versão simplificada e auto gerenciável.
"""

import json
import os
import platform
from pathlib import Path


class SistemaInfo:
    """
    Classe responsável por detectar o sistema atual
    e organizar as informações automaticamente.
    """

    def __init__(self) -> None:
        self.dados: dict[str, str] = {}
        self._coletar_informacoes()

    # ===============================
    # MÉTODO PRINCIPAL
    # ===============================

    def _coletar_informacoes(self) -> None:
        """Detecta o SO e direciona para coleta específica."""

        self.dados.clear()  # Garante que os dados sejam limpos antes de coletar

        sistema: str = platform.system()
        self.dados.update(
            {
                "nome_sistema": sistema,
                "versao_sistema": platform.release(),
                "arquitetura": platform.machine(),
                "nome_computador": platform.node(),
                "user_home": str(Path.home()),
                "python_versao": platform.python_version(),
            }
        )

        if sistema == "Windows":
            self._coletar_windows()

        elif sistema == "Linux":
            self._coletar_linux()

        elif sistema == "Darwin":
            self._coletar_macos()

        else:
            raise RuntimeError(f"Sistema não suportado: {sistema}")

    # ===============================
    # COLETAS ESPECÍFICAS
    # ===============================

    def _coletar_windows(self) -> None:
        """Adiciona informações específicas do Windows."""
        perfil_usuario: str = os.environ.get("USERPROFILE", "Desconecido")
        home_drive: str = os.environ.get("HOMEDRIVE", "Desconecido")
        home_path: str = os.environ.get("HOMEPATH", "Desconecido")
        self.dados.update(
            {
                "windows_USERPROFILE": perfil_usuario,
                "windows_HOMEDRIVE": home_drive,
                "windows_HOMEPATH": home_path,
            }
        )

    def _coletar_linux(self) -> None:
        """Adiciona informações específicas do Linux."""
        try:
            if os.path.exists("/etc/os-release"):
                os_release: dict[str, str] = platform.freedesktop_os_release()
                distribuicao: str = str(os_release.get("PRETTY_NAME"))
            else:
                distribuicao = "Distribuição desconhecida"
        except (ValueError, KeyError):
            distribuicao = "Não identificado"

        self.dados.update({"linux_distribuicao": distribuicao})

    def _coletar_macos(self) -> None:
        """Adiciona informações específicas do macOS."""
        versao: str = platform.mac_ver()[0]
        self.dados.update({"macos_versao": versao})

    # ===============================
    # EXPORTAÇÃO
    # ===============================

    def to_dict(self) -> dict[str, str]:
        """Retorna os dados coletados."""
        return self.dados

    def gerar_relatorio(self, output_dir: Path | None = None) -> Path:
        """Gera arquivo JSON com os dados."""
        pasta: Path = Path(output_dir) if output_dir else Path.cwd()

        arquivo: Path = pasta / f"relatorio_{self.dados['nome_sistema']}.json"

        arquivo.write_text(
            json.dumps(self.dados, indent=4, ensure_ascii=False),
            encoding="utf-8",
        )

        return arquivo
