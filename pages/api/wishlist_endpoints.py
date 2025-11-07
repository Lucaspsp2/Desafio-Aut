# aut-americanas/pages/api/wishlist_endpoints.py
from utils.api_client import APIClient

class WishlistEndpoints:
    """Encapsula a lógica de requisições para os endpoints de Wishlists e Produtos."""
    
    WISHLISTS_ENDPOINT = "/wishlists"
    PRODUCTS_ENDPOINT = "/products"
    
    def __init__(self, client: APIClient):
        self.client = client
        
    # --- Métodos de Wishlist (Cenários 14, 15, 17, 18, 19) ---

    def create_wishlist(self, token, name):
        """Cenário 14: Cria uma nova wishlist."""
        headers = {"Authorization": f"Bearer {token}"}
        payload = {"name": name}
        return self.client.post(self.WISHLISTS_ENDPOINT, json_data=payload, headers=headers)

    def get_all_wishlists(self, token):
        """Cenário 18, 19: Retorna todas as wishlists do usuário."""
        headers = {"Authorization": f"Bearer {token}"}
        return self.client.get(self.WISHLISTS_ENDPOINT, headers=headers)
    
    # --- Métodos de Produto (Cenários 21, 25, 26, 27) ---
    
    def add_product_to_wishlist(self, token, wishlist_id, product_data):
        """Cenário 21: Adiciona um produto a uma wishlist específica."""
        headers = {"Authorization": f"Bearer {token}"}
        endpoint = f"{self.WISHLISTS_ENDPOINT}/{wishlist_id}/products"
        return self.client.post(endpoint, json_data=product_data, headers=headers)
        
    def get_products_from_wishlist(self, token, wishlist_id, filters=None):
        """Cenário 25, 26, 27: Retorna produtos da wishlist, opcionalmente com filtros."""
        headers = {"Authorization": f"Bearer {token}"}
        endpoint = f"{self.WISHLISTS_ENDPOINT}/{wishlist_id}/products"
        return self.client.get(endpoint, params=filters, headers=headers)

    # --- Métodos de Ação em Produto (Cenários 29, 32) ---
    
    def update_product(self, token, product_id, update_data):
        """Cenário 29: Atualiza detalhes de um produto existente."""
        headers = {"Authorization": f"Bearer {token}"}
        endpoint = f"{self.PRODUCTS_ENDPOINT}/{product_id}"
        return self.client.put(endpoint, json_data=update_data, headers=headers)
        
    def delete_product(self, token, product_id):
        """Cenário 32: Deleta um produto."""
        headers = {"Authorization": f"Bearer {token}"}
        endpoint = f"{self.PRODUCTS_ENDPOINT}/{product_id}"
        return self.client.delete(endpoint, headers=headers)

    def toggle_product_purchased(self, token, product_id):
        """Alterna o status is_purchased (Cenário 35/36 - PATCH)"""
        headers = {"Authorization": f"Bearer {token}"}
        endpoint = f"{self.PRODUCTS_ENDPOINT}/{product_id}/toggle"
        # O endpoint PATCH geralmente não precisa de corpo, a ação está na URL.
        return self.client.put(endpoint, headers=headers) # Assumindo que a API usa PUT em vez de PATCH