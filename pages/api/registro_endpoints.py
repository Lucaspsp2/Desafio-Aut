from utils.api_client import APIClient

class RegistroEndpoints:
    """Encapsula a lógica de requisições para os endpoints de Registro e Login."""
    
    REGISTER_ENDPOINT = "/auth/register"
    LOGIN_ENDPOINT = "/auth/login"

    def __init__(self, client: APIClient):
        self.client = client

    # Cenário 8, 9, 10 (Registro)
    def register_user(self, email, password, username): 
        """Envia requisição para registrar um novo usuário."""
        payload = {
            "email": email, 
            "password": password,
            "username": username 
        }
        return self.client.post(self.REGISTER_ENDPOINT, json_data=payload)
                                
    # Cenário 11, 12, 13 (Login)
    def login_user(self, email, password):
        """Envia requisição para autenticar um usuário."""
        payload = {"email": email, "password": password}
        return self.client.post(self.LOGIN_ENDPOINT, json_data=payload)