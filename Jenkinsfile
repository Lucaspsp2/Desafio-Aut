pipeline {
    agent {
        label 'built-in' 
    }
// Variáveis de ambiente que serão usadas nos estágios
environment {
    VENV_NAME = 'venv_aut'
    ALLURE_RESULTS_DIR = 'allure-results'
    // Define RUN_MOBILE_TESTS como 'false' por padrão para que o estágio Mobile só rode se o Appium estiver pronto.
    RUN_MOBILE_TESTS = 'false' 
}

stages {
    stage('Preparação do Ambiente') {
        steps {
            script {
                echo "Limpando diretórios antigos..."
                sh "rm -rf ${ALLURE_RESULTS_DIR}"

                // Cria e ativa um ambiente virtual Python
                echo "Criando e ativando ambiente virtual..."
                // Usamos 'python3' pois é o padrão no macOS (brew)
                sh "python3 -m venv ${VENV_NAME}" 
                
                // IMPORTANTE: O Jenkins precisa usar o python do ambiente virtual criado
                sh ". ${VENV_NAME}/bin/activate" 

                // Instala as dependências a partir do requirements.txt
                echo "Instalando dependências..."
                sh ". ${VENV_NAME}/bin/activate && pip install --upgrade pip"
                sh ". ${VENV_NAME}/bin/activate && pip install -r requirements.txt"
                echo "Preparação concluída."
            }
        }
    }

    stage('Execução dos Testes API e Web') {
        steps {
            script {
                echo "Executando testes API e Web (sem Mobile)..."
                // Executa o pytest, pulando os testes marcados com @pytest.mark.mobile
                sh ". ${VENV_NAME}/bin/activate && pytest -m 'not mobile' --alluredir=${ALLURE_RESULTS_DIR}"
            }
        }
    }

    stage('Execução dos Testes Mobile') {
        // Este estágio só será executado se você definir RUN_MOBILE_TESTS='true' nas configurações do Job.
        when {
            expression { return env.RUN_MOBILE_TESTS == 'true' } 
        }
        steps {
            script {
                echo "Executando testes Mobile. Appium e Emulador devem estar ativos."
                sh ". ${VENV_NAME}/bin/activate && pytest -m mobile --alluredir=${ALLURE_RESULTS_DIR}"
            }
        }
    }
}

post {
    always {
        // Desativa o ambiente virtual
        script {
            sh "deactivate"
        }
    }
    // Publica o relatório Allure (requer o plugin Allure instalado no Jenkins)
    allways {
        allure(
            reportBuildPolicy: 'ALWAYS',
            results: [[path: ALLURE_RESULTS_DIR]]
        )
    }
}
}