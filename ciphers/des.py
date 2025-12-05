"""
Алгоритм DES (Data Encryption Standard)
"""
from .base import BaseCipher
from .keygen import key_generator


class DESCipher(BaseCipher):
    IP = [58, 50, 42, 34, 26, 18, 10, 2,
          60, 52, 44, 36, 28, 20, 12, 4,
          62, 54, 46, 38, 30, 22, 14, 6,
          64, 56, 48, 40, 32, 24, 16, 8,
          57, 49, 41, 33, 25, 17, 9, 1,
          59, 51, 43, 35, 27, 19, 11, 3,
          61, 53, 45, 37, 29, 21, 13, 5,
          63, 55, 47, 39, 31, 23, 15, 7]

    IP_INV = [40, 8, 48, 16, 56, 24, 64, 32,
              39, 7, 47, 15, 55, 23, 63, 31,
              38, 6, 46, 14, 54, 22, 62, 30,
              37, 5, 45, 13, 53, 21, 61, 29,
              36, 4, 44, 12, 52, 20, 60, 28,
              35, 3, 43, 11, 51, 19, 59, 27,
              34, 2, 42, 10, 50, 18, 58, 26,
              33, 1, 41, 9, 49, 17, 57, 25]

    # Таблица расширения E (32 -> 48 бит)
    E = [32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9,
         8, 9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17,
         16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25,
         24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1]

    # Перестановка P
    P = [16, 7, 20, 21, 29, 12, 28, 17,
         1, 15, 23, 26, 5, 18, 31, 10,
         2, 8, 24, 14, 32, 27, 3, 9,
         19, 13, 30, 6, 22, 11, 4, 25]

    # S-блоки
    S_BOXES = [
        [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
         [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
         [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
         [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
        [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
         [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
         [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
         [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
        [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
         [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
         [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
         [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
        [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
         [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
         [10, 6, 9, 0, 12, 11, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
         [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
        [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
         [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
         [4, 2, 1, 11, 10, 13, 7, 8, 15, 1, 3, 14, 12, 3, 0, 14],
         [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
        [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
         [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
         [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
         [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
        [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
         [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
         [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
         [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
        [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
         [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
         [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
         [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]
    ]

    # Перестановка PC1
    PC1 = [57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18,
           10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36,
           63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22,
           14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4]

    # Перестановка PC2
    PC2 = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10,
           23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2,
           41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48,
           44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]

    # Сдвиги для каждого раунда
    SHIFTS = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

    def __init__(self):
        super().__init__()
        self.name = "Алгоритм DES"
        self.key_hint = "Подсказка: ключ 8 символов (например, mykey123)"
        self.default_key = "mykey123"
        self.cipher_type = "des"

    def _str_to_bits(self, s: str) -> list:
        bits = []
        for char in s:
            byte = ord(char)
            for i in range(7, -1, -1):
                bits.append((byte >> i) & 1)
        return bits

    def _bits_to_str(self, bits: list) -> str:
        chars = []
        for i in range(0, len(bits), 8):
            byte = 0
            for j in range(8):
                if i + j < len(bits):
                    byte = (byte << 1) | bits[i + j]
            chars.append(chr(byte))
        return ''.join(chars)

    def _bits_to_hex(self, bits: list) -> str:
        hex_str = ""
        for i in range(0, len(bits), 4):
            val = 0
            for j in range(4):
                if i + j < len(bits):
                    val = (val << 1) | bits[i + j]
            hex_str += format(val, 'x')
        return hex_str.upper()

    def _hex_to_bits(self, hex_str: str) -> list:
        bits = []
        for char in hex_str:
            val = int(char, 16)
            for i in range(3, -1, -1):
                bits.append((val >> i) & 1)
        return bits

    def _permute(self, block: list, table: list) -> list:
        return [block[i - 1] for i in table]

    def _left_shift(self, bits: list, n: int) -> list:
        return bits[n:] + bits[:n]

    def _xor(self, a: list, b: list) -> list:
        return [x ^ y for x, y in zip(a, b)]

    def _generate_keys(self, key_bits: list) -> list:
        key56 = self._permute(key_bits, self.PC1)
        c, d = key56[:28], key56[28:]

        keys = []
        for i in range(16):
            c = self._left_shift(c, self.SHIFTS[i])
            d = self._left_shift(d, self.SHIFTS[i])
            cd = c + d
            key48 = self._permute(cd, self.PC2)
            keys.append(key48)

        return keys

    def _s_box_substitution(self, bits48: list) -> list:
        result = []
        for i in range(8):
            block = bits48[i * 6:(i + 1) * 6]
            row = (block[0] << 1) | block[5]
            col = (block[1] << 3) | (block[2] << 2) | (block[3] << 1) | block[4]
            val = self.S_BOXES[i][row][col]
            for j in range(3, -1, -1):
                result.append((val >> j) & 1)
        return result

    def _f_function(self, right: list, key: list) -> list:
        expanded = self._permute(right, self.E)
        xored = self._xor(expanded, key)
        substituted = self._s_box_substitution(xored)
        return self._permute(substituted, self.P)

    def _encrypt_block(self, block: list, keys: list) -> list:
        permuted = self._permute(block, self.IP)
        left, right = permuted[:32], permuted[32:]

        for i in range(16):
            new_left = right
            f_result = self._f_function(right, keys[i])
            new_right = self._xor(left, f_result)
            left, right = new_left, new_right

        combined = right + left
        return self._permute(combined, self.IP_INV)

    def _decrypt_block(self, block: list, keys: list) -> list:
        return self._encrypt_block(block, keys[::-1])

    def _pad_text(self, text: str) -> str:
        pad_len = 8 - (len(text) % 8)
        return text + chr(pad_len) * pad_len

    def _unpad_text(self, text: str) -> str:
        if not text:
            return text
        pad_len = ord(text[-1])
        if pad_len > 8:
            return text
        return text[:-pad_len]

    def _prepare_key(self, key: str) -> list:
        if len(key) < 8:
            key = key + '\0' * (8 - len(key))
        elif len(key) > 8:
            key = key[:8]
        return self._str_to_bits(key)

    def encrypt(self, text: str, key: str) -> str:
        if not key:
            return "Ошибка: введите ключ (8 символов)"

        key_bits = self._prepare_key(key)
        keys = self._generate_keys(key_bits)
        padded = self._pad_text(text)

        result_bits = []
        for i in range(0, len(padded), 8):
            block = padded[i:i + 8]
            block_bits = self._str_to_bits(block)
            encrypted_bits = self._encrypt_block(block_bits, keys)
            result_bits.extend(encrypted_bits)

        return self._bits_to_hex(result_bits)

    def decrypt(self, hex_text: str, key: str) -> str:
        if not key:
            return "Ошибка: введите ключ (8 символов)"

        hex_text = hex_text.replace(" ", "").replace("\n", "")

        try:
            self._hex_to_bits(hex_text)
        except:
            return "Ошибка: введите зашифрованный текст в hex формате"

        key_bits = self._prepare_key(key)
        keys = self._generate_keys(key_bits)
        cipher_bits = self._hex_to_bits(hex_text)

        result = ""
        for i in range(0, len(cipher_bits), 64):
            block = cipher_bits[i:i + 64]
            if len(block) < 64:
                block.extend([0] * (64 - len(block)))
            decrypted_bits = self._decrypt_block(block, keys)
            result += self._bits_to_str(decrypted_bits)

        return self._unpad_text(result)

    def crack(self, hex_text: str) -> str:
        result = ["=== Ну че епта, взламываем? DES==="]
        hex_text = hex_text.replace(" ", "").replace("\n", "").strip()

        if not hex_text:
            return "Ошибка: пустой зашифрованный текст"

        if len(hex_text) % 16 != 0:
            result.append(f"Внимание: длина hex-строки ({len(hex_text)}) не кратна 16")

        result.append("\n1. Пробуем брут по словарю:")

        dictionary = [
            "password",
            "12345678",
            "qwertyui",
            "admin123",
            "letmein",
            "secret00",
            "testkey0",
            "abcdefgh",
            "password1",
            "11111111",
            "mykey123"
        ]

        found_key = None
        found_plaintext = None

        for test_key in dictionary:
            try:
                decrypted = self.decrypt(hex_text, test_key)

                if decrypted and self._looks_like_text(decrypted):
                    found_key = test_key
                    found_plaintext = decrypted
                    result.append(f"✓ Найден ключ: '{test_key}'")
                    result.append(f"   Расшифрованный текст: {decrypted[:60]}...")
                    break
                else:
                    result.append(f"✗ Ключ '{test_key}': результат не похож на текст")

            except Exception as e:
                result.append(f"✗ Ключ '{test_key}': ошибка при расшифровке")

        result.append("\n2. ЧАСТИЧНЫЙ БРУТФОРС:")

        if not found_key:
            result.append("Поиск простых комбинаций ASCII символов...")

            # Генерируем простые комбинации для демонстрации
            simple_patterns = [
                ''.join(chr(ord('A') + i) for i in range(8)),  # ABCDEFGH
                ''.join(chr(ord('a') + i) for i in range(8)),  # abcdefgh
                '00000000',
                '11111111',
                'aaaaaaaa',
                'AAAAAAAA',
            ]

            for pattern in simple_patterns:
                try:
                    decrypted = self.decrypt(hex_text, pattern)
                    if decrypted and self._looks_like_text(decrypted):
                        result.append(f"✓ Найден паттерн: '{pattern}'")
                        break
                except:
                    pass
        # Вычисляем предполагаемую длину ключа
        result.append(f"• Длина зашифрованных данных: {len(hex_text) // 2} байт")

        # Проверяем наличие известных заголовков/паттернов
        common_patterns = {
            "текст": ["54", "65", "78", "74"],  # "Text" в ASCII
            "PNG": ["89", "50", "4E", "47"],  # PNG заголовок
            "PDF": ["25", "50", "44", "46"],  # PDF заголовок
            "ZIP": ["50", "4B", "03", "04"],  # ZIP заголовок
        }

        for pattern_name, pattern_bytes in common_patterns.items():
            # Простая проверка первых байт (для учебных целей)
            if hex_text[:8].upper() in ''.join(pattern_bytes).upper():
                result.append(f"• Возможный формат: {pattern_name}")

        # 4. Вывод результатов
        result.append("\n4. РЕЗУЛЬТАТЫ:")

        if found_key:
            result.append(f"• УСПЕШНЫЙ ВЗЛОМ!")
            result.append(f"• Ключ: {found_key}")
            result.append(f"• Первые 100 символов текста: {found_plaintext[:100]}...")
        else:
            result.append("• Ключ не найден в словаре")

        return "\n".join(result)

    def _looks_like_text(self, text: str, threshold: float = 0.7) -> bool:

        if not text:
            return False

        printable_count = sum(1 for c in text[:100] if 32 <= ord(c) <= 126)

        space_count = text[:100].count(' ')

        return (printable_count / min(100, len(text))) > threshold or space_count > 5

    def generate_key(self) -> str:
        return key_generator.generate_for_cipher(self.cipher_type)
