from selenium.webdriver.common.by import By

# -----------------------------
# URLs base dos sites
# -----------------------------
class URLs:
    TEMP_MAIL = "https://temp-mail.io/en"
    AMERICANAS_HOME = "https://www.americanas.com.br/"

# -----------------------------
# Locators da TempMailPage
# -----------------------------
class TempMailLocators:
    EMAIL_FIELD = (By.CSS_SELECTOR, 'input[data-qa="current-email"]')  # campo do email temporário
    FIRST_EMAIL_ROW = (By.CSS_SELECTOR, '[data-qa="message"]')  # linha do primeiro email recebido

    # Novo locator para o código dentro do e-mail
    VERIFICATION_CODE = (By.CSS_SELECTOR, "span[data-qa='message-subject']")
# -----------------------------
# Locators da LoginPageWeb
# -----------------------------
class LoginPageLocators:
    BANNER_CLOSE_BUTTON = (By.ID, "close-button-1454703513200")
    LOGIN_SIGNUP_LINK = (By.CSS_SELECTOR, 'a.ButtonLogin_Container__sgzuk')
    LOGIN_TITLE_HEADER = (By.XPATH, "//h2[contains(text(), 'login do cliente')]")
    EMAIL_INPUT = (By.NAME, "email")
    CONTINUAR_BUTTON = (By.XPATH, "//button//span[contains(text(), 'Enviar')]")
    CODE_INPUT = (By.NAME, "token")
    CONFIRMAR_REGISTRO_BUTTON = (By.XPATH, "//button//span[contains(text(), 'Confirmar')]")
    USER_HEADER_LINK = (By.CSS_SELECTOR, 'div.ButtonLogin_textContainer__7NZHr')
    MINHA_CONTA_MENU = (By.CSS_SELECTOR, 'span.ButtonLogin_myAccount__mte5i')
    SET_PASSWORD_SECTION = (By.XPATH, "//a[contains(text(), 'Autenticação')]")
    SET_PASSWORD_BUTTON = (By.XPATH, "//button//*[contains(text(), 'Definir senha')]")
    SECOND_CODE_INPUT = (By.CSS_SELECTOR, 'input[type="text"]:not([name])')
    NEW_PASSWORD_INPUT = (By.CSS_SELECTOR, 'input[type="password"]')
    SALVAR_SENHA_BUTTON = (By.XPATH, "//button//*[contains(text(), 'Salvar senha')]")
    RULE_8_CHAR = (By.CSS_SELECTOR, '.vtex-my-authentication-1-x-passValidation_minLength')
    RULE_NUMBER = (By.CSS_SELECTOR, '.vtex-my-authentication-1-x-passValidation_number')
    RULE_LOWERCASE = (By.CSS_SELECTOR, '.vtex-my-authentication-1-x-passValidation_lower')
    RULE_UPPERCASE = (By.CSS_SELECTOR, '.vtex-my-authentication-1-x-passValidation_upper')
    PASSWORD_SUCCESS_ASTERIKS = (By.CSS_SELECTOR, '.vtex-my-authentication-1-x-maskedPassword_content')
