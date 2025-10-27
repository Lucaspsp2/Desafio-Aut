import pytest
from utils.logger import log
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException


@pytest.fixture(scope="function")
def web_driver():
    """
    Fixture para inicializar e finalizar o Driver do Selenium (Web).
    """
    driver = None
    try:
        log.info("Inicializando Fixture: web_driver.")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        driver.implicitly_wait(5)
        driver.maximize_window()
    except WebDriverException as e:
        log.critical(f"Falha ao iniciar o WebDriver Web: {e}")
        pytest.skip(f"Não foi possível iniciar o Chrome. Pule este teste. Erro: {e}")
    yield driver
    if driver:
        log.info("Fechando o navegador.")
        driver.quit()

