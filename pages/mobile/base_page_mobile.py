from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.logger import log
from appium.webdriver.common.appiumby import AppiumBy
import time

class BasePageMobile:
    def __init__(self, driver, default_timeout=10):
        self.driver = driver
        self.default_timeout = default_timeout
        self.wait = WebDriverWait(driver, default_timeout)

    # --- waits & interações básicas ---
    def wait_for_element(self, locator, timeout=None):
        """Aguarda o elemento estar visível."""
        t = timeout or self.default_timeout
        try:
            WebDriverWait(self.driver, t).until(EC.visibility_of_element_located(locator))
            log.info(f"Elemento visível: {locator}")
            return True
        except Exception:
            log.warning(f"Timeout esperando elemento: {locator}")
            return False

    def click_element(self, locator, timeout=None):
        t = timeout or self.default_timeout
        element = WebDriverWait(self.driver, t).until(EC.element_to_be_clickable(locator))
        element.click()
        log.info(f"Clicou no elemento: {locator}")

    def send_keys(self, locator, text, timeout=None):
        t = timeout or self.default_timeout
        element = WebDriverWait(self.driver, t).until(EC.visibility_of_element_located(locator))
        try:
            element.clear()
        except Exception:
            pass
        element.send_keys(text)
        log.info(f"Enviou texto '{text}' para o elemento: {locator}")

    def get_text(self, locator, timeout=None):
        t = timeout or self.default_timeout
        element = WebDriverWait(self.driver, t).until(EC.visibility_of_element_located(locator))
        text = element.text
        log.info(f"Texto do elemento {locator}: {text}")
        return text

    def is_displayed(self, locator, timeout=3):
        try:
            element = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return element.is_displayed()
        except Exception:
            return False

    # --- helpers específicos para app mobile ---
    def close_promo_banner_if_present(self, banner_locator, wait_seconds=5):
        """
        Aguarda um pouco e tenta fechar o banner, se existir.
        Retorna True se fechou, False caso não encontrado.
        """
        try:
            log.info("Verificando banner promocional...")
            time.sleep(wait_seconds)  # banner aparece ~5s após abertura
            if self.is_displayed(banner_locator, timeout=4):
                self.click_element(banner_locator, timeout=4)
                log.info("Banner fechado com sucesso.")
                return True
            log.info("Nenhum banner encontrado.")
            return False
        except Exception as e:
            log.warning(f"Erro ao fechar banner (ignorado): {e}")
            return False

    def terminate_and_wait(self, app_package, wait_seconds=2):
        """
        Termina app (terminate_app) e espera. Usa terminate_app/activate_app.
        """
        try:
            self.driver.terminate_app(app_package)
        except Exception:
            try:
                self.driver.execute_script("mobile: terminateApp", {"appId": app_package})
            except Exception:
                log.warning("Não foi possível terminar o app via driver.")
        time.sleep(wait_seconds)

    def activate_app(self, app_package):
        """
        Reativa o app após término.
        """
        try:
            self.driver.activate_app(app_package)
        except Exception:
            try:
                self.driver.execute_script("mobile: activateApp", {"appId": app_package})
            except Exception:
                log.warning("Não foi possível ativar o app via driver.")
