# Framework de Automação Americanas (Desafio Técnico)

## Objetivo
Este projeto consiste na implementação de um framework robusto de automação de testes para validar fluxos Web, Mobile (App Americanas) e a API de Wishlist. O foco é a aplicação de boas práticas de desenvolvimento e arquitetura, utilizando o padrão Page Object Model (POM) e testes orientados a dados.

---

## Tecnologias e Arquitetura

### Framework Core
| Componente | Função | Padrão Aplicado |
| :--- | :--- | :--- |
| **Pytest** | Executor principal dos testes. | Markers, Fixtures, Hooks. |
| **Appium** | Automação Mobile. | Explicit Waits, BasePage, POM. |
| **Requests** | Automação e pré-condição dos testes de API. | Testes de API Orientados a Cenário. |
| **Selenium** | Automação Web (Site Americanas). | POM e Configurações de Driver. |

### Arquitetura (Padrões de Código)
* **Page Object Model (POM):** Classes separadas para Web, Mobile e API.
* **Fluent Interface:** Métodos de Page Object que retornam a próxima página.
* **Locators:** Utilização de classes aninhadas (`class Locators`) para alta manutenção.
* **Sincronização:** Uso exclusivo de **Explicit Waits** para evitar testes frágeis (`time.sleep`).

### Evidências e Logs
* **Allure Report:** Geração de relatórios HTML detalhados.
* **Logging Profissional:** Módulo `logging` com logs em tempo real (INFO/DEBUG).
* **Captura de Evidência:** Screenshots e **Gravação de Vídeo** automáticas em caso de falha de teste.

---

## Pré-requisitos e Setup

Para executar o framework, você deve ter os seguintes itens instalados e configurados:

1.  **Python 3.x** e o ambiente virtual (`americanas/`) ativado.
2.  **Appium Server** rodando (porta padrão `4723`).
3.  **ADB/Android Emulator** ou dispositivo físico conectado (para testes Mobile).
4.  **Wishlist API** rodando localmente (na porta `8000`).
5.  **Allure Command-Line** (para geração final do HTML).

### 1. Instalação de Dependências
```bash
# Ative o ambiente (americanas)
source americanas/bin/activate 

# Instale as bibliotecas
pip install -r requirements.txt
