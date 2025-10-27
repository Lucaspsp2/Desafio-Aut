import pytest
import time
import re
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.web.base_page_web import BasePageWeb
from locators.web_locators import TempMailLocators, URLs, LoginPageLocators
from utils.logger import log


@pytest.mark.web
def test_new_user_registration_and_password_setup(web_driver):
    base_page = BasePageWeb(web_driver)
    wait = WebDriverWait(web_driver, 10)

    # ABRE AMERICANAS
    log.info("Abrindo Americanas na primeira aba...")
    web_driver.get(URLs.AMERICANAS_HOME)
    # Espera a página inicial carregar (ex: botão de login visível)
    wait.until(EC.visibility_of_element_located(LoginPageLocators.LOGIN_SIGNUP_LINK))
    log.info("✅ Página inicial carregada")

    # Fecha banner se existir
    try:
        banner_close = base_page._wait_for_element(LoginPageLocators.BANNER_CLOSE_BUTTON)
        if banner_close:
            base_page.click_element(LoginPageLocators.BANNER_CLOSE_BUTTON)
            # Espera o banner desaparecer
            wait.until(EC.invisibility_of_element_located(LoginPageLocators.BANNER_CLOSE_BUTTON))
            log.info("✅ Banner fechado com sucesso")
    except Exception:
        log.info("Nenhum Banner para fechar")

    # Navega para Login/SignUp
    base_page.click_element(LoginPageLocators.LOGIN_SIGNUP_LINK)
    wait.until(EC.visibility_of_element_located(LoginPageLocators.EMAIL_INPUT))
    log.info("✅ Página de login aberta com sucesso")

    # ABRE TEMP MAIL em nova aba
    web_driver.execute_script("window.open('');")
    web_driver.switch_to.window(web_driver.window_handles[1])
    web_driver.get(URLs.TEMP_MAIL)
    time.sleep(5)  # Aguarda geração do e-mail

    # Copia e-mail temporário
    email_field = base_page._wait_for_element(TempMailLocators.EMAIL_FIELD)
    temp_email = email_field.get_attribute("value")
    log.info(f"E-mail temporário: {temp_email}")
    time.sleep(10)  # Aguarda estabilidade da página

    # Retorna à aba do Americanas
    web_driver.switch_to.window(web_driver.window_handles[0])

    # Preenche e-mail no cadastro e envia
    wait.until(EC.visibility_of_element_located(LoginPageLocators.EMAIL_INPUT))
    base_page.safe_send_keys(LoginPageLocators.EMAIL_INPUT, temp_email)
    log.info("✅ E-mail inserido no cadastro")
    base_page.click_element(LoginPageLocators.CONTINUAR_BUTTON)
    wait.until(EC.visibility_of_element_located(LoginPageLocators.CODE_INPUT))
    log.info("✅ Campo de código de verificação visível")

    # CAPTURA CÓDIGO DE VERIFICAÇÃO DO E-MAIL
    web_driver.switch_to.window(web_driver.window_handles[1])
    verification_email_row = WebDriverWait(web_driver, 20).until(
        EC.visibility_of_element_located(TempMailLocators.FIRST_EMAIL_ROW)
    )
    verification_email_row.click()

    verification_text = WebDriverWait(web_driver, 15).until(
        EC.visibility_of_element_located(TempMailLocators.VERIFICATION_CODE)
    ).text
    log.info(f"Texto completo do e-mail: {verification_text}")

    # Extrai apenas os dígitos do código
    match = re.search(r"\b(\d{6})\b", verification_text)
    verification_code = match.group(1) if match else None
    assert verification_code is not None, "❌ Código de verificação não encontrado no e-mail."
    log.info(f"✅ Código de verificação capturado: {verification_code}")

    # CONFIRMA REGISTRO
    web_driver.switch_to.window(web_driver.window_handles[0])
    wait.until(EC.visibility_of_element_located(LoginPageLocators.CODE_INPUT))
    base_page.safe_send_keys(LoginPageLocators.CODE_INPUT, verification_code) 
    base_page.click_element(LoginPageLocators.CONFIRMAR_REGISTRO_BUTTON) 

    # VALIDA LOGIN
    user_header = wait.until(
        EC.visibility_of_element_located(LoginPageLocators.USER_HEADER_LINK)
    )
    assert user_header, "❌ Login não confirmado."
    log.info(f"✅ Login confirmado para o usuário: {user_header.text.strip()}")

    # ACESSA MINHA CONTA E AUTENTICAÇÃO
    base_page.click_element(LoginPageLocators.MINHA_CONTA_MENU)
    wait.until(EC.visibility_of_element_located(LoginPageLocators.SET_PASSWORD_SECTION))
    base_page.click_element(LoginPageLocators.SET_PASSWORD_SECTION)
    set_password_button = wait.until(
        EC.element_to_be_clickable(LoginPageLocators.SET_PASSWORD_BUTTON)
    )
    set_password_button.click() 
    log.info("✅ Botão 'Definir senha' clicado com sucesso")

    # CAPTURA CÓDIGO DE SENHA NO TEMP MAIL
    web_driver.switch_to.window(web_driver.window_handles[1])
    log.info("Aguardando o segundo e-mail de código de senha...")
    time.sleep(10)  # Aguarda chegada do e-mail
    password_email_row = WebDriverWait(web_driver, 20).until(
        EC.visibility_of_element_located(TempMailLocators.FIRST_EMAIL_ROW)
    )
    password_email_row.click()
    time.sleep(5)

    password_email_text = WebDriverWait(web_driver, 10).until(
        EC.visibility_of_element_located(TempMailLocators.VERIFICATION_CODE)
    ).text
    match = re.search(r"\b(\d{6})\b", password_email_text)
    password_code = match.group(1) if match else None
    assert password_code is not None, "❌ Código de senha não encontrado no e-mail."
    log.info(f"Código de senha recebido: {password_code}")

    # INSERE CÓDIGO DE SENHA
    web_driver.switch_to.window(web_driver.window_handles[0])
    wait.until(EC.visibility_of_element_located(LoginPageLocators.SECOND_CODE_INPUT))
    base_page.safe_send_keys(LoginPageLocators.SECOND_CODE_INPUT, password_code)
    log.info("✅ Código de redefinição de senha inserido")

    # TESTE DAS REGRAS DE SENHA
    password_field = base_page._wait_for_element(LoginPageLocators.NEW_PASSWORD_INPUT)

    # Menor que 8 caracteres
    password_field.send_keys("Ab1")
    time.sleep(1)
    assert "valid" not in base_page._wait_for_element(LoginPageLocators.RULE_8_CHAR).get_attribute("class"), \
        "❌ Regra de 8 caracteres marcada como válida incorretamente"

    # Sem números
    password_field.send_keys(Keys.COMMAND, "a", Keys.DELETE)
    password_field.send_keys("SenhaValida")
    time.sleep(1)
    assert "valid" not in base_page._wait_for_element(LoginPageLocators.RULE_NUMBER).get_attribute("class"), \
        "❌ Regra de número marcada como válida incorretamente"

    # Sem letras minúsculas
    password_field.send_keys(Keys.COMMAND, "a", Keys.DELETE)
    password_field.send_keys("SENHA123")
    time.sleep(1)
    assert "valid" not in base_page._wait_for_element(LoginPageLocators.RULE_LOWERCASE).get_attribute("class"), \
        "❌ Regra de minúscula marcada como válida incorretamente"

    # Sem letras maiúsculas
    password_field.send_keys(Keys.COMMAND, "a", Keys.DELETE)
    password_field.send_keys("senha123")
    time.sleep(1)
    assert "valid" not in base_page._wait_for_element(LoginPageLocators.RULE_UPPERCASE).get_attribute("class"), \
        "❌ Regra de maiúscula marcada como válida incorretamente"

    # DEFINE SENHA VÁLIDA
    password_field.send_keys(Keys.COMMAND, "a", Keys.DELETE)
    password_field.send_keys("Teste001")
    base_page.click_element(LoginPageLocators.SALVAR_SENHA_BUTTON)

    # VALIDA SUCESSO
    success_indicator = WebDriverWait(web_driver, 5).until(
        EC.visibility_of_element_located(LoginPageLocators.PASSWORD_SUCCESS_ASTERIKS)
    )
    assert success_indicator is not None, "❌ Falha ao salvar a senha válida"
    log.info("✅ Fluxo de teste de regras de senha e definição de senha concluído com sucesso")