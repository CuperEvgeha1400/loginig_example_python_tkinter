import tkinter as tk
import sqlite3


class SubscriptionsWindow:
    def __init__(self, username):
        self.username = username

        # Подключение к базе данных
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Получение user_id по имени пользователя
        cursor.execute('SELECT id FROM users WHERE username = ?', (self.username,))
        result = cursor.fetchone()
        if result:
            self.user_id = result[0]

        # Создание окна
        self.window = tk.Tk()
        self.window.title('Список подписок')

        # Создание виджета списка для отображения подписок
        self.listbox_subscriptions = tk.Listbox(self.window)
        self.listbox_subscriptions.pack()

        # Создание метки и поля ввода для новой подписки
        self.label_subscription_type = tk.Label(self.window, text='Тип подписки:')
        self.label_subscription_type.pack()
        self.entry_subscription_type = tk.Entry(self.window)
        self.entry_subscription_type.pack()

        self.button_unsubscribe = tk.Button(self.window, text='Отписаться', command=self.unsubscribe)
        self.button_unsubscribe.pack()

        # Создание кнопки "Создать подписку"
        self.button_create_subscription = tk.Button(self.window, text='Создать подписку',
                                                    command=self.create_subscription)
        self.button_create_subscription.pack()

        # Создание кнопки "Удалить подписку" для суперпользователя
        if self.username == 'admin':
            self.button_delete_subscription = tk.Button(self.window, text='Удалить подписку',
                                                        command=self.delete_subscription)
            self.button_delete_subscription.pack()

        # Создание кнопки "Добавить подписку"
        self.button_add_existing_subscription = tk.Button(self.window, text='Добавить подписку',
                                                          command=self.add_existing_subscription)
        self.button_add_existing_subscription.pack()

        # Закрытие соединения с базой данных
        cursor.close()
        conn.close()

        # Обновление списка подписок
        self.update_subscriptions()

    def show(self):
        # Запуск главного цикла событий для окна списка подписок
        self.window.mainloop()

    def unsubscribe(self):
        selected_subscription = self.listbox_subscriptions.curselection()
        if selected_subscription:
            subscription_type = self.listbox_subscriptions.get(selected_subscription)
            # Подключение к базе данных
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()

            # Выполнение запроса для удаления подписки
            cursor.execute('DELETE FROM subscriptions WHERE user_id = ? AND subscription_type = ?',
                           (self.user_id, subscription_type))
            conn.commit()

            # Закрытие соединения с базой данных
            cursor.close()
            conn.close()

            # Обновление списка подписок
            self.update_subscriptions()


    def create_subscription(self):
        subscription_type = self.entry_subscription_type.get()

        # Проверка, чтобы обычный пользователь мог добавлять только существующие подписки
        if self.username != 'admin':
            # Подключение к базе данных
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()

            # Выполнение запроса для проверки существования подписки
            cursor.execute('SELECT * FROM subscriptions WHERE subscription_type = ?', (subscription_type,))
            result = cursor.fetchone()

            # Закрытие соединения с базой данных
            cursor.close()
            conn.close()

            if not result:
                self.label_result.config(text='Неверный тип подписки', fg='red')
                return

            # Подключение к базе данных
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()

            # Выполнение запроса для создания новой подписки для текущего пользователя
            cursor.execute('INSERT INTO subscriptions (user_id, subscription_type) VALUES (?, ?)',
                           (self.user_id, subscription_type))
            conn.commit()

            # Закрытие соединения с базой данных
            cursor.close()
            conn.close()

            # Очистка поля ввода
            self.entry_subscription_type.delete(0, tk.END)

            # Обновление списка подписок текущего пользователя
            self.update_subscriptions()

    def delete_subscription(self):
        selected_subscription = self.listbox_subscriptions.curselection()
        if selected_subscription:
            subscription_type = self.listbox_subscriptions.get(selected_subscription)
            # Подключение к базе данных
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()

            # Выполнение запроса для удаления подписки
            cursor.execute('DELETE FROM subscriptions WHERE user_id = ? AND subscription_type = ?',
                           (self.user_id, subscription_type))
            conn.commit()

            # Закрытие соединения с базой данных
            cursor.close()
            conn.close()

            # Обновление списка подписок
            self.update_subscriptions()

    def update_subscriptions(self):
        # Очистка списка подписок
        self.listbox_subscriptions.delete(0, tk.END)

        # Подключение к базе данных
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Выполнение запроса для получения списка подписок текущего пользователя
        cursor.execute('SELECT subscription_type FROM subscriptions WHERE user_id = ?', (self.user_id,))
        subscriptions = cursor.fetchall()

        # Отображение подписок в списке
        for subscription in subscriptions:
            self.listbox_subscriptions.insert(tk.END, subscription[0])  # Отображение только subscription_type

        # Закрытие соединения с базой данных
        cursor.close()
        conn.close()

    def add_existing_subscription(self):
        # Подключение к базе данных
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Выполнение запроса для получения списка всех существующих подписок
        cursor.execute('SELECT subscription_type FROM subscriptions')
        subscriptions = cursor.fetchall()

        # Закрытие соединения с базой данных
        cursor.close()
        conn.close()

        # Создание нового окна для выбора подписки
        window = tk.Toplevel(self.window)
        window.title('Выберите подписку')

        # Создание виджета списка для отображения подписок
        listbox_existing_subscriptions = tk.Listbox(window)
        listbox_existing_subscriptions.pack()

        # Заполнение списка подписок
        for subscription in subscriptions:
            listbox_existing_subscriptions.insert(tk.END, subscription[0])

        # Создание кнопки "Добавить"
        button_add_subscription = tk.Button(window, text='Добавить',
                                            command=lambda: self.add_subscription_from_listbox(
                                                listbox_existing_subscriptions.get(
                                                    listbox_existing_subscriptions.curselection())))
        button_add_subscription.pack()

    def add_subscription_from_listbox(self, subscription_type):
        # Подключение к базе данных
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Выполнение запроса для проверки существования подписки
        cursor.execute('SELECT * FROM subscriptions WHERE subscription_type = ?', (subscription_type,))
        result = cursor.fetchone()

        # Закрытие соединения с базой данных
        cursor.close()
        conn.close()

        if not result:
            self.label_result.config(text='Неверный тип подписки', fg='red')
            return

        # Подключение к базе данных
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Выполнение запроса для создания новой подписки для текущего пользователя
        cursor.execute('INSERT INTO subscriptions (user_id, subscription_type) VALUES (?, ?)',
                       (self.user_id, subscription_type))
        conn.commit()

        # Закрытие соединения с базой данных
        cursor.close()
        conn.close()

        # Обновление списка подписок текущего пользователя
        self.update_subscriptions()
