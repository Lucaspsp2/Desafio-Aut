# aut-americanas/utils/api_client.py
import requests
from utils.logger import log

class APIClient:
    """Cliente HTTP básico configurado para interagir com a Wishlist API."""
    
    BASE_URL = "http://127.0.0.1:8000"

    def __init__(self):
        # A sessão persistente é útil para manter cookies ou configurações, embora não seja estritamente necessário para JWT.
        self.session = requests.Session()
        log.info(f"Cliente API inicializado, base: {self.BASE_URL}")

    def post(self, endpoint, json_data=None, headers=None):
        url = f"{self.BASE_URL}{endpoint}"
        log.info(f"API POST: {endpoint}")
        return self.session.post(url, json=json_data, headers=headers)

    def get(self, endpoint, params=None, headers=None):
        url = f"{self.BASE_URL}{endpoint}"
        log.info(f"API GET: {endpoint}")
        return self.session.get(url, params=params, headers=headers)

    def put(self, endpoint, json_data=None, headers=None):
        url = f"{self.BASE_URL}{endpoint}"
        log.info(f"API PUT: {endpoint}")
        return self.session.put(url, json=json_data, headers=headers)

    def delete(self, endpoint, headers=None):
        url = f"{self.BASE_URL}{endpoint}"
        log.info(f"API DELETE: {endpoint}")
        return self.session.delete(url, headers=headers)