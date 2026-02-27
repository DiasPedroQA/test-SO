# pylint: disable=C0413
#!/usr/bin/env python3

"""
Testes unitários para o módulo sistema_info.
"""

import unittest
import sys
import os
from pathlib import Path

# Importa direto do src (funciona porque temos __init__.py)
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.sistema_info import SistemaInfo


class TestSistemaInfo(unittest.TestCase):
    """Testes para a classe SistemaInfo"""

    def test_get_nome_sistema(self):
        """Testa se retorna um nome de sistema válido"""
        nome = SistemaInfo.get_nome_sistema()
        self.assertIn(nome, ["Linux", "Windows", "Darwin"])
        print(f"  ✅ Sistema: {nome}")

    def test_get_home_path(self):
        """Testa se retorna um caminho de home válido"""
        home = SistemaInfo.get_home_path()
        self.assertIsInstance(home, str)
        self.assertTrue(len(home) > 0)
        self.assertTrue(os.path.isabs(home))
        print(f"  ✅ Home: {home}")

    def test_validar_home_path(self):
        """Testa se a validação da home funciona"""
        self.assertTrue(SistemaInfo.validar_home_path())
        print("  ✅ Home válida")

    def test_get_info_completa(self):
        """Testa se retorna todas as informações esperadas"""
        info = SistemaInfo.get_info_completa()

        # Campos obrigatórios
        campos = [
            "sistema",
            "sistema_versao",
            "arquitetura",
            "hostname",
            "home_path",
            "python_versao",
        ]

        for campo in campos:
            self.assertIn(campo, info)
            self.assertTrue(info[campo])

        print(f"  ✅ Info completa para {info['sistema']}")


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("🧪 TESTANDO SISTEMA INFO")
    print("=" * 50)
    unittest.main(verbosity=2)
