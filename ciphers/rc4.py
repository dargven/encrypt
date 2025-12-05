"""
Потоковый шифр RC4 (Rivest Cipher 4)
Реализация с нуля без использования криптографических библиотек
"""
from .base import BaseCipher
from .keygen import key_generator


class RC4Cipher(BaseCipher):
    """Реализация потокового шифра RC4"""
    
    def __init__(self):
        super().__init__()
        self.name = "Потоковый шифр RC4"
        self.key_hint = "Подсказка: hex-ключ (например, 1A2B3C4D5E6F)"
        self.default_key = "SECRET"
        self.cipher_type = "rc4"
    
    def _ksa(self, key: bytes) -> list:
        """Key Scheduling Algorithm - инициализация S-блока"""
        S = list(range(256))
        j = 0
        
        for i in range(256):
            j = (j + S[i] + key[i % len(key)]) % 256
            S[i], S[j] = S[j], S[i]
        
        return S
    
    def _prga(self, S: list, length: int) -> list:
        """Pseudo-Random Generation Algorithm - генерация потока ключей"""
        i = 0
        j = 0
        keystream = []
        
        for _ in range(length):
            i = (i + 1) % 256
            j = (j + S[i]) % 256
            S[i], S[j] = S[j], S[i]
            K = S[(S[i] + S[j]) % 256]
            keystream.append(K)
        
        return keystream
    
    def _prepare_key(self, key: str) -> bytes:
        """Подготовка ключа из строки"""
        # Пробуем интерпретировать как hex
        clean_key = key.replace(" ", "").upper()
        if all(c in "0123456789ABCDEF" for c in clean_key) and len(clean_key) % 2 == 0:
            try:
                return bytes(int(clean_key[i:i+2], 16) for i in range(0, len(clean_key), 2))
            except:
                pass
        
        # Иначе используем как ASCII
        return key.encode('utf-8')
    
    def encrypt(self, text: str, key: str) -> str:
        """Шифрование текста алгоритмом RC4"""
        if not key:
            return "Ошибка: введите ключ"
        
        key_bytes = self._prepare_key(key)
        if len(key_bytes) == 0:
            return "Ошибка: недопустимый ключ"
        
        text_bytes = text.encode('utf-8')
        
        S = self._ksa(key_bytes)
        keystream = self._prga(S, len(text_bytes))
        
        # XOR текста с потоком ключей
        cipher_bytes = bytes(t ^ k for t, k in zip(text_bytes, keystream))
        
        # Результат в hex формате
        return cipher_bytes.hex().upper()
    
    def decrypt(self, hex_text: str, key: str) -> str:
        """Расшифровка текста алгоритмом RC4 (RC4 симметричен)"""
        if not key:
            return "Ошибка: введите ключ"
        
        # Очистка hex строки
        hex_text = hex_text.replace(" ", "").replace("\n", "").upper()
        
        # Проверка на валидный hex
        if not all(c in "0123456789ABCDEF" for c in hex_text):
            return "Ошибка: введите зашифрованный текст в hex формате"
        
        if len(hex_text) % 2 != 0:
            return "Ошибка: неверная длина hex строки"
        
        try:
            cipher_bytes = bytes(int(hex_text[i:i+2], 16) for i in range(0, len(hex_text), 2))
        except:
            return "Ошибка: неверный hex формат"
        
        key_bytes = self._prepare_key(key)
        if len(key_bytes) == 0:
            return "Ошибка: недопустимый ключ"
        
        S = self._ksa(key_bytes)
        keystream = self._prga(S, len(cipher_bytes))
        
        # XOR с потоком ключей (расшифровка = шифрование для RC4)
        plain_bytes = bytes(c ^ k for c, k in zip(cipher_bytes, keystream))
        
        try:
            return plain_bytes.decode('utf-8')
        except UnicodeDecodeError:
            return "Ошибка: не удалось декодировать результат (неверный ключ?)"
    
    def crack(self, hex_text: str) -> str:
        result = []

        common_keys = ["SECRET", "password", "key", "1234", "admin", "test"]
        hex_text = hex_text.replace(" ", "").replace("\n", "").upper()
        
        for test_key in common_keys:
            try:
                decrypted = self.decrypt(hex_text, test_key)
                if not decrypted.startswith("Ошибка"):
                    # Проверяем на читаемость
                    if all(31 < ord(c) < 128 or c in '\n\r\t' for c in decrypted[:20] if c):
                        result.append(f"Ключ '{test_key}': {decrypted[:50]}...")
                    else:
                        result.append(f"Ключ '{test_key}': [нечитаемый результат]")
                else:
                    result.append(f"Ключ '{test_key}': [ошибка]")
            except:
                result.append(f"Ключ '{test_key}': [ошибка]")
        
        return "\n".join(result)
    
    def generate_key(self) -> str:
        """Генерация случайного ключа"""
        return key_generator.generate_for_cipher(self.cipher_type)
