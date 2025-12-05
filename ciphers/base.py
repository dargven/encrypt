"""
Базовый класс для всех шифров
"""
from abc import ABC, abstractmethod


class BaseCipher(ABC):
    def __init__(self):
        self.name = "Базовый шифр"
        self.key_hint = "Введите ключ"
        self.default_key = ""
        self.cipher_type = "generic"
    
    @abstractmethod
    def encrypt(self, text: str, key: str) -> str:
        pass
    
    @abstractmethod
    def decrypt(self, text: str, key: str) -> str:
        pass
    
    @abstractmethod
    def crack(self, text: str) -> str:
        pass
    
    def generate_key(self) -> str:
        from .keygen import key_generator
        return key_generator.generate_for_cipher(self.cipher_type)
    
    def get_info(self) -> dict:
        return {
            "name": self.name,
            "key_hint": self.key_hint,
            "default_key": self.default_key
        }
