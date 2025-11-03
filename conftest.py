import pytest
from utils.logger import log
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException
from appium import webdriver as appium_webdriver #add agora
from appium.options.android import UiAutomator2Options #add agora



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


# FIXTURE MOBILE 

@pytest.fixture(scope="function")
def mobile_driver():
    """
    Fixture para inicializar e finalizar o Driver do Appium (Mobile).
    """
    driver = None
    try:
        log.info("Inicializando Fixture: mobile_driver (Appium).")

        options = UiAutomator2Options()
        options.platform_name = "Android"
        options.device_name = "emulator-5544"
        options.app_package = "com.b2w.americanas"
        options.app_activity = "com.b2w.americanas.MainActivity"
        options.automation_name = "UiAutomator2"
        options.no_reset = True

        driver = appium_webdriver.Remote("http://localhost:4723", options=options)
        driver.implicitly_wait(10)
        log.info("Driver Appium inicializado com sucesso.")

    except WebDriverException as e:
        log.critical(f"Falha ao iniciar o Appium: {e}")
        pytest.skip(f"Appium não iniciou corretamente. Erro: {e}")

    yield driver

    if driver:
        log.info("Encerrando driver Appium.")
        driver.quit()