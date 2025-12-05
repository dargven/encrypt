
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTextEdit, QLineEdit, QStackedWidget,
    QFrame, QMessageBox, QScrollArea
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor

from ciphers import CaesarCipher, FourSquareCipher, DESCipher, RC4Cipher


class CryptoApp(QMainWindow):
    """Главный класс приложения"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Криптографическое приложение")
        self.setMinimumSize(800, 650)
        
        # Мягкая цветовая схема
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #f5f5f5;
                color: #4a4a4a;
                font-family: 'Helvetica', 'Arial', sans-serif;
            }
            QTextEdit, QLineEdit {
                background-color: white;
                border: 1px solid #d0d0d0;
                border-radius: 4px;
                padding: 8px;
                font-family: 'Helvetica', 'Arial', sans-serif;
                font-size: 11pt;
                color: #4a4a4a;
            }
            QTextEdit:focus, QLineEdit:focus {
                border: 1px solid #a0c0e0;
            }
            QPushButton {
                border: none;
                border-radius: 4px;
                padding: 10px 20px;
                font-size: 11pt;
            }
            QPushButton:hover {
                opacity: 0.9;
            }
            QLabel {
                color: #4a4a4a;
            }
        """)
        
        self.current_cipher = None
        
        # Инициализация шифров
        self.ciphers = {
            "caesar": CaesarCipher(),
            "foursquare": FourSquareCipher(),
            "des": DESCipher(),
            "rc4": RC4Cipher()
        }
        
        # Главный виджет со стеком страниц
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Создание страниц
        self.create_main_menu()
        self.cipher_page = None
    
    def create_main_menu(self):
        """Главное меню выбора алгоритма"""
        menu_widget = QWidget()
        layout = QVBoxLayout(menu_widget)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)
        
        # Заголовок
        title = QLabel("Выберите алгоритм шифрования")
        title.setFont(QFont('Segoe UI', 18))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        layout.addSpacing(30)
        
        # Кнопки выбора алгоритма
        algorithms = [
            ("Шифр Цезаря", "caesar", "#a8d5ba"),
            ("Шифр Квадроинженера", "foursquare", "#a8c5e2"),
            ("Алгоритм DES", "des", "#e2d5a8"),
            ("Потоковый шифр RC4", "rc4", "#d5a8e2"),
            ("Алгоритм RSA", None, "#e8e8e8"),
            ("Хэш-функции", None, "#e8e8e8"),
        ]
        
        for name, cipher_key, color in algorithms:
            btn = QPushButton(name)
            btn.setFixedSize(300, 50)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: #3a3a3a;
                    font-size: 12pt;
                }}
                QPushButton:hover {{
                    background-color: {self._darken_color(color)};
                }}
            """)
            if cipher_key:
                btn.clicked.connect(lambda checked, k=cipher_key: self.open_cipher(k))
            else:
                btn.clicked.connect(self.not_implemented)
            layout.addWidget(btn, alignment=Qt.AlignCenter)
        
        self.stacked_widget.addWidget(menu_widget)

    
    def _darken_color(self, hex_color: str) -> str:
        """Затемнить цвет на 10%"""
        color = QColor(hex_color)
        return color.darker(110).name()
    
    def not_implemented(self):
        """Заглушка для нереализованных алгоритмов"""
        QMessageBox.information(self, "Информация", "Этот алгоритм будет реализован позже")
    
    def open_cipher(self, cipher_key: str):
        """Открыть интерфейс выбранного шифра"""
        self.current_cipher = self.ciphers[cipher_key]
        info = self.current_cipher.get_info()
        self.create_cipher_interface(info["name"], info["key_hint"], info["default_key"])
    
    def create_cipher_interface(self, title_text: str, key_hint: str, default_key: str):
        """Создание интерфейса для шифра"""
        # Удаляем старую страницу шифра если есть
        if self.cipher_page:
            self.stacked_widget.removeWidget(self.cipher_page)
            self.cipher_page.deleteLater()
        
        self.cipher_page = QWidget()
        main_layout = QVBoxLayout(self.cipher_page)
        main_layout.setContentsMargins(25, 15, 25, 15)
        main_layout.setSpacing(10)
        
        # Верхняя панель с кнопкой назад
        top_layout = QHBoxLayout()
        back_btn = QPushButton("← Назад")
        back_btn.setFixedSize(100, 35)
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #e8e8e8;
                color: #4a4a4a;
            }
            QPushButton:hover {
                background-color: #d8d8d8;
            }
        """)
        back_btn.clicked.connect(self.go_back)
        top_layout.addWidget(back_btn)
        top_layout.addStretch()
        main_layout.addLayout(top_layout)
        
        # Заголовок
        title = QLabel(title_text)
        title.setFont(QFont('Segoe UI', 16))
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # Поле ввода текста
        text_label = QLabel("Текст:")
        text_label.setFont(QFont('Segoe UI', 10))
        main_layout.addWidget(text_label)
        
        self.text_input = QTextEdit()
        self.text_input.setMaximumHeight(100)
        self.text_input.setPlaceholderText("Введите текст для шифрования/расшифровки...")
        main_layout.addWidget(self.text_input)
        
        # Поле ключа с кнопкой генерации
        key_layout = QHBoxLayout()
        
        key_label_layout = QVBoxLayout()
        key_label = QLabel("Ключ:")
        key_label.setFont(QFont('Segoe UI', 10))
        key_label_layout.addWidget(key_label)
        
        self.key_input = QLineEdit()
        self.key_input.setText(default_key)
        self.key_input.setPlaceholderText("Введите ключ...")
        key_label_layout.addWidget(self.key_input)
        
        if key_hint:
            hint_label = QLabel(key_hint)
            hint_label.setFont(QFont('Segoe UI', 9))
            hint_label.setStyleSheet("color: #888888;")
            key_label_layout.addWidget(hint_label)
        
        key_layout.addLayout(key_label_layout, stretch=1)
        
        generate_btn = QPushButton("Сгенерировать\nключ")
        generate_btn.setFixedSize(100, 60)
        generate_btn.setStyleSheet("""
            QPushButton {
                background-color: #c5d5e5;
                color: #3a3a3a;
                font-size: 9pt;
            }
            QPushButton:hover {
                background-color: #b5c5d5;
            }
        """)
        generate_btn.clicked.connect(self.generate_key)
        key_layout.addWidget(generate_btn)
        
        main_layout.addLayout(key_layout)
        
        # Кнопки действий
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)
        
        encrypt_btn = QPushButton("Зашифровать")
        encrypt_btn.setFixedSize(150, 45)
        encrypt_btn.setStyleSheet("""
            QPushButton {
                background-color: #a8d5ba;
                color: #3a3a3a;
                font-size: 11pt;
            }
            QPushButton:hover {
                background-color: #8fc5a1;
            }
        """)
        encrypt_btn.clicked.connect(self.encrypt)
        btn_layout.addWidget(encrypt_btn)
        
        decrypt_btn = QPushButton("Расшифровать")
        decrypt_btn.setFixedSize(150, 45)
        decrypt_btn.setStyleSheet("""
            QPushButton {
                background-color: #a8c5e2;
                color: #3a3a3a;
                font-size: 11pt;
            }
            QPushButton:hover {
                background-color: #8ab5d2;
            }
        """)
        decrypt_btn.clicked.connect(self.decrypt)
        btn_layout.addWidget(decrypt_btn)
        
        crack_btn = QPushButton("Взломать")
        crack_btn.setFixedSize(150, 45)
        crack_btn.setStyleSheet("""
            QPushButton {
                background-color: #e2b8b8;
                color: #3a3a3a;
                font-size: 11pt;
            }
            QPushButton:hover {
                background-color: #d2a8a8;
            }
        """)
        crack_btn.clicked.connect(self.crack)
        btn_layout.addWidget(crack_btn)
        
        main_layout.addLayout(btn_layout)
        
        # Поле результата
        result_label = QLabel("Результат:")
        result_label.setFont(QFont('Segoe UI', 10))
        main_layout.addWidget(result_label)
        
        self.result_output = QTextEdit()
        self.result_output.setReadOnly(False)
        self.result_output.setPlaceholderText("Здесь появится результат...")
        main_layout.addWidget(self.result_output, stretch=1)
        
        # Кнопка очистки
        clear_btn = QPushButton("Очистить")
        clear_btn.setFixedSize(150, 40)
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #e8e8e8;
                color: #4a4a4a;
            }
            QPushButton:hover {
                background-color: #d8d8d8;
            }
        """)
        clear_btn.clicked.connect(self.clear_fields)
        main_layout.addWidget(clear_btn, alignment=Qt.AlignCenter)
        
        self.stacked_widget.addWidget(self.cipher_page)
        self.stacked_widget.setCurrentWidget(self.cipher_page)
    
    def go_back(self):
        """Вернуться в главное меню"""
        self.stacked_widget.setCurrentIndex(0)
    
    def generate_key(self):
        """Генерация случайного ключа"""
        if self.current_cipher:
            new_key = self.current_cipher.generate_key()
            self.key_input.setText(new_key)
    
    def encrypt(self):
        """Шифрование текста"""
        text = self.text_input.toPlainText().strip()
        key = self.key_input.text().strip()
        
        if not text:
            QMessageBox.warning(self, "Внимание", "Введите текст")
            return
        
        result = self.current_cipher.encrypt(text, key)
        self.result_output.setText(result)
    
    def decrypt(self):
        """Расшифровка текста"""
        text = self.text_input.toPlainText().strip()
        key = self.key_input.text().strip()
        
        if not text:
            QMessageBox.warning(self, "Внимание", "Введите текст")
            return
        
        result = self.current_cipher.decrypt(text, key)
        self.result_output.setText(result)
    
    def crack(self):
        """Взлом шифра"""
        text = self.text_input.toPlainText().strip()
        
        if not text:
            QMessageBox.warning(self, "Внимание", "Введите зашифрованный текст")
            return
        
        result = self.current_cipher.crack(text)
        self.result_output.setText(result)
    
    def clear_fields(self):
        """Очистка полей"""
        self.text_input.clear()
        self.key_input.clear()
        self.result_output.clear()
        
        if self.current_cipher:
            self.key_input.setText(self.current_cipher.default_key)
