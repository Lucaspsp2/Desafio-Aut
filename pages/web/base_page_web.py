from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from utils.logger import log

class BasePageWeb:
    """Classe base para todas as páginas Web."""
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout

    def _wait_for_element(self, locator):
        """Espera até o elemento estar visível e interagível."""
        try:
            element = WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return element
        except TimeoutException:
            log.error(f"Elemento não encontrado: {locator}")
            return None

    def click_element(self, locator):
        """Clica em um elemento após esperar que esteja visível."""
        element = self._wait_for_element(locator)
        if element:
            try:
                element.click()
                log.info(f"Clique realizado: {locator}")
            except ElementClickInterceptedException:
                self.driver.execute_script("arguments[0].click();", element)
                log.info(f"Clique via JS realizado: {locator}")
        else:
            log.error(f"Falha ao clicar: {locator}")

    def safe_send_keys(self, locator, text):
        """Envia texto ao input com verificação."""
        element = self._wait_for_element(locator)
        if element:
            element.clear()
            element.send_keys(text)
            log.info(f"Texto enviado a {locator}: {text}")
        else:
            log.error(f"Falha ao enviar texto para {locator}")
    