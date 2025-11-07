import pytest
from utils.logger import log
#imports web
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException
#imports mobile
from appium import webdriver as appium_webdriver 
from appium.options.android import UiAutomator2Options
#imports API
from utils.api_client import APIClient 
from pages.api.registro_endpoints import RegistroEndpoints 
from pages.api.wishlist_endpoints import WishlistEndpoints
from utils.data_generator import DataGenerator
import logging


logger = logging.getLogger('aut-americanas')

#FIXTURE API
@pytest.fixture(scope="session")# A fixture sera executada apenas uma vez
def api_client():
    """Fornece uma instância do cliente API (base para todos os serviços)."""
    return APIClient()

@pytest.fixture(scope="session")
def registro_api(api_client):
    """Fornece a instância do serviço RegistroEndpoints."""
    return RegistroEndpoints(api_client)

@pytest.fixture(scope="session")
def wishlist_api(api_client):
    """Fornece a instância do serviço WishlistEndpoints."""
    return WishlistEndpoints(api_client)

@pytest.fixture(scope="session")
def default_auth_token(registro_api):
    """
    Autentica o usuário padrão (projeto@example.com) e retorna o JWT.
    Usado para testes que requerem um token válido.
    """
    log.info("Fixture: Obtendo token do usuário padrão.")
    email = "projeto@example.com"
    password = "Senha123!" 
    
    response = registro_api.login_user(email, password)
    assert response.status_code == 200, "Falha na fixture: Não conseguiu obter token do usuário padrão."
    
    return response.json().get("access_token")

@pytest.fixture(scope="function") # Usuario sera criado do zero para cada funcao de teste
def unique_registered_user(registro_api):
    """Cria, registra, faz login e retorna os dados do usuário ÚNICO com o token."""
    email = DataGenerator.generate_unique_email()
    password = DataGenerator.generate_strong_password()
    username = DataGenerator.generate_unique_username()

    # 1. TENTA REGISTRAR O USUÁRIO
    response_register = registro_api.register_user(email, password, username)

    # Verifica se o registro falhou por algum erro inesperado (ex: 422, 500)
    if response_register.status_code != 200:
        error_detail = response_register.text
        # (código de debug 422 pode continuar aqui)
        # Se for 409 (Duplicado) pode ser aceitável dependendo do ambiente, mas 200 é o ideal
        assert response_register.status_code == 200, (
            f"Falha na fixture: Não conseguiu registrar o usuário único. "
            f"Resposta: {response_register.status_code}\nCorpo do erro: {response_register.text}"
        )

    # 2. FAZ LOGIN PARA OBTER O TOKEN
    # Como a API de Registro (200) não retorna o token, preciso fazer o Login.
    response_login = registro_api.login_user(email, password)
    
    assert response_login.status_code == 200, (
        f"Falha na fixture: Registro OK, mas não conseguiu fazer Login. "
        f"Resposta: {response_login.status_code}\nCorpo do erro: {response_login.text}"
    )

    # 3. EXTRAI O TOKEN
    token = response_login.json().get("access_token")

    assert token is not None, f"Falha na fixture: Login bem-sucedido (200) mas sem 'access_token' na resposta: {response_login.text}"

    # Retorna o token, email e password para ser usado na fixture unique_auth_token
    return {
        "email": email,
        "password": password,
        "username": username,
        "token": token
    }
@pytest.fixture(scope="function")
def unique_auth_token(registro_api, unique_registered_user):
    """Cria um usuário único, loga, e retorna seu token."""
    login_response = registro_api.login_user(
        unique_registered_user["email"], 
        unique_registered_user["password"]
    )
    assert login_response.status_code == 200
    return login_response.json().get("access_token")

# FIXTURES DE DADOS PARA TESTES DE WISHLIST/PRODUCTS

@pytest.fixture(scope="function")
def empty_wishlist_token(registro_api):
    """Cria um novo usuário que não possui nenhuma wishlist."""
    # 1. Cria usuário
    email = DataGenerator.generate_unique_email()
    password = DataGenerator.generate_strong_password()
    username = DataGenerator.generate_unique_username()
        
    # Passando o novo argumento
    registro_api.register_user(email, password, username)
        
    # 2. Loga para obter token
    login_response = registro_api.login_user(email, password)
    assert login_response.status_code == 200
    return login_response.json().get("access_token")

@pytest.fixture(scope="function")
def created_wishlist(unique_auth_token, wishlist_api):
    """Cria uma wishlist única para o token fornecido e retorna seu ID e token."""
    name = DataGenerator.generate_unique_wishlist_name()
    response = wishlist_api.create_wishlist(unique_auth_token, name)
    assert response.status_code == 200
    
    return {
        "id": response.json()["id"],
        "name": name,
        "token": unique_auth_token
    }

@pytest.fixture(scope="function")
def created_product(created_wishlist, wishlist_api):
    """Cria um produto na wishlist única e retorna o ID do produto, wishlist_id e token."""
    product_data = {
        "Product": "Test Product to Delete", 
        "Price": "100.00", 
        "Zipcode": "12345678",
        # NOVOS CAMPOS ADICIONADOS:
        "delivery_estimate": "5 dias úteis",  
        "shipping_fee": "10.50"               # Uma string ou o formato esperado pela API
    }
    response = wishlist_api.add_product_to_wishlist(
        created_wishlist["token"], 
        created_wishlist["id"], 
        product_data
    )
    
    # --- NOVO TRECHO DE DEBUG ---
    if response.status_code != 200:
        # Se o status não for 200, loga o código e o corpo para entender o 500
        log.error(f"Erro na fixture created_product. Status: {response.status_code}. Corpo: {response.text}")
    # --- FIM NOVO TRECHO DE DEBUG ---
    
    assert response.status_code == 200
    
    return {
        "id": response.json()["id"], 
        "wishlist_id": created_wishlist["id"],
        "token": created_wishlist["token"]
    }


#FIXTURE WEB

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