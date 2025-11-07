# aut-americanas/utils/data_generator.py
import time
import uuid
import random
import string

class DataGenerator:
    
    @staticmethod
    def generate_unique_email():
        """Gera um e-mail único usando timestamp e UUID."""
        timestamp = int(time.time() * 1000)
        unique_id = str(uuid.uuid4())[:6] 
        return f"api_test_{unique_id}_{timestamp}@testmail.com"

    @staticmethod
    def generate_unique_username(): # ⬅️ ADICIONADO
        """Gera um nome de usuário único."""
        unique_id = str(uuid.uuid4())[:8].replace('-', '') # Limita e remove traços
        timestamp = int(time.time())
        return f"user_{unique_id}_{timestamp}"
    
    @staticmethod
    def generate_unique_wishlist_name():
        """Gera um nome de wishlist único."""
        unique_id = str(uuid.uuid4())[:4]
        return f"Wishlist_{unique_id}_{int(time.time())}"

    @staticmethod
    def generate_strong_password(length=10):
        """Gera uma senha forte com minúsculas, maiúsculas, dígitos e símbolos."""
        
        # Garante que pelo menos um caractere de cada tipo esteja presente
        lower = string.ascii_lowercase
        upper = string.ascii_uppercase
        digits = string.digits
        symbols = string.punctuation
        
        # Cria a string base de todos os caracteres permitidos
        all_chars = lower + upper + digits + symbols
        
        # Garante a inclusão de pelo menos 1 de cada tipo
        password = [
            random.choice(lower),
            random.choice(upper),
            random.choice(digits),
            random.choice(symbols)
        ]
        
        # Preenche o restante da senha com caracteres aleatórios
        password += random.choices(all_chars, k=length - len(password))
        
        # Embaralha a lista para que a ordem seja aleatória
        random.shuffle(password)
        
        return "".join(password)