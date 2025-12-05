"""
Модуль генерации случайных ключей для шифров
"""
import random
import string
import time


class KeyGenerator:
    """Генератор случайных ключей для различных алгоритмов"""
    
    def __init__(self):
        # Инициализация PRNG текущим временем
        random.seed(time.time())
    
    def generate_numeric(self, min_val: int = 1, max_val: int = 33) -> str:
        """Генерация числового ключа (для шифра Цезаря)"""
        return str(random.randint(min_val, max_val))
    
    def generate_alphabetic(self, length: int = 8, uppercase: bool = True) -> str:
        """Генерация буквенного ключа (для Квадроинженера)"""
        chars = string.ascii_uppercase if uppercase else string.ascii_lowercase
        return ''.join(random.choice(chars) for _ in range(length))
    
    def generate_two_words(self, length1: int = 6, length2: int = 6) -> str:
        """Генерация двух слов-ключей (для Квадроинженера)"""
        word1 = self.generate_alphabetic(length1)
        word2 = self.generate_alphabetic(length2)
        return f"{word1} {word2}"
    
    def generate_bytes(self, length: int = 8) -> str:
        """Генерация ключа из печатных символов (для DES)"""
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(length))
    
    def generate_hex(self, length: int = 16) -> str:
        """Генерация hex-ключа (для потокового шифра)"""
        return ''.join(random.choice('0123456789ABCDEF') for _ in range(length))
    
    def generate_for_cipher(self, cipher_type: str) -> str:
        """Генерация ключа для конкретного типа шифра"""
        generators = {
            "caesar": lambda: self.generate_numeric(1, 33),
            "foursquare": lambda: self.generate_two_words(6, 6),
            "des": lambda: self.generate_bytes(8),
            "rc4": lambda: self.generate_hex(16),
        }
        
        generator = generators.get(cipher_type, lambda: self.generate_bytes(8))
        return generator()


key_generator = KeyGenerator()
