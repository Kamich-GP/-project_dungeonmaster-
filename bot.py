import telebot
import buttons
import database

# Создаем объект бота
bot = telebot.TeleBot('TOKEN')
# Временные данные
users = {}

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    # Проверяем пользователя на наличие в БД
    if database.check_user(user_id):
        bot.send_message(user_id, 'Добро пожаловать!',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.send_message(user_id, 'Выберите пункт меню:',
                         reply_markup=buttons.main_menu(database.get_pr_buttons()))
    else:
        bot.send_message(user_id, 'Привет! Давай начнем регистрацию, напиши свое имя',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        # Переход на этап получения имени
        bot.register_next_step_handler(message, get_name)

# Этап получения имени
def get_name(message):
    user_id = message.from_user.id
    user_name = message.text
    # Проверяем, что текст сообщения состоит только из букв
    if message.text.isalpha():
        bot.send_message(user_id, 'Супер! А теперь отправь свой номер!',
                         reply_markup=buttons.num_button())
        # Переход на этап получения номера
        bot.register_next_step_handler(message, get_num, user_name)
    else:
        bot.send_message(user_id, 'Имя некорректно. Напиши свое настоящее имя, ковбой)')
        # Возвращение на этап получения имени
        bot.register_next_step_handler(message, get_name)

# Этап получения номера
def get_num(message, user_name):
    user_id = message.from_user.id
    # Проверка на правильность номера
    if message.contact:
        user_num = message.contact.phone_number
        database.register(user_id, user_name, user_num)
        bot.send_message(user_id, 'Регистрация прошла успешно!',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.send_message(user_id, 'Выберите пункт меню:',
                         reply_markup=buttons.main_menu(database.get_pr_buttons()))
    else:
        bot.send_message(user_id, 'Номер некорректный. Отправь по кнопке, ковбой)')
        # Возвращение на этап получения номера
        bot.register_next_step_handler(message, get_num, user_name)

# Выбор кол-ва продукта
@bot.callback_query_handler(lambda call: call.data in ['increment', 'decrement', 'to_cart', 'back'])
def choose_pr_count(call):
    user_id = call.message.chat.id
    if call.data == 'increment':
        user_count = users[user_id]['product_count'] # Достали текущее кол-во у пользователя
        stock = database.get_exact_pr(users[user_id]['product_id'])[3] # Достали кол-во товара со склада
        if user_count < stock:
            bot.edit_message_reply_markup(chat_id=user_id, message_id=call.message.message_id,
                                          reply_markup=buttons.choose_count_buttons(stock, user_count, 'increment'))
            users[user_id]['product_count'] += 1
    elif call.data == 'decrement':
        user_count = users[user_id]['product_count'] # Достали текущее кол-во у пользователя
        stock = database.get_exact_pr(users[user_id]['product_id'])[3] # Достали кол-во товара со склада
        if 1 < user_count:
            bot.edit_message_reply_markup(chat_id=user_id, message_id=call.message.message_id,
                                          reply_markup=buttons.choose_count_buttons(stock, user_count, 'decrement'))
            users[user_id]['product_count'] -= 1
    elif call.data == 'to_cart':
        user_product = database.get_exact_pr(users[user_id]['product_id'])[1] # Достали название товара
        user_pr_amount = users[user_id]['product_count'] # Достали текущее кол-во у пользователя
        database.add_to_cart(user_id, user_product, user_pr_amount)
        bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
        bot.send_message(user_id, 'Товар успешно помещен в корзину! Желаете что-то еще?',
                         reply_markup=buttons.main_menu(database.get_pr_buttons()))
    elif call.data == 'back':
        bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
        bot.send_message(user_id, 'Выберите пункт меню:',
                         reply_markup=buttons.main_menu(database.get_pr_buttons()))

# Корзина
@bot.callback_query_handler(lambda call: call.data in ['cart'])
def cart_handle(call):
    user_id = call.message.chat.id
    if call.data == 'cart':
        text = 'Ваша корзина:\n\n'
        total = 0
        user_cart = database.show_cart(user_id)
        if user_cart:
            for i in user_cart:
                text += f'Товар: {i[1]}\nКоличество: {i[-1]}\n\n'
                total += database.get_pr_price(i[1]) * i[-1]
            bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
            bot.send_message(user_id, text, reply_markup=buttons.cart_buttons())

# Выбор продукта
@bot.callback_query_handler(lambda call: int(call.data) in [i[0] for i in database.get_all_pr()])
def choose_product(call):
    user_id = call.message.chat.id
    # Достаем данные из БД
    pr_info = database.get_exact_pr(int(call.data))
    if pr_info[3] > 0:
        bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
        bot.send_photo(user_id, photo=pr_info[-1], caption=f'{pr_info[1]}\n\n'
                                                           f'Описание: {pr_info[2]}\n'
                                                           f'Количество: {pr_info[3]}\n'
                                                           f'Цена: {pr_info[4]}сум\n',
                       reply_markup=buttons.choose_count_buttons(pr_info[3]))
        users[user_id] = {'product_id': pr_info[0], 'product_count': 1}
    else:
        bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
        bot.send_photo(user_id, photo=pr_info[-1], caption=f'{pr_info[1]}\n\n'
                                                           f'Описание: {pr_info[2]}\n'
                                                           f'Количество: НЕТ В НАЛИЧИИ\n'
                                                           f'Цена: {pr_info[4]}сум\n',
                       reply_markup=buttons.back_button())

# Запуск бота
bot.polling(non_stop=True)