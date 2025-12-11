"""
Алгоритм RSA (Rivest-Shamir-Adleman)
"""
import random
from typing import re

from .base import BaseCipher


class RSACipher(BaseCipher):
    """Реализация асимметричного шифра RSA"""

    def __init__(self):
        super().__init__()
        self.name = "Алгоритм RSA"
        self.key_hint = "Подсказка: публичный ключ (e,n), например: 65537,3233"
        self.default_key = ""
        self.cipher_type = "rsa"

        # Сохраняем последнюю пару ключей
        self.last_public_key = None
        self.last_private_key = None

    def _is_prime(self, n: int, k: int = 5) -> bool:
        """Тест Миллера-Рабина на простоту"""
        if n < 2:
            return False
        if n == 2 or n == 3:
            return True
        if n % 2 == 0:
            return False

        # Представляем n-1 как 2^r * d
        r, d = 0, n - 1
        while d % 2 == 0:
            r += 1
            d //= 2

        for _ in range(k):
            a = random.randrange(2, n - 1)
            x = pow(a, d, n)

            if x == 1 or x == n - 1:
                continue

            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False

        return True

    def _generate_prime(self, bits: int = 16) -> int:
        while True:
            num = random.getrandbits(bits)
            num |= (1 << bits - 1) | 1
            if self._is_prime(num):
                return num

    def _gcd(self, a: int, b: int) -> int:
        while b:
            a, b = b, a % b
        return a

    def _extended_gcd(self, a: int, b: int) -> tuple:
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = self._extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y

    def _mod_inverse(self, e: int, phi: int) -> int:
        gcd, x, _ = self._extended_gcd(e, phi)
        if gcd != 1:
            raise ValueError("Обратный элемент не существует")
        return x % phi

    def generate_keypair(self, bits: int = 16) -> tuple:
        """
        Генерация пары ключей RSA
        Возвращает: ((e, n), (d, n))
        """
        p = self._generate_prime(bits)
        q = self._generate_prime(bits)

        n = p * q
        phi = (p - 1) * (q - 1)

        e = 65537  # Стандартное значение
        if e >= phi or self._gcd(e, phi) != 1:
            e = 3
            while self._gcd(e, phi) != 1:
                e += 2

        d = self._mod_inverse(e, phi)

        # Сохраняем ключи
        self.last_public_key = (e, n)
        self.last_private_key = (d, n)

        return ((e, n), (d, n))

    def _parse_key(self, key_str: str) -> tuple:
        try:
            parts = key_str.replace(" ", "").split(",")
            if len(parts) != 2:
                return None, None
            return int(parts[0]), int(parts[1])
        except:
            return None, None

    def _text_to_numbers(self, text: str) -> list:
        return [ord(char) for char in text]

    def _numbers_to_text(self, numbers: list) -> str:
        try:
            return ''.join(chr(num) for num in numbers)
        except:
            return "[Ошибка декодирования]"

    def encrypt(self, text: str, key: str) -> str:
        if not text:
            return "Ошибка: введите текст"

        if not key:
            public_key, private_key = self.generate_keypair()
            e, n = public_key
            info = f"Сгенерированы новые ключи:\nПубличный (для шифрования): {e},{n}\nПриватный (для расшифровки): {private_key[0]},{private_key[1]}\n\n"
        else:
            e, n = self._parse_key(key)
            if e is None or n is None:
                return "Ошибка: неверный формат ключа. Используйте формат: e,n"
            info = ""

        numbers = self._text_to_numbers(text)

        if any(num >= n for num in numbers):
            return f"Ошибка: некоторые символы имеют код ≥ n={n}. Используйте большее значение n"

        encrypted = [pow(m, e, n) for m in numbers]

        result = info + "Зашифрованные числа:\n" + " ".join(str(c) for c in encrypted)
        return result

    def decrypt(self, text: str, key: str) -> str:
        if not text:
            return "Ошибка: введите зашифрованный текст"

        if not key:
            return "Ошибка: введите приватный ключ (d,n)"

        d, n = self._parse_key(key)
        if d is None or n is None:
            return "Ошибка: неверный формат ключа. Используйте формат: d,n"

        try:
            lines = text.strip().split('\n')
            numbers_line = lines[-1]

            encrypted = [int(x) for x in numbers_line.split()]

            decrypted = [pow(c, d, n) for c in encrypted]

            result_text = self._numbers_to_text(decrypted)

            if all(32 <= ord(c) <= 126 or c in '\n\r\t' for c in result_text):
                return f"Расшифровано успешно:\n{result_text}"
            else:
                return f"УЧЕБНЫЙ РЕЖИМ: Расшифровка с текущим ключом:\n{result_text}\n\n💡 Подсказка: Возможно, это неправильный ключ. Попробуйте приватный ключ (d,n)."

        except Exception as e:
            return f"Ошибка расшифровки: {str(e)}\n\n💡 Убедитесь, что используете правильный формат ключа (d,n)"

    def crack(self, text: str) -> str:
        """Взлом RSA (факторизация малых n)"""
        result = ["=== ВЗЛОМ RSA ===\n"]

        try:
            lines = text.strip().split('\n')

            public_key_line = None
            for line in lines:
                if 'Публичный' in line or 'публичный' in line:
                    public_key_line = line
                    break

            if not public_key_line and self.last_public_key:
                e, n = self.last_public_key
                result.append(f"Используем последний публичный ключ: e={e}, n={n}\n")
            elif public_key_line:
                # Извлекаем e и n
                numbers = re.findall(r'\d+', public_key_line)
                if len(numbers) >= 2:
                    e = int(numbers[0])
                    n = int(numbers[1])
                else:
                    result.append("Не удалось извлечь публичный ключ из текста")
                    return "\n".join(result)
            else:
                result.append("Для взлома нужен публичный ключ (e,n)")
                return "\n".join(result)

            result.append(f"Анализ публичного ключа:")
            result.append(f"   e = {e}")
            result.append(f"   n = {n}")
            result.append(f"   Битность n: ~{n.bit_length()} бит\n")

            result.append("Попытка факторизации n...\n")

            if n < 10000000:
                p, q = self._factorize(n)
                if p and q:
                    result.append(f"Успешная факторизация!")
                    result.append(f"   p = {p}")
                    result.append(f"   q = {q}")
                    result.append(f"   Проверка: p × q = {p * q} {'✓' if p * q == n else '✗'}\n")

                    phi = (p - 1) * (q - 1)
                    d = self._mod_inverse(e, phi)
                    result.append(f"Вычислен приватный ключ!")
                    result.append(f"   φ(n) = (p-1)(q-1) = {phi}")
                    result.append(f"   d = {d}")
                    result.append(f"\n Приватный ключ для расшифровки: {d},{n}\n")

                    # Пробуем расшифровать
                    decrypted = self.decrypt(text, f"{d},{n}")
                    if not decrypted.startswith("Ошибка") and not decrypted.startswith(""):
                        result.append(f"Расшифрованный текст:\n{decrypted}")
                else:
                    result.append("Факторизация не удалась (возможно, n - простое число)")
            else:
                result.append(f"Модуль n={n} слишком велик для учебной факторизации")

        except Exception as e:
            result.append(f"Ошибка анализа: {str(e)}")

        return "\n".join(result)

    def _factorize(self, n: int) -> tuple:
        if n < 2:
            return None, None

        for i in range(2, min(int(n ** 0.5) + 1, 1000000)):
            if n % i == 0:
                return i, n // i

        return None, None

    def generate_key(self) -> str:

        public_key, private_key = self.generate_keypair(bits=16)
        e, n = public_key
        d, _ = private_key

        return f"{e},{n}|{d},{n}"
