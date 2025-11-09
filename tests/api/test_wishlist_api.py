import pytest
from utils.data_generator import DataGenerator
from utils.logger import log


PRODUCT_BASE_DATA = {
    "Product": "Laptop Teste", 
    "Price": "1500.00", 
    "Zipcode": "99999999"
}

# TESTES DE WISHLIST (Cenários 14, 15, 16, 17, 18, 19)

@pytest.mark.api
def test_scenario_14_successful_create_wishlist(wishlist_api, unique_auth_token):
    """Scenario 14: Criação de wishlist bem-sucedida."""
    name = DataGenerator.generate_unique_wishlist_name()
    response = wishlist_api.create_wishlist(unique_auth_token, name)
    
    assert response.status_code == 200, f"Status esperado 200, obteve {response.status_code}"
    response_json = response.json()
    assert "id" in response_json
    assert response_json["name"] == name
    assert "owner_id" in response_json
    log.info(f"Cenário 14: Wishlist criada com sucesso: {name}.")

@pytest.mark.api
def test_scenario_15_create_wishlist_duplicate_name(wishlist_api, created_wishlist):
    """Scenario 15: Tentativa de criar wishlist com nome duplicado."""
    name = created_wishlist["name"]
    token = created_wishlist["token"]
    
    response = wishlist_api.create_wishlist(token, name)
    
    assert response.status_code == 409, f"Status esperado 409, obteve {response.status_code}"
    response_json = response.json()
    assert "A wishlist with this name already exists" in response_json.get("message", "")
    log.info(f"Cenário 15: Nome duplicado rejeitado (409 Conflict).")

@pytest.mark.api
def test_scenario_16_create_wishlist_unauthenticated(wishlist_api):
    """Scenario 16: Criação de wishlist sem autenticação."""
    name = DataGenerator.generate_unique_wishlist_name()
    # Enviando token inválido/vazio
    response = wishlist_api.create_wishlist("invalid_token_123", name) 
    
    assert response.status_code == 401, f"Status esperado 401, obteve {response.status_code}"
    log.info(f"Cenário 16: Criação sem autenticação rejeitada (401).")

@pytest.mark.api
def test_scenario_17_create_wishlist_invalid_data(api_client, wishlist_api, unique_auth_token):
    """Scenario 17: Criação de wishlist sem nome (dados inválidos/ausentes)."""
    headers = {"Authorization": f"Bearer {unique_auth_token}"}
    # Enviar corpo vazio
    response = api_client.post(wishlist_api.WISHLISTS_ENDPOINT, json_data={}, headers=headers)
    
    assert response.status_code == 422, f"Status esperado 422, obteve {response.status_code}"
    response_json = response.json()

    error_details = response_json.get("detail", {})

    # Adicionando robustez para lidar com detalhe que não é uma lista (como acontece no registro)
    if not isinstance(error_details, list):
        error_details = [{"msg": str(error_details)}]
        
    assert any("required" in error["msg"] for error in error_details) # ou "field required"
    log.info(f"Cenário 17: Dados inválidos/ausentes rejeitados (422).")

@pytest.mark.api
def test_scenario_18_retrieve_all_wishlists(wishlist_api, created_wishlist):
    """Scenario 18: Recuperar todas as wishlists do usuário."""
    token = created_wishlist["token"]
    
    response = wishlist_api.get_all_wishlists(token)
    
    assert response.status_code == 200, f"Status esperado 200, obteve {response.status_code}"
    response_json = response.json()
    assert isinstance(response_json, list)
    # Deve conter pelo menos a wishlist criada pela fixture
    assert len(response_json) >= 1 
    # Verifica se a wishlist recém-criada está na lista
    assert any(item["name"] == created_wishlist["name"] for item in response_json)
    log.info(f"Cenário 18: Recuperação de wishlists bem-sucedida.")

@pytest.mark.api
def test_scenario_19_retrieve_wishlists_when_none_exist(wishlist_api, empty_wishlist_token):
    """Scenario 19: Recuperar wishlists quando nenhuma existe (retorno array vazio)."""
    response = wishlist_api.get_all_wishlists(empty_wishlist_token)
    
    assert response.status_code == 200, f"Status esperado 200, obteve {response.status_code}"
    response_json = response.json()
    assert isinstance(response_json, list)
    assert len(response_json) == 0
    log.info(f"Cenário 19: Retorno array vazio para usuário sem wishlists.")

@pytest.mark.api
def test_scenario_20_retrieve_wishlists_unauthenticated(wishlist_api):
    """Scenario 20: Recuperar wishlists sem autenticação."""
    # Enviando token inválido/vazio
    response = wishlist_api.get_all_wishlists("invalid_token_123")
    
    assert response.status_code == 401, f"Status esperado 401, obteve {response.status_code}"
    log.info(f"Cenário 20: Recuperação sem autenticação rejeitada (401).")



# TESTES DE PRODUTO: ADICIONAR E LER (Cenários 21, 22, 23, 24, 25, 26, 27, 28)

@pytest.mark.api
def test_scenario_21_successful_add_product(wishlist_api, created_wishlist):
    """Scenario 21: Adição de produto bem-sucedida."""
    token = created_wishlist["token"]
    wishlist_id = created_wishlist["id"]
    
    response = wishlist_api.add_product_to_wishlist(token, wishlist_id, PRODUCT_BASE_DATA)
    
    assert response.status_code == 200, f"Status esperado 200, obteve {response.status_code}"
    response_json = response.json()
    assert "id" in response_json
    assert response_json["wishlist_id"] == wishlist_id
    assert response_json["Product"] == PRODUCT_BASE_DATA["Product"]
    assert response_json["is_purchased"] is False
    log.info(f"Cenário 21: Produto adicionado com sucesso.")

@pytest.mark.api
def test_scenario_22_add_product_non_existent_wishlist(wishlist_api, unique_auth_token):
    """Scenario 22: Adicionar produto a wishlist inexistente."""
    non_existent_id = 99999
    response = wishlist_api.add_product_to_wishlist(unique_auth_token, non_existent_id, PRODUCT_BASE_DATA)
    
    assert response.status_code == 404, f"Status esperado 404, obteve {response.status_code}"
    assert "Wishlist not found" in response.json().get("detail", "")
    log.info(f"Cenário 22: Wishlist inexistente rejeitada (404).")

@pytest.mark.api
def test_scenario_23_add_product_another_user_wishlist(registro_api, wishlist_api, created_wishlist):
    """Scenario 23: Adicionar produto a wishlist de outro usuário. (CORRIGIDO)"""
    
    response_login = registro_api.login_user("projeto@example.com", "Senha123!") 
    another_user_token = response_login.json()["access_token"]
    
    # Tenta adicionar produto à wishlist do 'created_wishlist' (que pertence a outro usuário)
    response = wishlist_api.add_product_to_wishlist(another_user_token, created_wishlist["id"], PRODUCT_BASE_DATA)
    
    # A API deve retornar 404 porque o ID da wishlist não existe para AQUELE usuário
    assert response.status_code == 404, f"Status esperado 404, obteve {response.status_code}"
    assert "Wishlist not found" in response.json().get("detail", "")
    log.info(f"Cenário 23: Adição à wishlist de outro usuário rejeitada (404).")

@pytest.mark.api
def test_scenario_24_add_product_incomplete_data(wishlist_api, created_wishlist):
    """Scenario 24: Adicionar produto com dados incompletos (missing required fields)."""
    incomplete_data = {"Price": "10.00"} # Faltando "Product"
    response = wishlist_api.add_product_to_wishlist(
        created_wishlist["token"], 
        created_wishlist["id"], 
        incomplete_data
    )
    
    assert response.status_code == 422, f"Status esperado 422, obteve {response.status_code}"
    response_json = response.json()
    
    error_details = response_json.get("detail", {})
    if not isinstance(error_details, list):
        error_details = [{"msg": str(error_details)}]
        
    assert any("required" in error["msg"] for error in error_details)
    log.info(f"Cenário 24: Dados incompletos rejeitados (422).")

@pytest.mark.api
def test_scenario_25_successful_retrieve_products(wishlist_api, created_product):
    """Scenario 25: Recuperação de produtos de uma wishlist."""
    token = created_product["token"]
    wishlist_id = created_product["wishlist_id"]
    
    response = wishlist_api.get_products_from_wishlist(token, wishlist_id)
    
    assert response.status_code == 200, f"Status esperado 200, obteve {response.status_code}"
    response_json = response.json()
    assert isinstance(response_json, list)
    assert len(response_json) >= 1
    # Verifica se o produto criado pela fixture está na lista
    assert any(item["id"] == created_product["id"] for item in response_json)
    log.info(f"Cenário 25: Recuperação de produtos bem-sucedida.")

@pytest.mark.api
def test_scenario_26_retrieve_products_filter_by_name(wishlist_api, created_wishlist):
    """Scenario 26: Filtragem de produtos por nome."""
    token = created_wishlist["token"]
    wishlist_id = created_wishlist["id"]
    
    # Adicionar um produto com nome específico
    specific_name = "Apple iPhone Teste"
    wishlist_api.add_product_to_wishlist(token, wishlist_id, {"Product": specific_name, "Price": "1000", "Zipcode": "12345678"})
    
    # Filtro: ?Product=iPhone
    response = wishlist_api.get_products_from_wishlist(token, wishlist_id, filters={"Product": "iPhone"})
    
    assert response.status_code == 200
    response_json = response.json()
    
    # Deve conter apenas produtos que incluem 'iPhone' no nome
    assert len(response_json) > 0
    assert all("iPhone" in item["Product"] for item in response_json)
    log.info(f"Cenário 26: Filtragem por nome bem-sucedida.")


@pytest.mark.api
def test_scenario_27_retrieve_products_filter_by_purchased_status(wishlist_api, created_product):
    """Scenario 27: Filtragem de produtos por status is_purchased."""
    token = created_product["token"]
    wishlist_id = created_product["wishlist_id"]
    product_id = created_product["id"]
    
    # 1. Marcar o produto criado pela fixture como COMPRADO
    wishlist_api.toggle_product_purchased(token, product_id)
    
    # 2. Filtrar por is_purchased=true
    response = wishlist_api.get_products_from_wishlist(token, wishlist_id, filters={"is_purchased": "true"})
    
    assert response.status_code == 200
    response_json = response.json()
    
    assert len(response_json) >= 1
    assert all(item["is_purchased"] is True for item in response_json)
    log.info(f"Cenário 27: Filtragem por status comprado bem-sucedida.")

@pytest.mark.api
def test_scenario_28_retrieve_products_another_user_wishlist(wishlist_api, created_wishlist, default_auth_token):
    """Scenario 28: Recuperar produtos de wishlist de outro usuário."""
    # default_auth_token é o 'outro' usuário
    response = wishlist_api.get_products_from_wishlist(default_auth_token, created_wishlist["id"])
    
    # A API deve retornar 404 porque o ID da wishlist não existe para o default_auth_token
    assert response.status_code == 404, f"Status esperado 404, obteve {response.status_code}"
    assert "Wishlist not found" in response.json().get("detail", "")
    log.info(f"Cenário 28: Recuperação de produtos de outro usuário rejeitada (404).")

# TESTES DE PRODUTO: ATUALIZAR (Cenários 29, 30, 31)

@pytest.mark.api
def test_scenario_29_successful_update_product(wishlist_api, created_product):
    """Scenario 29: Atualização de produto bem-sucedida."""
    update_data = {"Price": "9999.99", "Zipcode": "11111111"}
    token = created_product["token"]
    product_id = created_product["id"]
    
    response = wishlist_api.update_product(token, product_id, update_data)
    
    assert response.status_code == 200, f"Status esperado 200, obteve {response.status_code}"
    response_json = response.json()
    assert response_json["Price"] == "9999.99"
    log.info(f"Cenário 29: Atualização de produto bem-sucedida.")

@pytest.mark.api
def test_scenario_30_update_non_existent_product(wishlist_api, unique_auth_token):
    """Scenario 30: Atualizar produto inexistente."""
    non_existent_id = 99999
    update_data = {"Price": "1.00"}
    response = wishlist_api.update_product(unique_auth_token, non_existent_id, update_data)
    
    assert response.status_code == 404, f"Status esperado 404, obteve {response.status_code}"
    assert "Product not found" in response.json().get("detail", "")
    log.info(f"Cenário 30: Atualização de produto inexistente rejeitada (404).")

@pytest.mark.api
def test_scenario_31_update_another_user_product(wishlist_api, created_product, default_auth_token):
    """Scenario 31: Atualizar produto de outro usuário."""
    product_id = created_product["id"]
    update_data = {"Price": "1.00"}
    
    # default_auth_token é o 'outro' usuário
    response = wishlist_api.update_product(default_auth_token, product_id, update_data)
    
    # A API deve retornar 404 porque o ID do produto não existe para AQUELE usuário
    assert response.status_code == 404, f"Status esperado 404, obteve {response.status_code}"
    assert "Product not found" in response.json().get("detail", "")
    log.info(f"Cenário 31: Atualização de produto de outro usuário rejeitada (404).")

# ----------------------------------------
# TESTES DE PRODUTO: DELETAR (Cenários 32, 33, 34)
# ----------------------------------------

@pytest.mark.api
def test_scenario_32_successful_delete_product(wishlist_api, created_product):
    """Scenario 32: Deleção de produto bem-sucedida."""
    token = created_product["token"]
    product_id = created_product["id"]
    
    response = wishlist_api.delete_product(token, product_id)
    
    # O código esperado para deleção bem-sucedida sem conteúdo de retorno é 204 No Content
    assert response.status_code == 204, f"Status esperado 204, obteve {response.status_code}"
    
    # Verifica que o produto realmente sumiu (GET deve retornar 404 ou lista vazia)
    response_get = wishlist_api.get_products_from_wishlist(token, created_product["wishlist_id"])
    # Verifica se a lista de produtos recuperada NÃO contém o ID do produto excluído
    assert not any(item["id"] == product_id for item in response_get.json())
    log.info(f"Cenário 32: Deleção de produto bem-sucedida (204).")


@pytest.mark.api
def test_scenario_33_delete_non_existent_product(wishlist_api, unique_auth_token):
    """Scenario 33: Deletar produto inexistente."""
    non_existent_id = 99999
    response = wishlist_api.delete_product(unique_auth_token, non_existent_id)
    
    assert response.status_code == 404, f"Status esperado 404, obteve {response.status_code}"
    assert "Product not found" in response.json().get("detail", "")
    log.info(f"Cenário 33: Deleção de produto inexistente rejeitada (404).")

@pytest.mark.api
def test_scenario_34_delete_another_user_product(wishlist_api, created_product, default_auth_token):
    """Scenario 34: Deletar produto de outro usuário."""
    product_id = created_product["id"]
    
    # default_auth_token é o 'outro' usuário
    response = wishlist_api.delete_product(default_auth_token, product_id)
    
    # A API deve retornar 404 porque o ID do produto não existe para AQUELE usuário
    assert response.status_code == 404, f"Status esperado 404, obteve {response.status_code}"
    assert "Product not found" in response.json().get("detail", "")
    log.info(f"Cenário 34: Deleção de produto de outro usuário rejeitada (404).")



# TESTES GERAIS DE AUTENTICAÇÃO (Cenários 35, 36)

# Lista de TUPLAS que definem a chamada do endpoint:
# (Função de Serviço, Argumentos necessários (além do token))
ENDPOINT_CALLS = [
    # POST /wishlists
    (lambda api, token: api.create_wishlist(token, DataGenerator.generate_unique_wishlist_name())), 
    
    # GET /wishlists
    (lambda api, token: api.get_all_wishlists(token)), 
    
    # POST /wishlists/{id}/products (Usamos um ID fictício para este teste)
    (lambda api, token: api.add_product_to_wishlist(token, 1, PRODUCT_BASE_DATA)), 
    
    # GET /wishlists/{id}/products
    (lambda api, token: api.get_products_from_wishlist(token, 1)), 
    
    # PUT /products/{id}
    (lambda api, token: api.update_product(token, 1, {"Price": "1.00"})), 
    
    # DELETE /products/{id}
    (lambda api, token: api.delete_product(token, 1)), 

    # PATCH/PUT /products/{id}/toggle
    (lambda api, token: api.toggle_product_purchased(token, 1)),
]
@pytest.mark.api
@pytest.mark.parametrize("api_call", ENDPOINT_CALLS)
def test_scenario_35_access_endpoint_without_token(api_call, wishlist_api):
    """Scenario 35: Acessar endpoints protegidos sem token."""
    
    # passei wishlist_api como 'api' e um token inválido como 'token'
    # 'invalid_token_format' no conftest está sendo usado para simular a ausência
    response = api_call(wishlist_api, "invalid_token_format") 
    
    assert response.status_code == 401, f"Endpoint {response.request.path} - Status esperado 401, obteve {response.status_code}"
    # O token "invalid_token_format" normalmente é interpretado como "Not authenticated" ou malformado.
    expected_messages = ["Not authenticated", "Could not validate credentials"]

    assert any(msg in response.json().get("detail", "") for msg in expected_messages)
    log.info(f"Cenário 35: Acesso sem autenticação rejeitado (401).")

@pytest.mark.api
@pytest.mark.parametrize("api_call", ENDPOINT_CALLS)
def test_scenario_36_access_endpoint_with_invalid_token(api_call, wishlist_api):
    """Scenario 36: Acessar endpoints protegidos com token inválido/malformado."""
    # Usamos um token JWT malformado
    invalid_token = "invalid.malformed.token.123"
    
    # A chamada de função é refeita com um token inválido
    response = api_call(wishlist_api, invalid_token)
    
    assert response.status_code == 401, f"Endpoint {response.request.url} - Status esperado 401, obteve {response.status_code}"
    # Mensagem de erro esperada para token inválido/expirado
    detail = response.json().get("detail", "")
    assert any(msg in detail for msg in ["Could not validate credentials", "Token has expired", "Not authenticated"])
    log.info(f"Cenário 36: Acesso com token inválido rejeitado (401).")