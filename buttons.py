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
