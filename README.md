# test-SO

Validação e simulação de Sistemas Operacionais com testes multi-OS reais e pipeline de integração contínua avançada.

---

## 📊 Status do Projeto

![CI](https://github.com/DiasPedroQA/test-SO/actions/workflows/ci.yml/badge.svg)
![Coverage](https://codecov.io/gh/DiasPedroQA/test-SO/branch/main/graph/badge.svg)
![Python](https://img.shields.io/badge/python-3.10%20|%203.11%20|%203.12-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 🎯 Objetivo

Este projeto demonstra técnicas de:

* Validação de comportamento dependente de sistema operacional
* Simulação de ambientes utilizando monkeypatch
* Execução de testes em múltiplos sistemas operacionais reais
* Integração contínua com cobertura mínima garantida
* Publicação automatizada de métricas de qualidade

---

## 🧪 Funcionalidades Demonstradas

* ✔ Detecção automática de sistema operacional
* ✔ Simulação controlada via monkeypatch
* ✔ Testes executados em:

  * Linux
  * Windows
  * macOS
* ✔ Cobertura mínima obrigatória (90%)
* ✔ Integração com Codecov
* ✔ Análise estática de segurança com Bandit
* ✔ Pipeline CI multi-OS no GitHub Actions

---

## 🚀 Como executar localmente

### 1️⃣ Clone o projeto

```bash
git clone https://github.com/DiasPedroQA/test-SO.git
cd test-SO
```

### 2️⃣ Crie ambiente virtual

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# ou
.venv\Scripts\activate  # Windows
```

### 3️⃣ Instale dependências de teste

```bash
pip install -r requirements-dev.txt
```

### 4️⃣ Execute os testes

```bash
pytest
```

---

## 📈 Cobertura de Código

O projeto exige:

* Cobertura mínima de 90%
* Geração de relatório XML
* Upload automático para Codecov
* Análise de cobertura por patch e projeto

---

## 🔐 Segurança

O pipeline inclui análise estática com Bandit para identificar possíveis vulnerabilidades.

---

## 🏗 Estrutura do Projeto

```powershell
test-SO/
│
├── src/
│   └── ...
│
├── tests/
│   └── ...
│
├── .github/workflows/
│   ├── ci.yml
│   └── test-multi-os.yml
│
├── pytest.ini
├── codecov.yml
└── requirements-dev.txt
```

---

## 📄 Licença

Distribuído sob licença MIT.
