import config
import mysql_handler as mysql

import mikrotik_handler as mikrotik
import markups_handler as markup
import payments_handler as pay
from datetime import datetime

import telebot

bot = telebot.TeleBot(config.token)

def ios_set(user_id, pasw):
            img_path = 'img/howto/ios'
            #1
            bot.send_message(user_id, '*Шаг 1.* Перейди в "Настройки" -> "Основные"', parse_mode='Markdown')
            bot.send_photo(user_id, photo=open(f'{img_path}/ios_step1.png', 'rb'))
            #2
            bot.send_message(user_id, '*Шаг 2.* Выбери "VPN и управление устройством"', parse_mode='Markdown')
            bot.send_photo(user_id, photo=open(f'{img_path}/ios_step2.png', 'rb'))
            #3
            bot.send_message(user_id, '*Шаг 3.* Тап сюда', parse_mode='Markdown')
            bot.send_photo(user_id, photo=open(f'{img_path}/ios_step3.png', 'rb'))
            #4
            bot.send_message(user_id, '*Шаг 4.*\nВыбери "Добавить конфигурацию VPN..."', parse_mode='Markdown')
            bot.send_photo(user_id, photo=open(f'{img_path}/ios_step4.png', 'rb'))
            #5
            bot.send_message(user_id, f'*Шаг 5.*Теперь заполни поля так:', parse_mode='Markdown')
            bot.send_photo(user_id, photo=open(f'{img_path}/ios_step5.png', 'rb'))
            bot.send_message(user_id, f'Тип (5): L2TP\n\nОписание (6): GETMYVPN\n\nСервер: `{config.vpnserver}` _(нажми на адрес для копирования)_\n\nУчетная запись (8): `{user_id}` _(нажми на текст для копирования)_\n\nRSA SecurID (9) - выключено\n\nПароль (10): `{pasw}` _(нажми на пароль для копирования)_\n\nОбщий ключ (11): `{config.sharekey}` _(нажми на ключ для копирования)_\n\nДля всех данных (12) - включено\n\nПрокси (13) - "Выкл."\n\n\nТеперь нажми "Готово" сверху (14)', parse_mode='Markdown')
            #6
            bot.send_message(user_id, f'*Шаг 6.* Сейчас нужно включить этот переключатель (15) и дождаться смены статуса (16):', parse_mode='Markdown')
            bot.send_photo(user_id, photo=open(f'{img_path}/ios_step6.png', 'rb'))
            #7
            bot.send_message(user_id, f'*Шаг 7.* Если статус (17), сменился на "Подключено", значит ты все настроил правильно и VPN работает. На этом настройка завершена.', parse_mode='Markdown')
            bot.send_photo(user_id, photo=open(f'{img_path}/ios_step7.png', 'rb'))
            #7
            bot.send_message(user_id, f'*Шаг 8.* В финале, вот тут должен появиться на секунду значек "VPN"', parse_mode='Markdown')
            bot.send_photo(user_id, photo=open(f'{img_path}/ios_step8.png', 'rb'))
            bot.send_message(user_id, f'*Шаг 9.* Пользуйся!', parse_mode='Markdown')

def ios_use(user_id):
            img_path = 'img/howto/ios'
            #1
            bot.send_message(user_id, '*Шаг 1.* Перейди в "Настройки" -> "Основные"', parse_mode='Markdown')
            bot.send_photo(user_id, photo=open(f'{img_path}/ios_step1.png', 'rb'))
            #2
            bot.send_message(user_id, '*Шаг 2.* Включи переключатель VPN', parse_mode='Markdown')
            bot.send_photo(user_id, photo=open(f'{img_path}/ios_use_step1.png', 'rb'))
            #3
            bot.send_message(user_id, '*Шаг 3.* Убедись, что в шапке сверху появился значек VPN, это означает, что соединение - установлено.', parse_mode='Markdown')
            bot.send_photo(user_id, photo=open(f'{img_path}/ios_use_step2.png', 'rb'))
            #4
            bot.send_message(user_id, '*Шаг 3.* Пользуйся!', parse_mode='Markdown')

def macos_set(user_id, pasw):
            img_path = 'img/howto/macos'
            #1
            bot.send_message(user_id, '*Шаг 1.* Нажми на "Яблоко" в левом верхнем углу"', parse_mode='Markdown')
            bot.send_photo(user_id, photo=open(f'{img_path}/macos_step1.png', 'rb'))
            #2
            bot.send_message(user_id, '*Шаг 2.* Выбери "Системные настройки"', parse_mode='Markdown')
            bot.send_photo(user_id, photo=open(f'{img_path}/macos_step2.png', 'rb'))
            #3
            bot.send_message(user_id, '*Шаг 3.* Найди "Сеть"', parse_mode='Markdown')
            bot.send_photo(user_id, photo=open(f'{img_path}/macos_step3.png', 'rb'))
            #4
            bot.send_message(user_id, '*Шаг 4.* Теперь нажми "+" (4)', parse_mode='Markdown')
            bot.send_photo(user_id, photo=open(f'{img_path}/macos_step4.png', 'rb'))
            #5
            bot.send_message(user_id, f'*Шаг 5.* И заполни поля так:', parse_mode='Markdown')
            bot.send_photo(user_id, photo=open(f'{img_path}/macos_step5.png', 'rb'))
            bot.send_message(user_id, f'Интерфейс (5): VPN\n\nТип VPN (6): L2TP через IPSEC \n\nИмя службы (7): `GETMYVPN`\n\n Теперь нажми кнопку "Создать"', parse_mode='Markdown')
            #6
            bot.send_message(user_id, f'*Шаг 6.* Поставь галку (8)\n\nВведи адрес сервера (9): `{config.vpnserver}` _(нажми на адрес для копирования)_\n\nИмя учётной записи (10): `{user_id}` _(нажми на текст для копирования)_\n\nИ нажми на "Настройки аутентификации (11)"', parse_mode='Markdown')
            bot.send_photo(user_id, photo=open(f'{img_path}/macos_step6.png', 'rb'))
            #7
            bot.send_message(user_id, f'*Шаг 7.* Введи пароль (12): `{pasw}` _(нажми на пароль для копирования)_\n\nИ общий ключ (13): `{config.sharekey}` _(нажми на ключ для копирования)_\n\n ОК (14)', parse_mode='Markdown')
            bot.send_photo(user_id, photo=open(f'{img_path}/macos_step7.png', 'rb'))
            #8
            bot.send_message(user_id, f'*Шаг 8.* Теперь нажми на кнопку "Дополнительно"', parse_mode='Markdown')
            bot.send_photo(user_id, photo=open(f'{img_path}/macos_step8.png', 'rb'))
            #9
            bot.send_message(user_id, f'*Шаг 9.* Поставь галку "Отправлять весь трафик через VPN" (16) и нажми кнопку "ОК" (17)', parse_mode='Markdown')
            bot.send_photo(user_id, photo=open(f'{img_path}/macos_step9.png', 'rb'))
            #10
            bot.send_message(user_id, f'*Шаг 10.* Нажми на кнопку "Применить" (18) и кнопку "Подключить" (19)', parse_mode='Markdown')
            bot.send_photo(user_id, photo=open(f'{img_path}/macos_step10.png', 'rb'))
            #11
            bot.send_message(user_id, f'*Шаг 11.* Если статус (20) изменился на "Подключено", значит ты все сделал правильно, можно пользоваться', parse_mode='Markdown')
            bot.send_photo(user_id, photo=open(f'{img_path}/macos_step11.png', 'rb'))

def macos_use(user_id):
            img_path = 'img/howto/macos'
            #1
            bot.send_message(user_id, '*Шаг 1.* Найди этот значек в правом верхнем углу своего Mac"', parse_mode='Markdown')
            bot.send_photo(user_id, photo=open(f'{img_path}/macos_use_step1.png', 'rb'))
            #2
            bot.send_message(user_id, '*Шаг 2.* Выбери "Подключить GETMYVPN"', parse_mode='Markdown')
            bot.send_photo(user_id, photo=open(f'{img_path}/macos_use_step2.png', 'rb'))
            #3
            bot.send_message(user_id, '*Шаг 3.* Убедись, что время начало идти, это означает, что VPN - подключен', parse_mode='Markdown')
            bot.send_photo(user_id, photo=open(f'{img_path}/macos_use_step3.png', 'rb'))
            #4
            bot.send_message(user_id, '*Шаг 4.* Пользуйся', parse_mode='Markdown')
 