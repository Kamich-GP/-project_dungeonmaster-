import telebot
import buttons
import database

# Создаем объект бота
bot = telebot.TeleBot('TOKEN')

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    # Проверяем пользователя на наличие в БД
    if database.check_user(user_id):
        bot.send_message(user_id, 'Добро пожаловать!',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
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
    else:
        bot.send_message(user_id, 'Номер некорректный. Отправь по кнопке, ковбой)')
        # Возвращение на этап получения номера
        bot.register_next_step_handler(message, get_num, user_name)

# Запуск бота
bot.polling(non_stop=True)
