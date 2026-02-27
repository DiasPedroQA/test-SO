# pylint: disable=C0413
#!/usr/bin/env python3

"""
Testes que validam comportamentos específicos de cada SO.
"""

import unittest
import sys
import platform
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.sistema_info import SistemaInfo


class TestExpectedOutputs(unittest.TestCase):
    """Testes específicos por sistema operacional"""

    def setUp(self):
        """Configuração antes de cada teste"""
        self.info = SistemaInfo.get_info_completa()
        self.sistema_atual = platform.system()

    def test_sistema_correto(self):
        """O sistema identificado deve corresponder ao real"""
        self.assertEqual(self.info["sistema"], self.sistema_atual)
        print(f"  ✅ Sistema correto: {self.sistema_atual}")

    def test_home_path_formato(self):
        """Valida o formato da home path para cada SO"""
        home = self.info["home_path"]

        if self.sistema_atual == "Windows":
            self.assertTrue(
                ":\\" in home or ":/" in home or "\\Users\\" in home  # C:\  # C:/
            )
            print(f"  ✅ Home Windows: {home}")

        elif self.sistema_atual == "Linux":
            self.assertTrue(home.startswith("/home/") or home == "/root")
            print(f"  ✅ Home Linux: {home}")

        elif self.sistema_atual == "Darwin":  # macOS
            self.assertTrue(home.startswith("/Users/"))
            print(f"  ✅ Home macOS: {home}")

    def test_informacoes_especificas(self):
        """Testa informações específicas de cada SO"""
        if self.sistema_atual == "Linux":
            self.assertIn("distribuicao", self.info)
            print(f"  ✅ Distribuição: {self.info['distribuicao']}")

        elif self.sistema_atual == "Windows":
            self.assertIn("variaveis_windows", self.info)
            print("  ✅ Variáveis Windows encontradas")

        elif self.sistema_atual == "Darwin":
            self.assertIn("versao_macos", self.info)
            print(f"  ✅ Versão macOS: {self.info['versao_macos']}")


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print(f"🧪 TESTANDO EM {platform.system()}")
    print("=" * 50)
    unittest.main(verbosity=2)
