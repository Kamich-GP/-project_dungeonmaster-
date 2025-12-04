import sqlite3

# Подключение к БД
connection = sqlite3.connect('delivery.db', check_same_thread=False)
# Python + SQL
sql = connection.cursor()

# Создание таблиц
sql.execute('CREATE TABLE IF NOT EXISTS users '
            '(tg_id INTEGER, name TEXT, num TEXT);')


## Методы пользователя ##
# Регистрация
def register(tg_id, name, num):
    sql.execute('INSERT INTO users VALUES (?, ?, ?);', (tg_id, name, num))
    # Фиксируем изменения
    connection.commit()

# Проверка пользователя на наличие в БД
def check_user(tg_id):
    if sql.execute('SELECT * FROM users WHERE tg_id=?;', (tg_id,)).fetchone():
        return True
    else:
        return False
