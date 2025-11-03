import os
import logging
from datetime import datetime

# Configuração do arquivo geral de erros
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "erros.log")
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def log_failure(message):
    """
    Registra falhas no arquivo de log central.
    """
    logging.error(message)
    print(f"📝 Erro registrado em logs/erros.log: {message}")
