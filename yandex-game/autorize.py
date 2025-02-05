import subprocess
import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox

class AuthWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initDB()

    def initUI(self):
        self.setWindowTitle('Окно авторизации')
        self.setGeometry(100, 100, 300, 150)

        self.login_label = QLabel('Логин:', self)
        self.login_input = QLineEdit(self)

        self.password_label = QLabel('Пароль:', self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)

        self.auth_button = QPushButton('Войти', self)
        self.auth_button.clicked.connect(self.on_auth)

        layout = QVBoxLayout()
        layout.addWidget(self.login_label)
        layout.addWidget(self.login_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.auth_button)

        self.setLayout(layout)

    def initDB(self):
        self.conn = sqlite3.connect('users.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users
                               (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                login TEXT UNIQUE,
                                password TEXT)''')
        self.conn.commit()

        # Добавляем тестового пользователя, если его нет
        self.cursor.execute("INSERT OR IGNORE INTO users (login, password) VALUES (?, ?)", ('admin', 'admin'))
        self.conn.commit()

    def on_auth(self):
        login = self.login_input.text()
        password = self.password_input.text()

        self.cursor.execute("SELECT * FROM users WHERE login = ? AND password = ?", (login, password))
        user = self.cursor.fetchone()

        if user:
            QMessageBox.information(self, 'Успех', 'Авторизация прошла успешно!')
            self.close()  # Закрываем окно авторизации
            self.run_main()  # Запускаем main.py
        else:
            QMessageBox.warning(self, 'Ошибка', 'Неверный логин или пароль')

    def run_main(self):
        """Запуск файла main.py"""
        try:
            # Запускаем внешний процесс
            subprocess.run([sys.executable, "main.py"], check=True)
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось запустить main.py: {e}')
        except FileNotFoundError:
            QMessageBox.critical(self, 'Ошибка', 'Файл main.py не найден.')

    def closeEvent(self, event):
        self.conn.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    auth_window = AuthWindow()
    auth_window.show()
    sys.exit(app.exec_())