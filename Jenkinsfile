// Este Jenkinsfile utiliza o Python e o Allure Command Line Tool.
// Certifique-se de que as ferramentas 'Python3.11' e 'Allure_CLI' estejam configuradas em 'Gerenciar Jenkins > Ferramentas'.
pipeline {
    agent any

    environment {
        // Variáveis de ambiente para o pipeline
        VENV_NAME = 'venv' // Nome do ambiente virtual
        ALLURE_TOOL_NAME = 'Allure_CLI' // Nome configurado no Gerenciamento de Ferramentas
        REPORT_PATH = 'allure-results'
    }

    tools {
        // O Jenkins só precisa gerenciar a ferramenta Allure
        allure ALLURE_TOOL_NAME 
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Preparação, Instalação e Testes') {
            steps {
                sh '''#!/bin/bash -ex
                    # 1. Cria e ativa o ambiente virtual Python
                    python3 -m venv ${VENV_NAME}
                    source ${VENV_NAME}/bin/activate
                    
                    # 2. Instala as dependências
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    
                    # 3. Execução dos testes
                    rm -rf ${REPORT_PATH}
                    pytest --alluredir=${REPORT_PATH}
                    
                    # O cleanup do ambiente virtual será feito na fase final
                '''
            }
        }

        stage('Geração do Relatório Allure') {
            // Garante que o relatório será gerado mesmo se os testes falharem (pós-ação)
            when {
                expression {
                    return currentBuild.result != 'NOT_BUILT'
                }
            }
            steps {
                // 1. Verifica se a ferramenta Allure está disponível no PATH
                sh 'allure --version'

                // 2. Gera o relatório usando a ferramenta Allure CLI
                script {
                    // Verifica se arquivos de resultado foram realmente criados
                    def results = findFiles(glob: '${REPORT_PATH}/*')
                    if (results.length > 0) {
                        allure([
                            allureCommandline: ALLURE_TOOL_NAME,
                            includeProperties: false,
                            issuePattern: '',
                            reportDirectory: REPORT_PATH,
                            properties: [],
                            reportFormats: [
                                reportFormat(type: 'HTML')
                            ],
                            severityPattern: '',
                            skipHistory: false,
                            xml: false
                        ])
                    } else {
                        echo 'ATENÇÃO: Nenhum arquivo de resultado Allure encontrado. O relatório não será gerado.'
                    }
                }
            }
        }

        stage('Cleanup') {
            steps {
                // Deleta o ambiente virtual
                sh 'rm -rf ${VENV_NAME}'
            }
        }
    }
}