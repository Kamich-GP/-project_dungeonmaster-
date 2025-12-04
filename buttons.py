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
