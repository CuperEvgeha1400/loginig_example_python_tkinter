import tkinter as tk
import sqlite3


class RegisterWindow:
    def __init__(self, master):
        self.master = master

        self.register_window = tk.Toplevel(master)
        self.register_window.title('Регистрация')

        self.label_username = tk.Label(self.register_window, text='Имя пользователя:')
        self.label_username.pack()
        self.entry_username = tk.Entry(self.register_window)
        self.entry_username.pack()

        self.label_password = tk.Label(self.register_window, text='Пароль:')
        self.label_password.pack()
        self.entry_password = tk.Entry(self.register_window, show='*')
        self.entry_password.pack()

        self.button_save = tk.Button(self.register_window, text='Сохранить', command=self.save_user)
        self.button_save.pack()

        self.label_result_register = tk.Label(self.register_window, text='')
        self.label_result_register.pack()

    def save_user(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        # Подключение к базе данных
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Выполнение запроса для проверки существования пользователя с таким именем
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        result = cursor.fetchone()

        if result:
            self.label_result_register.config(text='Пользователь уже существует', fg='red')
        else:
            # Вставка нового пользователя в базу данных
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            self.label_result_register.config(text='Регистрация успешна', fg='green')

        # Закрытие соединения с базой данных
        cursor.close()
        conn.close()

    def show(self):
        # Запуск главного цикла событий для окна регистрации
        self.register_window.mainloop()
