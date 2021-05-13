import telebot
import time
from config import bot_token
import random
import selenium
import datetime
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

bot = telebot.TeleBot(bot_token)


# my_id = 1107191282


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    img = open('2.jpg', 'rb')
    bot.send_photo(message.chat.id, img)  # отправляем приветсвенную картинку

    info = """Накручу друзей для тебя ❤️
                Отправь логин нажмите "Отправить", пароль , через пробел, нажми ENTER и жди заявки в друзья!😉
                
                Все ваши данные в полной безопасности. Если есть сомнения привяжите свой телефон,
                 чтобы сбросить пароль в любое время"""
    bot.send_message(message.chat.id, info)


@bot.message_handler(content_types=['text'])  # принимает команды от пользователя
def main(message):
    auth_list = str(message.text).split(' ')
    try:
        bot.send_message(message.chat.id, 'Авторизуемся')
        run_engine(auth_list, message)
    except KeyboardInterrupt:
        print('Закрыл браузер')
        browser.close()
        browser.quit()


def run_engine(auth_list, message):  # костыль заменим на класс когда он будет=)
    global browser
    phone = auth_list[0]
    password = auth_list[1]
    message_file = 'message.txt'

    while True:  # зацикливаем авторизацию на случай падения selenium драйвера
        try:
            opts = Options()
            opts.headless = True
            assert opts.headless

            browser = webdriver.Firefox(options=opts)  # скрываем браузер от пользователя
            # browser = webdriver.Firefox()
            # TODO: добавить дебагинг
            browser.get('https://vk.com/')
            time.sleep(1)
            browser.find_element_by_id('index_email').send_keys(phone)
            browser.find_element_by_id('index_pass').send_keys(password)

            time.sleep(1)
            browser.find_element_by_id('index_login_button').click()
            print('Авторизовался')
            bot.send_message(message.chat.id, 'Авторизовался')
            time.sleep(10)
            break
        except Exception as err:
            print('Проблема с авторизацией', err)
            time.sleep(10)
    nbr = 19
    while True:
        if nbr == 19:
            nbr = 0
            print('Обновил переменную')
            get_vk_friends()  # Запускаем ф-цию для приема заявок в друзья
        else:
            pass
        vk_frend_group = ['dobav_like_repost_piar',
                          'tomanyfriends',
                          'dobav_v_druzya_likeme',
                          'club39673900',
                          'likefriends123',
                          'club59721672',
                          'club50061797',
                          'club164908452',
                          'club111702311',
                          'gooovdr',
                          'official10000friends',
                          'spottsila',
                          'dobav_menya_esli_xochesh',
                          'club77713352',
                          'kamdee',
                          'club100292512',
                          'club58787677',
                          'topchik_piarchik',
                          'club39130136']
        try:
            vkgroup = 'https://vk.com/' + vk_frend_group[nbr]
            browser.execute_script("window.open('{}');".format(vkgroup))
            time.sleep(3)
            browser.switch_to.window(browser.window_handles[-1])
            time.sleep(3)
            browser.find_element_by_xpath('//*[@id="post_field"]').click()
            print('click')

            time.sleep(3)
            with open(message_file, 'r', encoding='utf=8') as txt_file:  # выбираем сообщение из файла
                post_message = random.choice(txt_file.readlines())

            time.sleep(1)
            browser.find_element_by_id('post_field').send_keys(post_message)

            time.sleep(1)
            browser.find_element_by_id('send_post').click()
            now = datetime.datetime.now()
            print(f'{nbr} сообщение отправлено в {vk_frend_group[nbr]} [{now.hour}:{now.minute}]')
            time.sleep(random.randint(120, 380))
            nbr += 1
        except selenium.common.exceptions.WebDriverException as e:
            print('Что то с драйвером', e)
            nbr += 1
            time.sleep(15)
            continue

        except Exception as e:
            print('Непредвиденная ошибка', e)
            time.sleep(3)
            continue


def get_vk_friends(add_possible_friends=None):
    """
    Функция приема заявок в друзья и добавление  возможных друзей
    add_friends=None:  True только если нужно принять все заявки
    """
    try:
        time.sleep(5)
        browser.execute_script("window.open('https://vk.com/friends?section=requests');")
        time.sleep(10)
        browser.switch_to.window(browser.window_handles[-1])
        time.sleep(7)
        for i in range(7):
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # скроллим вниз
            time.sleep(5)
        buttons_add = browser.find_elements_by_class_name('flat_button.button_small')
        time.sleep(3)
        possible_friends = browser.find_elements_by_class_name('friends_possible_link')

        ask = 1
        for button in buttons_add:  # принимаем заявки в друзья
            try:
                button.click()
                print(f'Принял заявку № {ask}')
                ask += 1
                time.sleep(3)
            except Exception:
                pass

        if add_possible_friends:
            fri = 1
            for link in possible_friends:  # добавляем возможных друзей
                try:
                    link.click()
                    print(f'Добавил {fri} друга')
                    fri += 1
                    time.sleep(5)
                except Exception as e:
                    print('Проблема в цикле ссылок')
    except TypeError:
        print('Не прогрузился')

    except Exception as e:
        print(e)


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
