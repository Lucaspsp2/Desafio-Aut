import logging
import sys

# Função para configurar o logger centralizado
def setup_logger():
    # logger com um nome específico do projeto
    logger = logging.getLogger("aut-americanas")
    
    # Define o nível mínimo de logs para INFO (para ver no console)
    logger.setLevel(logging.INFO)

    # Cria um handler para imprimir no console (saída padrão)
    handler = logging.StreamHandler(sys.stdout)
    
    # Define o formato da mensagem de log
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Adiciona o handler ao logger APENAS se ele ainda não tiver um
    if not logger.handlers:
        logger.addHandler(handler)

    # Desabilita a propagação para o logger root do Pytest.
    logger.propagate = False

    return logger

# Instância global do nosso logger
log = setup_logger()

# Teste inicial (Opcional)
# log.info("Logger de automação inicializado com sucesso.") 
