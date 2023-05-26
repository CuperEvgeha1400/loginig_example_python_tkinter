import tkinter as tk
import sqlite3
from subscriptions_window import SubscriptionsWindow
from register_window import RegisterWindow


class LoginWindow:
    def __init__(self, master):
        self.master = master

        # Создание меток и полей ввода
        self.label_username = tk.Label(master, text='Имя пользователя:')
        self.label_username.pack()
        self.entry_username = tk.Entry(master)
        self.entry_username.pack()

        self.label_password = tk.Label(master, text='Пароль:')
        self.label_password.pack()
        self.entry_password = tk.Entry(master, show='*')
        self.entry_password.pack()

        # Создание кнопки входа
        self.button_login = tk.Button(master, text='Войти', command=self.login)
        self.button_login.pack()

        # Создание кнопки регистрации
        self.button_register = tk.Button(master, text='Регистрация', command=self.open_register_window)
        self.button_register.pack()

        # Метка для отображения результата
        self.label_result = tk.Label(master, text='')
        self.label_result.pack()

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        subscriptions_window = SubscriptionsWindow(username)
        subscriptions_window.refresh_subscriptions()
        subscriptions_window.show()

        # Подключение к базе данных
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Выполнение запроса для проверки учетных данных
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        result = cursor.fetchone()

        # Закрытие соединения с базой данных
        cursor.close()
        conn.close()

        # Проверка результата запроса
        if result:
            self.label_result.config(text='Вход выполнен', fg='green')
            # Закрытие текущего окна
            self.master.destroy()
            # Открытие второго окна со списком подписок
            subscriptions_window = SubscriptionsWindow(username)
            subscriptions_window.show()
        else:
            self.label_result.config(text='Неправильное имя пользователя или пароль', fg='red')

    def open_register_window(self):
        register_window = RegisterWindow(self.master)
        register_window.show()
