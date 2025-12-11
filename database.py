import sqlite3

# Подключение к БД
connection = sqlite3.connect('delivery.db', check_same_thread=False)
# Python + SQL
sql = connection.cursor()

# Создание таблиц
sql.execute('CREATE TABLE IF NOT EXISTS users '
            '(tg_id INTEGER, name TEXT, num TEXT);')
sql.execute('CREATE TABLE IF NOT EXISTS products '
            '(pr_id INTEGER PRIMARY KEY AUTOINCREMENT, pr_name TEXT, pr_des TEXT, pr_count INTEGER, '
            'pr_price INTEGER, pr_photo TEXT);')
sql.execute('CREATE TABLE IF NOT EXISTS cart (tg_id INTEGER, user_product TEXT, user_pr_amount INTEGER);')


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

## Методы продуктов ##
# Вывести все товары
def get_all_pr():
    return sql.execute('SELECT * FROM products;').fetchall()

# Вывод товаров для кнопок
def get_pr_buttons():
    return [i[:2] for i in get_all_pr()]

# Вывод конкретного товара
def get_exact_pr(pr_id):
    return sql.execute('SELECT * FROM products WHERE pr_id=?;', (pr_id,)).fetchone()

# Вывод цены товара по названию
def get_pr_price(pr_name):
    return sql.execute('SELECT pr_price FROM products WHERE pr_name=?;', (pr_name,)).fetchone()[0]

## Методы корзины ##
# Добавление товара в корзину
def add_to_cart(tg_id, user_product, user_pr_amount):
    sql.execute('INSERT INTO cart VALUES(?, ?, ?);', (tg_id, user_product, user_pr_amount))
    # Фиксируем изменения
    connection.commit()

# Очистить корзину
def del_from_cart(tg_id):
    sql.execute('DELETE FROM cart WHERE tg_id=?;', (tg_id,))
    # Фиксируем изменения
    connection.commit()

# Вывод корзины
def show_cart(tg_id):
    return sql.execute('SELECT tg_id, user_product, user_pr_amount, SUM(user_pr_amount) as total FROM '
                       'cart WHERE tg_id=? GROUP BY user_product;', (tg_id,)).fetchall()

# Оформление заказа
def make_order(tg_id):
    user_cart = sql.execute('SELECT user_product, user_pr_amount FROM cart WHERE tg_id=?;', (tg_id,)).fetchall()

    for pr_name, pr_count in user_cart:
        # Получаем кол-во товара на складе
        stock = sql.execute('SELECT pr_count FROM products WHERE pr_name=?;', (pr_name,)).fetchone()[0]
        new_count = stock - pr_count
        sql.execute('UPDATE products SET pr_count=? WHERE pr_name=?;', (new_count, pr_name))
    # Фиксируем изменения
    connection.commit()
