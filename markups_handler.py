import config
import payments_handler as pay
import config
import mysql_handler as mysql
from yoomoney import Client
from yoomoney import Quickpay
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def more():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Подробнее ⏩", callback_data="more"))
    return markup

def tariffs():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("🤝 Тарифы", callback_data="tariffs"))
    return markup

def buy_with_trial():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("🤟 Оформить подписку", callback_data="subscribe"),
                InlineKeyboardButton("🆓 Попробовать БЕСПЛАТНО", callback_data="trial"))
    return markup

def buy_without_trial():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("🤟 Оформить подписку", callback_data="subscribe"))
                

    return markup

def howto():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("🤓 Как настроить?", callback_data="howto"))

    return markup

def instructions():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("📱 iPhone/iPad", callback_data="ios"),
                InlineKeyboardButton("📱 Android", callback_data="android"),
                InlineKeyboardButton("🖥 MacOS", callback_data="macos"),
                InlineKeyboardButton("🖥 Windows 10/11", callback_data="windows")
                )

    return markup

def android():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Samsung и др.", callback_data="samsung"),
                InlineKeyboardButton("Xiaomi и др.", callback_data="xiaomi"),
                InlineKeyboardButton("Huawei\Honor", callback_data="honor")
                )
    return markup

def catalog():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("1 месяц за 490 ₽", callback_data="1mon"),
                InlineKeyboardButton("3 месяца за 1 250 ₽", callback_data="3mon"),
                InlineKeyboardButton("12 месяцев за 4 990 ₽", callback_data="12mon"))

    return markup

def gotopay1(user_id):
    #Удаляем предзаказы в базе, если такие есть
    mysql.delete_formed_order_id_in_orders(user_id)
    #Создаем заказ в базе
    mysql.write_user_id_in_orders(user_id, 'formed', 'Subscribe 1 month', 1, 490)
    #Получаем ID заказа из базы
    order_id = mysql.select_formed_order_id_in_orders(user_id)['MAX(id)']
    #Формируем ссылку для оплаты
    payurl = pay.gen_invoice_url(490, 'Оплата сервиса GETMY.VPN сроком на 1 месяц', order_id)
    
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("⏪ Назад", callback_data="subscribe"),
                    InlineKeyboardButton(text="Перейти к оплате ⏩", url=f"{payurl}"),
                    InlineKeyboardButton(text="Я оплатил! ✅", callback_data="checkpayment"))
    return markup

def gotopay2(user_id):
    #Удаляем предзаказы в базе, если такие есть
    mysql.delete_formed_order_id_in_orders(user_id)
    #Создаем заказ в базе
    mysql.write_user_id_in_orders(user_id, 'formed', 'Subscribe 3 month', 3, 1250)
    #Получаем ID заказа из базы
    order_id = mysql.select_formed_order_id_in_orders(user_id)['MAX(id)']
    #Формируем ссылку для оплаты
    payurl = pay.gen_invoice_url(1250, 'Оплата сервиса GETMY.VPN сроком на 3 месяца', order_id)
    
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("⏪ Назад", callback_data="subscribe"),
                    InlineKeyboardButton(text="Перейти к оплате ⏩", url=f"{payurl}"),
                    InlineKeyboardButton(text="Я оплатил! ✅", callback_data="checkpayment"))
    return markup

def gotopay3(user_id):
    #Удаляем предзаказы в базе, если такие есть
    mysql.delete_formed_order_id_in_orders(user_id)
    #Создаем заказ в базе
    mysql.write_user_id_in_orders(user_id, 'formed', 'Subscribe 12 month', 12, 4990)
    #Получаем ID заказа из базы
    order_id = mysql.select_formed_order_id_in_orders(user_id)['MAX(id)']
    #Формируем ссылку для оплаты
    payurl = pay.gen_invoice_url(4990, 'Оплата сервиса GETMY.VPN сроком на 12 месяцев', order_id)
    
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("⏪ Назад", callback_data="subscribe"),
                    InlineKeyboardButton(text="Перейти к оплате ⏩", url=f"{payurl}"),
                    InlineKeyboardButton(text="Я оплатил! ✅", callback_data="checkpayment"))
    return markup

def help():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("🤟 Оформить подписку", callback_data="subscribe"),
                InlineKeyboardButton("💫 Проверить подписку", callback_data="check_subscribe"),
                InlineKeyboardButton("🤓 Как настроить?", callback_data="howto"),
                InlineKeyboardButton("❔ FAQ", callback_data="FAQ"),
                InlineKeyboardButton("😫 Восстановить пароль", callback_data="resetpass"),
                InlineKeyboardButton("🔰 Техподдержка", callback_data="support"))
    return markup

def faq_catalog():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Зачем мне платить за VPN?", callback_data="q1"),
                InlineKeyboardButton("Замедлит ли VPN моё интернет-соединение?", callback_data="q2"),
                InlineKeyboardButton("Стоит ли использовать VPN постоянно?", callback_data="q3"),
                InlineKeyboardButton("Насколько безопасен ваш VPN?", callback_data="q4"),
                InlineKeyboardButton("Как работает VPN?", callback_data="q5"))
    return markup

def to_faq_catalog():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("К списку вопросов", callback_data="faq_catalog"))
    return markup
