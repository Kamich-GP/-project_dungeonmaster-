from telebot import types


# Кнопка отправки номера
def num_button():
    # Создаем пространство
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Создаем сами кнопки
    but1 = types.KeyboardButton('Отправить номер📞',
                                request_contact=True)
    # Добавляем кнопки в пространство
    kb.add(but1)
    return kb

# Кнопки вывода товаров
def main_menu(products):
    # Создаем пространство
    kb = types.InlineKeyboardMarkup(row_width=2)
    # Создаем сами кнопки
    cart = types.InlineKeyboardButton(text='Корзина🛒', callback_data='cart')
    all_pr = [types.InlineKeyboardButton(text=f'{i[1]}', callback_data=i[0]) for i in products]
    # Добавляем кнопки в пространство
    kb.add(*all_pr)
    kb.row(cart)
    return kb

# Кнопки выбора кол-ва товара
def choose_count_buttons(stock, amount=1, plus_or_minus=''):
    # Создаем пространство
    kb = types.InlineKeyboardMarkup(row_width=3)
    # Создаем сами кнопки
    plus = types.InlineKeyboardButton(text='+', callback_data='increment')
    minus = types.InlineKeyboardButton(text='-', callback_data='decrement')
    count = types.InlineKeyboardButton(text=str(amount), callback_data=str(amount))
    back = types.InlineKeyboardButton(text='Назад🔙', callback_data='back')
    to_cart = types.InlineKeyboardButton(text='В корзину🛒', callback_data='to_cart')
    # Алгоритм изменения кол-ва
    if plus_or_minus == 'increment':
        if amount < stock:
            count = types.InlineKeyboardButton(text=str(amount+1), callback_data=str(amount+1))
    elif plus_or_minus == 'decrement':
        if 1 < amount:
            count = types.InlineKeyboardButton(text=str(amount-1), callback_data=str(amount-1))
    # Добавляем кнопки в пространство
    kb.add(minus, count, plus, back, to_cart)
    return kb

# Кнопка "Назад"
def back_button():
    # Создаем пространство
    kb = types.InlineKeyboardMarkup(row_width=1)
    # Создаем саму кнопку
    back = types.InlineKeyboardButton(text='Назад🔙', callback_data='back')
    # Добавляем кнопку в пространство
    kb.add(back)
    return kb

# Кнопки корзины
def cart_buttons():
    # Создаем пространство
    kb = types.InlineKeyboardMarkup(row_width=2)
    # Создаем сами кнопки
    clear = types.InlineKeyboardButton(text='Очистить корзину🗑️', callback_data='clear')
    order = types.InlineKeyboardButton(text='Оформить заказ🧾', callback_data='order')
    back = types.InlineKeyboardButton(text='Назад🔙', callback_data='back')
    # Добавляем кнопки в пространство
    kb.add(order, clear, back)
    return kb

# Кнопка отправки локации
def loc_button():
    # Создаем пространство
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Создаем сами кнопки
    but1 = types.KeyboardButton('Отправить локацию📍', request_location=True)
    # Добавляем кнопки в пространство
    kb.add(but1)
    return kb
