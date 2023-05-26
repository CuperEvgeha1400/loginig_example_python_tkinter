import sqlite3

# Подключение к базе данных или создание новой, если она не существует
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Создание таблицы users для хранения информации о пользователях
cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, '
               'username TEXT UNIQUE NOT NULL, password TEXT NOT NULL, is_superuser INTEGER DEFAULT 0)')

# Создание таблицы subscriptions для хранения информации о подписках
cursor.execute('CREATE TABLE IF NOT EXISTS subscriptions (id INTEGER PRIMARY KEY AUTOINCREMENT, '
               'user_id INTEGER NOT NULL, subscription_type TEXT NOT NULL, '
               'FOREIGN KEY(user_id) REFERENCES users(id))')

# Проверка наличия суперпользователя с логином 'admin'
cursor.execute('SELECT * FROM users WHERE username = ?', ('admin',))
result = cursor.fetchone()
if not result:
    # Создание суперпользователя
    cursor.execute('INSERT INTO users (username, password, is_superuser) VALUES (?, ?, ?)',
                   ('admin', 'admin', 1))
    conn.commit()

# Закрытие соединения с базой данных
cursor.close()
conn.close()
