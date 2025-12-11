"""
Криптографические хэш-функции
Реализация MD5, SHA-1, SHA-256
"""
import math
import struct

from .base import BaseCipher


class HashFunctions(BaseCipher):

    def __init__(self):
        super().__init__()
        self.name = "Хэш-функции"
        self.key_hint = "Подсказка: выберите алгоритм - md5, sha1 или sha256"
        self.default_key = "sha256"
        self.cipher_type = "hash"

    def encrypt(self, text: str, key: str) -> str:
        """Вычисление хэша текста"""
        if not text:
            return "Ошибка: введите текст"

        # 🤖 ПАСХАЛКА: Киборги лучшие!
        if "киборг" in text.lower() or "cyborg" in text.lower():
            easter_egg = """
     ПАСХАЛКА ОБНАРУЖЕНА! 
    
         ╔═══╗
         ║ ◉ ◉ ║
         ║  ▽  ║   
         ╚═══╝
        ╱┃   ┃╲
       ╱ ┃   ┃ ╲
      ╱  ┗━━━┛  ╲
     
     КИБОРГИ ЛУЧШИЕ! 
    
    Продолжаем хэширование...
    
    ═══════════════════════════
    
"""
        else:
            easter_egg = ""

        algorithm = key.lower().strip() if key else "sha256"

        if algorithm == "md5":
            hash_value = self._md5(text)
            algo_name = "MD5"
        elif algorithm == "sha1" or algorithm == "sha-1":
            hash_value = self._sha1(text)
            algo_name = "SHA-1"
        elif algorithm == "sha256" or algorithm == "sha-256":
            hash_value = self._sha256(text)
            algo_name = "SHA-256"
        else:
            return f"Ошибка: неизвестный алгоритм '{algorithm}'. Используйте: md5, sha1, sha256"

        result = easter_egg
        result += f" Алгоритм: {algo_name}\n"
        result += f" Входной текст: {text[:50]}{'...' if len(text) > 50 else ''}\n"
        result += f"Длина текста: {len(text)} символов\n\n"
        result += f"Хэш ({algo_name}):\n{hash_value}\n\n"
        result += self._analyze_hash(hash_value, text, algorithm)

        return result

    def decrypt(self, text: str, key: str) -> str:
        """
        Хэш-функции необратимы, но в учебных целях можем попробовать найти коллизии
        """
        if not text:
            return "Ошибка: введите хэш для анализа"

        # Извлекаем хэш из текста
        hash_value = None
        lines = text.strip().split('\n')
        for line in lines:
            line = line.strip()
            if len(line) in [32, 40, 64] and all(c in '0123456789abcdefABCDEF' for c in line):
                hash_value = line.lower()
                break

        if not hash_value:
            return ("ВНИМАНИЕ: Хэш-функции необратимы!\n\n"
                    "Невозможно восстановить исходный текст из хэша.\n"
                    "Можно:\n"
                    "1. Ввести хэш в поле 'Текст'\n"
                    "2. Нажать 'Проверить' для попытки найти простые коллизии\n"
                    "3. Использовать кнопку 'Взломать' для словарной атаки")

        hash_len = len(hash_value)
        if hash_len == 32:
            algo = "md5"
        elif hash_len == 40:
            algo = "sha1"
        elif hash_len == 64:
            algo = "sha256"
        else:
            return "Неизвестный формат хэша"

        result = ["===АНАЛИЗ ХЭША ===\n"]
        result.append(f"Обнаружен {algo.upper()} хэш")
        result.append(f"Значение: {hash_value}\n")
        result.append("️Попытка найти простые коллизии...\n")

        # Пробуем простые варианты
        simple_tests = [
            "", "0", "1", "test", "hello", "password",
            "a", "abc", "123", "admin", "root"
        ]

        found = False
        for test_word in simple_tests:
            test_hash = self._compute_hash(test_word, algo)
            if test_hash == hash_value:
                result.append(f"НАЙДЕНО СОВПАДЕНИЕ!")
                result.append(f"Исходный текст: '{test_word}'")
                found = True
                break

        if not found:
            result.append("Простые коллизии не найдены")
            result.append("\n Попробуйте кнопку 'Взломать' для полного перебора")

        return "\n".join(result)

    def crack(self, text: str) -> str:
        """Взлом хэша методом перебора/словаря"""
        result = ["===  ВЗЛОМ ХЭША ===\n"]

        # Извлекаем хэш из текста
        hash_value = None
        lines = text.strip().split('\n')
        for line in lines:
            line = line.strip()
            if len(line) in [32, 40, 64] and all(c in '0123456789abcdefABCDEF' for c in line):
                hash_value = line.lower()
                break

        if not hash_value:
            result.append(" Не удалось найти хэш в тексте.")
            return "\n".join(result)

        # Определяем тип хэша по длине
        hash_len = len(hash_value)
        if hash_len == 32:
            algo = "md5"
            algo_name = "MD5"
        elif hash_len == 40:
            algo = "sha1"
            algo_name = "SHA-1"
        elif hash_len == 64:
            algo = "sha256"
            algo_name = "SHA-256"
        else:
            result.append(f" Неизвестная длина хэша: {hash_len}")
            return "\n".join(result)

        result.append(f" Обнаружен хэш: {algo_name}")
        result.append(f" Значение: {hash_value}\n")

        # Словарь для перебора (расширенный)
        dictionary = [
            "password", "123456", "12345678", "qwerty", "abc123",
            "password1", "admin", "letmein", "welcome", "monkey",
            "hello", "world", "test", "user", "master",
            "secret", "root", "pass", "1234", "password123",
            "киборги", "cyborg", "robot", "ai", "crypto",
            "", "a", "1", "0", "123"
        ]

        result.append(" АТАКА ПО СЛОВАРЮ")
        result.append(f"   Проверка {len(dictionary)} популярных паролей...\n")

        attempts = []
        found = False
        for word in dictionary:
            test_hash = self._compute_hash(word, algo)
            if test_hash == hash_value:
                result.append(f" НАЙДЕНО СОВПАДЕНИЕ!")
                result.append(f"Исходный текст: '{word}'")
                result.append(f"Хэш: {test_hash}")
                found = True
                break

        if not found:
            result.append(" Совпадений в словаре не найдено\n")

            result.append("БРУТФОРС (короткие строки)")
            result.append("   Проверка цифровых комбинаций...\n")

            for i in range(10000):
                word = str(i).zfill(4)
                test_hash = self._compute_hash(word, algo)
                if test_hash == hash_value:
                    result.append(f"НАЙДЕНО СОВПАДЕНИЕ!")
                    result.append(f" Исходный текст: '{word}'")
                    found = True
                    break

            if not found:
                result.append(" Совпадений не найдено\n")
                result.append("АСШИРЕННЫЙ ПЕРЕБОР")
                result.append("Проверка букв и коротких слов...\n")

                # Проверяем одиночные символы и короткие комбинации
                import string
                for char in string.ascii_lowercase[:10]:
                    test_hash = self._compute_hash(char, algo)
                    if test_hash == hash_value:
                        result.append(f"НАЙДЕНО: '{char}'")
                        found = True
                        break

        result.append(f"\n{'=' * 40}")
        result.append("СТАТИСТИКА")
        result.append(f"{'=' * 40}")
        result.append(f"• Длина хэша: {hash_len} символов")
        result.append(f"• Возможных значений: 16^{hash_len} ≈ 2^{hash_len * 4}")
        result.append(
            f"• Стойкость к коллизиям: {'Слабая' if algo == 'md5' else '️ Средняя' if algo == 'sha1' else ' Высокая'}")

        result.append(f"\n{'=' * 40}")
        return "\n".join(result)

    def _compute_hash(self, text: str, algorithm: str) -> str:
        if algorithm == "md5":
            return self._md5(text)
        elif algorithm == "sha1":
            return self._sha1(text)
        elif algorithm == "sha256":
            return self._sha256(text)
        return ""

    def _analyze_hash(self, hash_value: str, original_text: str, algorithm: str) -> str:
        result = "Свойства хэша:\n"
        result += f"   • Длина: {len(hash_value)} символов\n"
        result += f"   • Энтропия: {self._calculate_entropy(hash_value):.2f} бит/символ\n"

        # Проверка лавинного эффекта
        if len(original_text) > 0:
            # Изменяем один символ
            modified_text = original_text[:-1] + ('X' if original_text[-1] != 'X' else 'Y')
            modified_hash = self._compute_hash(modified_text, algorithm)

            # Считаем различия
            diff_count = sum(1 for a, b in zip(hash_value, modified_hash) if a != b)
            diff_percent = (diff_count / len(hash_value)) * 100

            result += f"   • Лавинный эффект: {diff_percent:.1f}% изменений при изменении 1 символа\n"

        return result

    def _calculate_entropy(self, text: str) -> float:
        if not text:
            return 0.0

        freq = {}
        for char in text:
            freq[char] = freq.get(char, 0) + 1

        entropy = 0.0
        length = len(text)
        for count in freq.values():
            p = count / length
            if p > 0:
                entropy -= p * math.log2(p)

        return entropy

    # ==================== MD5 ====================

    def _md5(self, text: str) -> str:
        """Реализация MD5"""
        T = [int(abs(math.sin(i + 1)) * 2 ** 32) & 0xFFFFFFFF for i in range(64)]
        A, B, C, D = 0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476

        msg = bytearray(text.encode('utf-8'))
        msg_len = len(msg) * 8
        msg.append(0x80)
        while len(msg) % 64 != 56:
            msg.append(0)
        msg += struct.pack('<Q', msg_len)

        for offset in range(0, len(msg), 64):
            block = msg[offset:offset + 64]
            X = list(struct.unpack('<16I', block))
            AA, BB, CC, DD = A, B, C, D

            for i in range(16):
                k = i
                s = [7, 12, 17, 22][i % 4]
                AC = T[i]
                F = (BB & CC) | (~BB & DD)
                temp = (AA + F + X[k] + AC) & 0xFFFFFFFF
                temp = ((temp << s) | (temp >> (32 - s))) & 0xFFFFFFFF
                AA, BB, CC, DD = DD, (BB + temp) & 0xFFFFFFFF, BB, CC

            for i in range(16):
                k = (1 + 5 * i) % 16
                s = [5, 9, 14, 20][i % 4]
                AC = T[16 + i]
                G = (DD & BB) | (~DD & CC)
                temp = (AA + G + X[k] + AC) & 0xFFFFFFFF
                temp = ((temp << s) | (temp >> (32 - s))) & 0xFFFFFFFF
                AA, BB, CC, DD = DD, (BB + temp) & 0xFFFFFFFF, BB, CC

            for i in range(16):
                k = (5 + 3 * i) % 16
                s = [4, 11, 16, 23][i % 4]
                AC = T[32 + i]
                H = BB ^ CC ^ DD
                temp = (AA + H + X[k] + AC) & 0xFFFFFFFF
                temp = ((temp << s) | (temp >> (32 - s))) & 0xFFFFFFFF
                AA, BB, CC, DD = DD, (BB + temp) & 0xFFFFFFFF, BB, CC

            for i in range(16):
                k = (7 * i) % 16
                s = [6, 10, 15, 21][i % 4]
                AC = T[48 + i]
                I = CC ^ (BB | ~DD)
                temp = (AA + I + X[k] + AC) & 0xFFFFFFFF
                temp = ((temp << s) | (temp >> (32 - s))) & 0xFFFFFFFF
                AA, BB, CC, DD = DD, (BB + temp) & 0xFFFFFFFF, BB, CC

            A = (A + AA) & 0xFFFFFFFF
            B = (B + BB) & 0xFFFFFFFF
            C = (C + CC) & 0xFFFFFFFF
            D = (D + DD) & 0xFFFFFFFF

        return ''.join(f'{x:08x}' for x in [A, B, C, D])

    # ==================== SHA-1 ====================

    def _sha1(self, text: str) -> str:
        """Реализация SHA-1"""
        h0, h1, h2, h3, h4 = 0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0

        msg = bytearray(text.encode('utf-8'))
        msg_len = len(msg) * 8
        msg.append(0x80)
        while len(msg) % 64 != 56:
            msg.append(0)
        msg += struct.pack('>Q', msg_len)

        for offset in range(0, len(msg), 64):
            block = msg[offset:offset + 64]
            w = list(struct.unpack('>16I', block))

            for i in range(16, 80):
                temp = w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16]
                w.append(((temp << 1) | (temp >> 31)) & 0xFFFFFFFF)

            a, b, c, d, e = h0, h1, h2, h3, h4

            for i in range(80):
                if i < 20:
                    f = (b & c) | (~b & d)
                    k = 0x5A827999
                elif i < 40:
                    f = b ^ c ^ d
                    k = 0x6ED9EBA1
                elif i < 60:
                    f = (b & c) | (b & d) | (c & d)
                    k = 0x8F1BBCDC
                else:
                    f = b ^ c ^ d
                    k = 0xCA62C1D6

                temp = (((a << 5) | (a >> 27)) + f + e + k + w[i]) & 0xFFFFFFFF
                e, d, c, b, a = d, c, ((b << 30) | (b >> 2)) & 0xFFFFFFFF, a, temp

            h0 = (h0 + a) & 0xFFFFFFFF
            h1 = (h1 + b) & 0xFFFFFFFF
            h2 = (h2 + c) & 0xFFFFFFFF
            h3 = (h3 + d) & 0xFFFFFFFF
            h4 = (h4 + e) & 0xFFFFFFFF

        return ''.join(f'{x:08x}' for x in [h0, h1, h2, h3, h4])

    # ==================== SHA-256 ====================

    def _sha256(self, text: str) -> str:
        """Реализация SHA-256"""
        K = [
            0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
            0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
            0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
            0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
            0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
            0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
            0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
            0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
        ]

        h = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]

        msg = bytearray(text.encode('utf-8'))
        msg_len = len(msg) * 8
        msg.append(0x80)
        while len(msg) % 64 != 56:
            msg.append(0)
        msg += struct.pack('>Q', msg_len)

        for offset in range(0, len(msg), 64):
            block = msg[offset:offset + 64]
            w = list(struct.unpack('>16I', block))

            for i in range(16, 64):
                s0 = self._rotr(w[i - 15], 7) ^ self._rotr(w[i - 15], 18) ^ (w[i - 15] >> 3)
                s1 = self._rotr(w[i - 2], 17) ^ self._rotr(w[i - 2], 19) ^ (w[i - 2] >> 10)
                w.append((w[i - 16] + s0 + w[i - 7] + s1) & 0xFFFFFFFF)

            a, b, c, d, e, f, g, h_temp = h

            for i in range(64):
                S1 = self._rotr(e, 6) ^ self._rotr(e, 11) ^ self._rotr(e, 25)
                ch = (e & f) ^ (~e & g)
                temp1 = (h_temp + S1 + ch + K[i] + w[i]) & 0xFFFFFFFF
                S0 = self._rotr(a, 2) ^ self._rotr(a, 13) ^ self._rotr(a, 22)
                maj = (a & b) ^ (a & c) ^ (b & c)
                temp2 = (S0 + maj) & 0xFFFFFFFF

                h_temp, g, f, e, d, c, b, a = g, f, e, (d + temp1) & 0xFFFFFFFF, c, b, a, (temp1 + temp2) & 0xFFFFFFFF

            h = [(x + y) & 0xFFFFFFFF for x, y in zip(h, [a, b, c, d, e, f, g, h_temp])]

        return ''.join(f'{x:08x}' for x in h)

    def _rotr(self, n: int, b: int) -> int:
        return ((n >> b) | (n << (32 - b))) & 0xFFFFFFFF

    def generate_key(self) -> str:
        return "md5|sha1|sha256"
