#!/usr/bin/env python3
"""
Криптографическое приложение
Точка входа
"""
import os
import sys

# Добавляем путь к модулям
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from ui import CryptoApp


def main():
    """Запуск приложения"""
    app = QApplication(sys.argv)
    window = CryptoApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
