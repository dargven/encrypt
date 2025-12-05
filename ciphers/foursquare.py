"""
Шифр Квадроинженера
"""
import random

from .base import BaseCipher
from .keygen import key_generator


class FourSquareCipher(BaseCipher):
    ALPHABET = "ABCDEFGHIKLMNOPQRSTUVWXYZ"

    # Частотный анализ английского языка
    ENGLISH_FREQ = {
        'E': 12.7, 'T': 9.1, 'A': 8.2, 'O': 7.5, 'I': 7.0,
        'N': 6.7, 'S': 6.3, 'H': 6.1, 'R': 6.0, 'D': 4.3,
        'L': 4.0, 'C': 2.8, 'U': 2.8, 'M': 2.4, 'W': 2.4,
        'F': 2.2, 'G': 2.0, 'Y': 2.0, 'P': 1.9, 'B': 1.5,
        'V': 1.0, 'K': 0.8, 'J': 0.2, 'X': 0.2, 'Q': 0.1, 'Z': 0.1
    }

    def __init__(self):
        super().__init__()
        self.name = "Шифр Квадроинженера (Four-Square)"
        self.key_hint = "Подсказка: два ключа через пробел (например, SECRET PASSWORD)"
        self.default_key = "EXAMPLE KEYWORD"
        self.cipher_type = "foursquare"

    def _create_square(self, key: str = "") -> list:
        """Создание квадрата 5x5 на основе ключа"""
        key = key.upper().replace("J", "I")

        used = set()
        square = []

        for char in key:
            if char in self.ALPHABET and char not in used:
                square.append(char)
                used.add(char)

        for char in self.ALPHABET:
            if char not in used:
                square.append(char)
                used.add(char)

        return square

    def _find_position(self, square: list, char: str) -> tuple:
        if char in square:
            idx = square.index(char)
            return idx // 5, idx % 5
        return None, None

    def _get_char_at(self, square: list, row: int, col: int) -> str:
        return square[row * 5 + col]

    def _parse_keys(self, key: str) -> tuple:
        keys = key.replace(",", " ").split()
        key1 = keys[0] if len(keys) > 0 else "EXAMPLE"
        key2 = keys[1] if len(keys) > 1 else "KEYWORD"
        return key1, key2

    def encrypt(self, text: str, key: str) -> str:
        key1, key2 = self._parse_keys(key)

        plain_square = self._create_square("")
        square_ur = self._create_square(key1)
        square_ll = self._create_square(key2)

        text = text.upper().replace("J", "I")
        clean_text = "".join(c for c in text if c in self.ALPHABET)

        if len(clean_text) % 2 == 1:
            clean_text += "X"

        result = ""

        for i in range(0, len(clean_text), 2):
            char1, char2 = clean_text[i], clean_text[i + 1]

            row1, col1 = self._find_position(plain_square, char1)
            row2, col2 = self._find_position(plain_square, char2)

            if row1 is not None and row2 is not None:
                enc1 = self._get_char_at(square_ur, row1, col2)
                enc2 = self._get_char_at(square_ll, row2, col1)
                result += enc1 + enc2
            else:
                result += char1 + char2

        return " ".join(result[i:i + 5] for i in range(0, len(result), 5))

    def decrypt(self, text: str, key: str) -> str:
        key1, key2 = self._parse_keys(key)

        plain_square = self._create_square("")
        square_ur = self._create_square(key1)
        square_ll = self._create_square(key2)

        text = text.upper().replace("J", "I").replace(" ", "")
        clean_text = "".join(c for c in text if c in self.ALPHABET)

        result = ""

        for i in range(0, len(clean_text), 2):
            if i + 1 >= len(clean_text):
                break

            char1, char2 = clean_text[i], clean_text[i + 1]

            row1, col1 = self._find_position(square_ur, char1)
            row2, col2 = self._find_position(square_ll, char2)

            if row1 is not None and row2 is not None:
                dec1 = self._get_char_at(plain_square, row1, col2)
                dec2 = self._get_char_at(plain_square, row2, col1)
                result += dec1 + dec2
            else:
                result += char1 + char2

        return result

    def _score_text(self, text: str) -> float:
        text = text.upper()
        total_chars = len(text)
        if total_chars == 0:
            return 0.0

        # Подсчет частот букв
        freq = {}
        for char in text:
            if char in self.ALPHABET:
                freq[char] = freq.get(char, 0) + 1

        score = 0.0
        for char in self.ALPHABET:
            expected_freq = self.ENGLISH_FREQ.get(char, 0.0) / 100.0
            actual_freq = freq.get(char, 0) / total_chars

            score += (expected_freq - actual_freq) ** 2

        common_bigrams = ['TH', 'HE', 'IN', 'ER', 'AN', 'RE', 'ND', 'AT', 'ON', 'NT']
        bigram_bonus = 0
        for i in range(len(text) - 1):
            bigram = text[i:i + 2]
            if bigram in common_bigrams:
                bigram_bonus += 1

        # Чем меньше score, тем лучше текст (ближе к английскому)
        return -score + (bigram_bonus / max(1, len(text))) * 0.1

    def _generate_key_combinations(self) -> list:
        common_words = [
            # Одиночные буквы и короткие слова
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M',
            'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
            'KEY', 'SEC', 'PWD', 'COD', 'PAS', 'ABC', 'XYZ', 'ONE', 'TWO',
            'YES', 'NO', 'GO', 'HI', 'OK', 'TOP', 'BOT', 'NEW', 'OLD',
            'CRYPT', 'ENCRYPT', 'DECRYPT', 'CIPHER', 'CODE', 'SECRET',
            'PASSWORD', 'KEYWORD', 'EXAMPLE', 'TEST', 'SAMPLE', 'DEMO',
            'ALPHA', 'BETA', 'GAMMA', 'DELTA', 'OMEGA', 'SIGMA',
            'BLUE', 'RED', 'GREEN', 'BLACK', 'WHITE', 'GOLD',
            'SUN', 'MOON', 'STAR', 'SKY', 'SEA', 'LAND',
        ]

        # Отбираем 16 самых вероятных слов
        selected_words = common_words[:16]

        # Генерируем пары (key1, key2)
        combinations = []

        # 1. Популярные комбинации
        popular_pairs = [
            ("SECRET", "PASSWORD"),
            ("EXAMPLE", "KEYWORD"),
            ("CIPHER", "CRYPTO"),
            ("ALPHA", "BETA"),
            ("KEY", "CODE"),
            ("ENCRYPT", "DECRYPT"),
            ("BLACK", "WHITE"),
            ("SUN", "MOON"),
            ("TOP", "SECRET"),
            ("NEW", "PASSWORD"),
        ]

        combinations.extend(popular_pairs)

        for word in ['KEY', 'CODE', 'PASS', 'SECRET', 'TEST']:
            combinations.append((word, word))

        random.seed(42)

        while len(combinations) < 32:
            key1 = random.choice(selected_words)
            key2 = random.choice(selected_words)
            if (key1, key2) not in combinations:
                combinations.append((key1, key2))

        return combinations[:32]  # Ограничиваем 32 комбинациями

    def crack(self, text: str) -> str:
        result = []
        result.append("=== ШИФР КВАДРОИНЖЕНЕРА (FOUR-SQUARE) - ВЗЛОМ ===\n")

        key_combinations = self._generate_key_combinations()

        attempts = []

        for key1, key2 in key_combinations:
            key_str = f"{key1} {key2}"
            try:
                decrypted = self.decrypt(text, key_str)
                if decrypted:  # Проверяем, что результат не пустой
                    score = self._score_text(decrypted)
                    attempts.append((score, key1, key2, decrypted))
            except Exception as e:
                continue

        attempts.sort(key=lambda x: x[0], reverse=True)

        result.append(f"Протестировано комбинаций: {len(attempts)}\n")

        for i, (score, key1, key2, decrypted) in enumerate(attempts[:10], 1):
            display_text = decrypted[:50] + "..." if len(decrypted) > 50 else decrypted
            result.append(f"\n{i}. Ключи: [{key1}, {key2}]")
            result.append(f"   Оценка: {score:.4f}")
            result.append(f"   Текст: {display_text}")

            words = decrypted.split()
            if words:
                sample_words = " ".join(words[:5])
                result.append(f"   Слова: {sample_words}...")

        clean_text = text.upper().replace("J", "I").replace(" ", "")

        # Анализ биграмм
        if len(clean_text) >= 4:
            result.append(f"Первые 4 символа: {clean_text[:4]}")
            result.append(f"Длина текста: {len(clean_text)} символов")

            bigrams = {}
            for i in range(0, len(clean_text) - 1, 2):
                bigram = clean_text[i:i + 2]
                bigrams[bigram] = bigrams.get(bigram, 0) + 1

            common_bigrams = sorted(bigrams.items(), key=lambda x: x[1], reverse=True)[:3]
            result.append("Наиболее частые биграммы:")
            for bigram, count in common_bigrams:
                result.append(f"  {bigram}: {count} раз")

        # Показываем 5 худших результатов для сравнения
        if len(attempts) > 10:
            result.append("\n=== ХУДШИЕ РЕЗУЛЬТАТЫ по частотному анализу ===")
            for i, (score, key1, key2, decrypted) in enumerate(attempts[-5:], 1):
                display_text = decrypted[:30] + "..." if len(decrypted) > 30 else decrypted
                result.append(f"{i}. [{key1}, {key2}]: {display_text}")

        return "\n".join(result)

    def generate_key(self) -> str:
        return key_generator.generate_for_cipher(self.cipher_type)


# Дополнительный класс для улучшенного взлома
class FourSquareCipherAdvanced(FourSquareCipher):

    def crack(self, text: str) -> str:
        result = []

        # Сначала получаем базовые результаты
        basic_result = super().crack(text)

        result.append("=== АНАЛИЗ ПАТТЕРНОВ ===")

        clean_text = text.upper().replace("J", "I").replace(" ", "")

        if len(clean_text) >= 20:
            patterns = {}
            pattern_length = 4  # Длина паттерна для поиска

            for i in range(len(clean_text) - pattern_length + 1):
                pattern = clean_text[i:i + pattern_length]
                if pattern in patterns:
                    patterns[pattern].append(i)
                else:
                    patterns[pattern] = [i]

            repeated_patterns = {p: pos for p, pos in patterns.items() if len(pos) > 1}

            if repeated_patterns:
                result.append(f"Найдено {len(repeated_patterns)} повторяющихся паттернов:")
                for pattern, positions in list(repeated_patterns.items())[:5]:
                    result.append(f"  '{pattern}' на позициях: {positions}")
            else:
                result.append("Повторяющиеся паттерны не найдены")

        result.append("\n" + basic_result)

        return "\n".join(result)
