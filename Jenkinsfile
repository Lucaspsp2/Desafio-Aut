// Este Jenkinsfile utiliza o Python e o Allure Command Line Tool.
// Certifique-se de que as ferramentas 'Python3.11' e 'Allure_CLI' estejam configuradas em 'Gerenciar Jenkins > Ferramentas'.
pipeline {
    agent any // Define onde o pipeline será executado (em qualquer agente disponível)

    // Variáveis de ambiente
    environment {
        VENV_NAME = 'venv_aut'
        ALLURE_RESULTS_DIR = 'allure-results'
        // Nomes das ferramentas configuradas no Jenkins
        PYTHON_TOOL_NAME = 'Python3.11'
        ALLURE_TOOL_NAME = 'Allure_CLI'
        // Define RUN_MOBILE_TESTS como 'false' por padrão
        RUN_MOBILE_TESTS = 'false' 
    }

    // Configuração das Ferramentas: Usa os nomes definidos no ambiente para carregar as ferramentas.
    tools {
        python PYTHON_TOOL_NAME
        allure ALLURE_TOOL_NAME
    }

    stages {
        stage('01. Preparação do Ambiente') {
            steps {
                script {
                    echo "Limpando diretórios antigos..."
                    // Garante que os diretórios sejam removidos, '|| true' previne falha se não existirem.
                    sh "rm -rf ${ALLURE_RESULTS_DIR} || true"
                    sh "rm -rf ${VENV_NAME} || true"

                    // Cria e ativa um ambiente virtual Python
                    echo "Criando e ativando ambiente virtual..."
                    sh "python3 -m venv ${VENV_NAME}" 
                    
                    // Instala as dependências a partir do requirements.txt
                    echo "Instalando dependências..."
                    // Todos os comandos que usam pip ou python devem ser prefixados pela ativação do venv
                    sh ". ${VENV_NAME}/bin/activate && pip install --upgrade pip"
                    sh ". ${VENV_NAME}/bin/activate && pip install -r requirements.txt"
                    echo "Preparação concluída."
                }
            }
        }

        stage('02. Execução dos Testes API e Web') {
            steps {
                script {
                    echo "Executando testes API e Web (sem Mobile)..."
                    // Executa o pytest e gera o diretório de resultados Allure
                    // O '|| true' garante que o pipeline continue para o bloco 'post' mesmo com falhas nos testes.
                    sh ". ${VENV_NAME}/bin/activate && pytest -m 'not mobile' --alluredir=${ALLURE_RESULTS_DIR} || true"
                    echo "Testes API e Web concluídos."
                }
            }
        }

        stage('03. Execução dos Testes Mobile') {
            // Este estágio só será executado se RUN_MOBILE_TESTS='true' no ambiente
            when {
                expression { return env.RUN_MOBILE_TESTS == 'true' } 
            }
            steps {
                script {
                    echo "Executando testes Mobile. Appium e Emulador devem estar ativos."
                    sh ". ${VENV_NAME}/bin/activate && pytest -m mobile --alluredir=${ALLURE_RESULTS_DIR} || true"
                    echo "Testes Mobile concluídos."
                }
            }
        }
    }

    // Bloco POST: Executa sempre
    post {
        always {
            echo "Publicando relatório Allure..."
            
            // Publica o relatório Allure
            allure(
                reportBuildPolicy: 'ALWAYS',
                results: [[path: ALLURE_RESULTS_DIR]],
                // ESSENCIAL: Especifica a ferramenta Allure CLI instalada no Jenkins
                allureCommandline: ALLURE_TOOL_NAME 
            )
            
            echo "Removendo ambiente virtual e limpando..."
            // Limpeza final: remove o ambiente virtual.
            sh "rm -rf ${VENV_NAME} || true"
        }
    }
}