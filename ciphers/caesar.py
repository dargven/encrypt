"""
Шифр Цезаря
"""
from .base import BaseCipher
from .keygen import key_generator


class CaesarCipher(BaseCipher):
    """Реализация шифра Цезаря"""
    
    def __init__(self):
        super().__init__()
        self.name = "Шифр Цезаря"
        self.key_hint = "Подсказка: введите число (например, 3)"
        self.default_key = "3"
        self.cipher_type = "caesar"
    
    def encrypt(self, text: str, key: str) -> str:
        result = ""
        try:
            shift = int(key) % 33
        except ValueError:
            return "Ошибка: ключ должен быть числом"
        
        for char in text:
            if char.isalpha():
                # Английский алфавит
                if char.lower() in 'abcdefghijklmnopqrstuvwxyz':
                    base = ord('A') if char.isupper() else ord('a')
                    shifted = (ord(char) - base + shift) % 26 + base
                    result += chr(shifted)
                # Русский алфавит
                elif char.lower() in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя':
                    rus_lower = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
                    rus_upper = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
                    if char.islower():
                        idx = rus_lower.index(char)
                        result += rus_lower[(idx + shift) % 33]
                    else:
                        idx = rus_upper.index(char)
                        result += rus_upper[(idx + shift) % 33]
                else:
                    result += char
            else:
                result += char
        return result
    
    def decrypt(self, text: str, key: str) -> str:
        try:
            shift = int(key)
        except ValueError:
            return "Ошибка: ключ должен быть числом"
        return self.encrypt(text, str(-shift))
    
    def crack(self, text: str) -> str:
        """Взлом шифра Цезаря перебором всех ключей"""
        results = ["=== Все варианты расшифровки ===\n"]
        for key in range(1, 34):
            decrypted = self.decrypt(text, str(key))
            results.append(f"Ключ {key:2d}: {decrypted[:50]}...")
        return "\n".join(results)
    
    def generate_key(self) -> str:
        """Генерация случайного ключа"""
        return key_generator.generate_for_cipher(self.cipher_type)
