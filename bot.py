import config
import mysql_handler as mysql

import mikrotik_handler as mikrotik
import markups_handler as markup
import payments_handler as pay
import howto as instruct
from datetime import datetime

import telebot

bot = telebot.TeleBot(config.token)

markdown = """
            *bold text*
            _italic text_
            [text](URL)
            """

# Обработчик inline клавиатуры
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call): 
    user_id = call.message.chat.id
    inline_message_id = call.inline_message_id
    
    
    if call.message:
        if call.data == "more":
            bot.send_message(user_id, 'Я знаю, что РКН уже отключили Instagram, FaceBook. На очереди YouTube. Люди покупают VPN в магазинах, и получают блокировку⛔️ потому, что РКН🇷🇺 находит и блокирует все публичные VPN-сервисы.\n\nВы устали устанавливать каждый день новые непонятные VPN-приложения и платить деньги за неработающие сервисы?\n\nХотите спокойно сидеть во всех заблокированных источниках, с сервисом, который никогда не заблокируют?\n\n*Мои основные преимущества:*\n✅ С моим VPN ты сможешь спокойно посещать все заблокированные сервисы\n✅ Твой траффик будет полностью скрыт. Это полезно, особено при использовании ненадженых Wi-Fi сетей\n✅ Я стою как 1 бизнес-ланч в твоём любимом ресторане\n✅ Я надежен как швейцарские часы\n✅ А еще я шифрую твоё интернет-соединение, защищая твои данные от хакеров, слежки провайдера и правительства\n✅ Моя скорость не оставит равнодушным никого', parse_mode='Markdown',reply_markup=markup.tariffs())
        elif call.data == "tariffs":
            bot.send_message(user_id, 'Я приготовил для тебя несколько тарифов\n\n‼️*Бесплатный пробный период 3 дня*‼️\nЭто для того, что бы ты мог понять, насколько я хорош.\n\n А затем:\n\n➡️ На 1 месяц за *490 ₽*\n\n➡️ На 3 месяца за *1 250 ₽* _(экономия 15%)_\n\n➡️ На 12 месяцев за *4 990 ₽* _(2 месяца в подарок)_', parse_mode='Markdown',reply_markup=markup.buy_with_trial())
        elif call.data == "trial":
            #Проверяем, активен ли пробный период
            trial = mysql.select_active_trial_status_in_trials(user_id)['count']     
            if trial == 0:
                #Текст на ожидание
                bot.send_message(user_id, 'Минутку☝️, сейчас я все подготовлю для тебя', parse_mode='Markdown')
                #Запускаем функцию создания пользователя на Микротик
                vpn_pass = mikrotik.write_vpn_user(user_id)
                #Вносим изменения в базу, активируем пробного периода
                mysql.write_null_trial_in_trials(user_id, 'active')
                #Отправляем пльзователю логин и пароль от микротика
                bot.send_message(user_id, f'✅ Бесплатный пробный период - активирован на 3️⃣ дня!\n⚠️ Для подключения используй следующие данные:\n➖➖➖➖➖➖➖➖\n\n_МОЖНО ПРОСТО НАЖИМАТЬ НА ТЕКСТ ДЛЯ ЕГО КОПИРОВАНИЯ_\n\nУчётная запись: `{user_id}`\nПароль: `{vpn_pass}`\nОбщий ключ: `{config.sharekey}`\nСервер: `{config.vpnserver}`\n➖➖➖➖➖➖➖➖', parse_mode='Markdown', reply_markup=markup.howto())
                #Заносим изменения в базу
                mysql.write_user_id_in_vpn_users(user_id, 'active', user_id, vpn_pass)
            else:
                bot.send_message(user_id, f'‼️ Похоже, что ты уже активировал бесплатный пробный период.☝️ Используй его, если он еще не истёк или оформи новую подписку.', parse_mode='Markdown', reply_markup=markup.buy_without_trial())

        #Отправка пароля из базы
        elif call.data == "resetpass":
                #Проверяем, есть ли подписка
                subscribe = mysql.select_active_subcribes_in_subcribes(user_id)['count']
                if subscribe > 0:
                    #Запрашиваем пароль в базе
                    pasw = mysql.select_vpn_pass_in_vpn_users(user_id)['vpn_pass']
                    #Отправляем пользователю логин и пароль от микротика
                    bot.send_message(user_id, f'Хорошо, что у меня все записано 😉 \n⚠️ Твои данные для подключения:\n➖➖➖➖➖➖➖➖\n\n_МОЖНО ПРОСТО НАЖИМАТЬ НА ТЕКСТ ДЛЯ ЕГО КОПИРОВАНИЯ_\n\nУчётная запись: `{user_id}`\nПароль: `{pasw}`\nОбщий ключ: `{config.sharekey}`\nСервер: `{config.vpnserver}`\n➖➖➖➖➖➖➖➖', parse_mode='Markdown', reply_markup=markup.howto())
                else:
                    #Проверяем есть ли активный триал     
                    trial = mysql.select_active_trial_status_in_trials(user_id)['count']     
                    if trial == 1: 
                        #Запрашиваем пароль в базе
                        pasw = mysql.select_vpn_pass_in_vpn_users(user_id)['vpn_pass']
                        #Отправляем пльзователю логин и пароль от микротика
                        bot.send_message(user_id, f'Хорошо, что у меня все записано 😉 \n⚠️ Твои данные для подключения:\n➖➖➖➖➖➖➖➖\n\n_МОЖНО ПРОСТО НАЖИМАТЬ НА ТЕКСТ ДЛЯ ЕГО КОПИРОВАНИЯ_\n\nУчётная запись: `{user_id}`\nПароль: `{pasw}`\nОбщий ключ: `{config.sharekey}`\nСервер: `{config.vpnserver}``\n➖➖➖➖➖➖➖➖', parse_mode='Markdown', reply_markup=markup.howto())
                    else:   
                        bot.send_message(user_id, f'‼️ Похоже, что ты уже активировал бесплатный пробный период ☝️ Используй его, если он еще не истёк или оформи подписку.', parse_mode='Markdown', reply_markup=markup.buy_without_trial()) 
      
      
        elif call.data == "check_subscribe":
            #Проверяем, есть ли подписка
            subscribe = mysql.select_active_subcribes_in_subcribes(user_id)['count']
            if subscribe > 0:
                #Запрашиваем дату окнчания подписки
                subscribe = mysql.select_subcribe_subscribe_datetime_end_in_subscribes(user_id)['subscribe_datetime_end']
                bot.send_message(user_id, f'✅ Твоя подписка активна и истекает: {subscribe}', parse_mode='Markdown')  
                ###
                ###Запрашиваем сколько дней осталось
                ###
            else:
                #Проверяем есть ли активный триал
                trial = mysql.select_active_trial_status_in_trials(user_id)['count']
                if trial > 0:
                    bot.send_message(user_id, f'⚠️ Похоже, что у тебя активирован бесплатный пробный период. Подписки нет. Предлагаю это исправить 😉', parse_mode='Markdown', reply_markup=markup.buy_without_trial())  
                else:
                    bot.send_message(user_id, f'‼️ Похоже, что у тебя нет действующих подписок. Предлагаю ее оформить 😉', parse_mode='Markdown', reply_markup=markup.buy_without_trial())  
    
    
        elif call.data == "howto":
            bot.send_message(user_id, 'Какая платформа тебя интересует? ⏩', parse_mode='Markdown', reply_markup=markup.instructions())
        elif call.data == "ios":
            bot.send_message(user_id, '✅ Инструкция для настройки VPN на iPhone/iPad ⏩', parse_mode='Markdown')
            bot.send_document(user_id, open(r'file/manual_iOS.pdf', 'rb'))
        elif call.data == "macos":
            bot.send_message(user_id, '✅ Инструкция для настройки VPN на MacOS ⏩', parse_mode='Markdown')
            bot.send_document(user_id, open(r'file/manual_macOS.pdf', 'rb'))
        elif call.data == "windows":
            bot.send_message(user_id, '✅ Инструкция для настройки VPN на Windows 10/11 ⏩', parse_mode='Markdown')
            bot.send_document(user_id, open(r'file/manual_windows10.pdf', 'rb'))
        elif call.data == "android":
            bot.send_message(user_id, '⁉️ Уточни, какой у тебя Android ⏩', parse_mode='Markdown',reply_markup=markup.android())
        elif call.data == "samsung":
            bot.send_message(user_id, '✅ Инструкция для настройки VPN на Samsung и др. ⏩', parse_mode='Markdown')
            bot.send_document(user_id, open(r'file/manual_samsung.pdf', 'rb'))
        elif call.data == "xiaomi":
            bot.send_message(user_id, '✅ Инструкция для настройки VPN на Xiaomi и др. ⏩', parse_mode='Markdown')
            bot.send_document(user_id, open(r'file/manual_xiaomi.pdf', 'rb'))
        elif call.data == "honor":
            bot.send_message(user_id, '✅ Инструкция для настройки VPN HONOR\HUAWEI и др. ⏩', parse_mode='Markdown')
            bot.send_document(user_id, open(r'file/manual_honor.pdf', 'rb'))
        elif call.data == "FAQ": 
            bot.send_message(user_id, 'Выбери вопрос ⏩', parse_mode='Markdown', reply_markup=markup.faq_catalog())
        elif call.data == "q1": 
            bot.send_message(user_id, 'Бесплатным VPN-сервисам трудно конкурировать с платными провайдерами в плане предоставляемых функций и услуг. Качество работы бесплатных VPN, как правило, оставляет желать лучшего, так как серверные соединения зачастую сильно перегружены, у них нет службы поддержки клиентов, они обеспечивают ограниченную или слабую безопасность и у них очень мало VPN-серверов. Бесплатные VPN-сервисы зарабатывают как правило на том, что продают ваш трафик другим людям. Являясь платным провайдером, мы предоставляем подключения, оптимизированные по скорости, безопасности и стабильности. Кроме того, вы можете обращаться в нашу службу поддержки с любыми вопросами в любое время суток.', parse_mode='Markdown', reply_markup=markup.to_faq_catalog())
        elif call.data == "q2": 
            bot.send_message(user_id, 'Все сети VPN потенциально могут замедлять ваше интернет-соединение, но благодаря нашим высокоскоростным VPN-серверам пользователи редко замечают разницу. На самом деле использование VPN может даже улучшить ваше соединение, если ваш провайдер ограничивает вам пропускную способность.', parse_mode='Markdown', reply_markup=markup.to_faq_catalog())
        elif call.data == "q3": 
            bot.send_message(user_id, 'Я рекомендую подключаться к VPN всякий раз, когда вы выходите в Интернет, в идеале — поддерживать подключение постоянно. Оставляя приложение работать в фоновом режиме, вы можете быть спокойны, зная, что ваша конфиденциальность всегда защищена.', parse_mode='Markdown', reply_markup=markup.to_faq_catalog())
        elif call.data == "q4": 
            bot.send_message(user_id, 'Мой VPN защищает вас. Мой VPN использует 256-битное шифрование AES для обеспечения вашей приватности и безопасной работы в Сети. Кроме того, наша политика отсутствия журналов гарантирует, что ваши данные не попадут в чужие руки — в том числе правительству и правоохранительным органам.', parse_mode='Markdown', reply_markup=markup.to_faq_catalog())
        elif call.data == "q5": 
            bot.send_message(user_id, 'Мой VPN скрывает ваш IP адрес и перенаправляет ваш интернет-трафик через зашифрованный VPN-туннель. Это позволяет защитить вашу цифровую личность от слежки вашего провайдера, государственных органов и хакеров', parse_mode='Markdown', reply_markup=markup.to_faq_catalog())
        elif call.data == "faq_catalog": 
            bot.send_message(user_id, 'Выбери вопрос ⏩', parse_mode='Markdown', reply_markup=markup.faq_catalog())
        elif call.data == "subscribe":
            bot.send_message(user_id, 'Выбери тариф ⏩', parse_mode='Markdown', reply_markup=markup.catalog())
        elif call.data == "support":
            bot.send_message(user_id, f'⚠️Форма обратной связи в настоящее время находиться в разработке.\n\nПо всем вопросам, ты можешь обратиться к нам на почту support@getmyvpn.ru', parse_mode='Markdown')  
        elif call.data == "1mon":
            bot.send_message(user_id, '✅ Ты выбрал подписку сроком на 1️⃣ месяц.\n➖➖➖➖➖➖➖➖\nЯ не буду автоматически списывать с тебя оплату каждый месяц, т.к. я не храню данные твоих карт и никакую персональную информацию о тебе.\nЧерез 3️⃣0️⃣ дней, тебе необходимо произвести оплату вручную. Не переживай, я напомню тебе об этом.\n➖➖➖➖➖➖➖➖\n⚠️ Для оплаты я буду использовать сервис Ю.Касса, это полностью безопасно для тебя.', parse_mode='Markdown', reply_markup=markup.gotopay1(user_id))
        elif call.data == "3mon":
            bot.send_message(user_id, '✅ Ты выбрал подписку сроком на 3️⃣ месяца.\n➖➖➖➖➖➖➖➖\nЯ не буду автоматически списывать с тебя оплату каждый месяц, т.к. я не храню данные твоих карт и никакую персональную информацию о тебе.\nЧерез 9️⃣0️⃣ дней, тебе необходимо произвести оплату вручную. Не переживай, я напомню тебе об этом.\n➖➖➖➖➖➖➖➖\n⚠️ Для оплаты я буду использовать сервис Ю.Касса, это полностью безопасно для тебя.', parse_mode='Markdown', reply_markup=markup.gotopay2(user_id))
        elif call.data == "12mon":
            bot.send_message(user_id, '✅ Ты выбрал подписку сроком на 1️⃣2️⃣ месяцeв.\n➖➖➖➖➖➖➖➖\nЯ не буду автоматически списывать с тебя оплату каждый месяц, т.к. я не храню данные твоих карт и никакую персональную информацию о тебе.\nЧерез 3️⃣6️⃣5️⃣ дней, тебе необходимо произвести оплату вручную. Не переживай, я напомню тебе об этом.\n➖➖➖➖➖➖➖➖\n⚠️ Для оплаты я буду использовать сервис Ю.Касса, это полностью безопасно для тебя.', parse_mode='Markdown', reply_markup=markup.gotopay3(user_id))
        
        #Проверка оплаты
        elif call.data == "checkpayment":
            #Мессейдж пользователю
            bot.send_message(user_id, 'Один момент, я проверяю данные о твоей оплате.', parse_mode='Markdown')
            #Находим номер заказа
            order_id = mysql.select_formed_order_id_in_orders(user_id)['MAX(id)']
            #Оплачен ли заказ?
            payment_status = pay.check_payment(order_id)
            #Если заказ оплачен
            if payment_status == 'true':
                #Пишем в базу, что заказ оплачен
                mysql.update_order_status_in_orders(order_id)
                #Смотрим, какое количество месяцов в заказе
                subscribe_period = mysql.select_subcribe_period_in_orders(order_id)['subcribe_period']
                #Проверяем есть ли подписка
                subscribe = mysql.select_user_id_in_subscribes(user_id)['count'] 
                #Если подписка есть
                if subscribe > 0:
                   #Получаем id подписки
                   subscribe_id = mysql.select_subscribe_id_in_subscribes(user_id)['id']
                   #Получаем статус подписки
                   subscribe_status = mysql.select_subscribe_status_in_subscribes(user_id)
                   #Если активна, то добавляем дни
                   if subscribe_status == 'active':
                       
                      
                       ###
                       ###ДОБАВИТЬ ТУТ ДОБАВЛЕНИЕ ДНЕЙ ПОДПИСКИ НЕ К ТЕКУЩЕЙ ДАТЕ А К ДАТЕ АКТИВНОЙ ПОДПИСКИ
                       ###

                       #Добавляем купленные дни к текущей подписке
                       mysql.update_subscription_datetime_end_in_subscriptions(subscribe_period, subscribe_id)
                       #Отправляем сообещение пользователю
                       bot.send_message(user_id, 'Твоя подписка обновлена', parse_mode='Markdown')
                   #Если подписка не активна 
                   else:
                       #Активируем подписку
                       mysql.update_subscribe_status_in_subscribes(subscribe_id)
                       #Добавляем купленные дни к текущей подписке текущей даты
                       mysql.update_subscription_datetime_end_in_subscriptions(subscribe_period, subscribe_id)
                       
                       ###
                       ###ДОПИСАТЬ АКТИВАЦИЮ ВПН-ПОЛЬЗОВАТЕЛЯ И ОТПРАВКУ СООБЩЕНИЯ ЮЗЕРУ
                       ###
                
                #Если подписки нет
                else:
                    #Проверяем, активен ли пробный период
                    trial = mysql.select_active_trial_status_in_trials(user_id)['count']     
                    if trial > 0:
                        #завершаем пробный период
                        mysql.update_trial_status_in_trials('finished',user_id)
                    #Создаем подписку
                    mysql.write_user_id_in_subscribes(user_id, subscribe_period, subscribe_period)
                    #Проверяем есть ли vpn_user в базе
                    vpn_user = mysql.select_user_id_in_vpn_users(user_id)['count'] 
                    #Если vpn_user есть
                    if vpn_user > 0:
                        #Проверяем его статус
                        vpn_user_status = mysql.select_vpn_user_status_in_vpn_users(user_id)['vpn_user_status']
                        #Если статус vpn_user активен
                        if vpn_user_status == 'active':
                            #Запрашиваем данные в базе
                            pasw = mysql.select_vpn_pass_in_vpn_users(user_id)['vpn_pass']
                           
                            ###
                            ### ДОБАВИТЬ ТУТ ЗАПРОС ДАТЫ ОКОНЧАНИЯ ПОДПИСКИ ЧТО БЫ УКАЗАТЬ ЕГО В СООБЩЕНИИ
                            ###
                           
                            #Отправляем пользователю логин и пароль от микротика
                            bot.send_message(user_id, f'✅ Отлично! Подписка - активирована!\n⚠️ Для подключения используй следующие данные:\n➖➖➖➖➖➖➖➖\n\n_МОЖНО ПРОСТО НАЖИМАТЬ НА ТЕКСТ ДЛЯ ЕГО КОПИРОВАНИЯ_\n\nУчётная запись: `{user_id}`\nПароль: `{pasw}`\nОбщий ключ: `{config.sharekey}`\nСервер: `{config.vpnserver}`\n➖➖➖➖➖➖➖➖', parse_mode='Markdown', reply_markup=markup.howto())

                        else:
                            #Активируем пользователя в БД
                            mysql.update_vpn_user_status_in_vpn_users(user_id)
                            #Активируем пользователя на микротике
                            mikrotik.enable_vpn_user(user_id)
                            #Отправляем пользователю логин и пароль от микротика
                            bot.send_message(user_id, f'✅ Отлично! Подписка - активирована!\n⚠️ Для подключения используй следующие данные:\n➖➖➖➖➖➖➖➖\n\n_МОЖНО ПРОСТО НАЖИМАТЬ НА ТЕКСТ ДЛЯ ЕГО КОПИРОВАНИЯ_\n\nУчётная запись: `{user_id}`\nПароль: `{pasw}`\nОбщий ключ: `{config.sharekey}`\nСервер: `{config.vpnserver}`\n➖➖➖➖➖➖➖➖', parse_mode='Markdown', reply_markup=markup.howto())
                    else:
                        #Генерируем нового пользователя
                        #Текст на ожидание
                        bot.send_message(user_id, 'Минутку☝️, сейчас я все подготовлю для тебя', parse_mode='Markdown')
                        #Запускаем функцию создания пользователя на Микротик
                        vpn_pass = mikrotik.write_vpn_user(user_id)
                        #Вносим изменения в базу, активируем пробного периода
                        mysql.write_null_trial_in_trials(user_id, 'active')
                        #Отправляем пльзователю логин и пароль от микротика
                        bot.send_message(user_id, f'✅ Отлично! Подписка - активирована!\n⚠️ Для подключения используй следующие данные:\n➖➖➖➖➖➖➖➖\n\n_МОЖНО ПРОСТО НАЖИМАТЬ НА ТЕКСТ ДЛЯ ЕГО КОПИРОВАНИЯ_\n\nУчётная запись: `{user_id}`\nПароль: `{vpn_pass}`\nОбщий ключ: `{config.sharekey}`\nСервер: `{config.vpnserver}`\n➖➖➖➖➖➖➖➖', parse_mode='Markdown', reply_markup=markup.howto())
                        #Заносим изменения в базу
                        mysql.write_user_id_in_vpn_users(user_id, 'active', user_id, vpn_pass)
            
            else:
               bot.send_message(user_id, '❌ Странно, но я пока не вижу информацию о оплате твоей подписки.\nПопробуй нажать на кнопку "Я оплатил" еще раз через несколько секунд.\n\n⚠️ Если ничего не помогает, пожалуйста, напиши нам на почту support@getmyvpn.ru. С тобой быстро свяжутся.', parse_mode='Markdown') 

               
##
## Обработчик команды /start
##
@bot.message_handler(func=lambda message: message.chat.type == 'private', commands=['start'])
def start(message):
    # Основные переменные
    user_id = message.chat.id
    user_lastname = message.from_user.last_name
    user_firstname = message.from_user.first_name
    text = message.text
    if text == '/start':
        #Проверяем есть ли запись о пользователе в таблице user
        rec = mysql.select_user_id_in_users(user_id)['count']
        # Если сообщение отправляется в приват
        if message.chat.type == 'private':
            #Создаем запись, если её нет
            if rec == 0:
                #В таблицу users
                mysql.write_user_id_in_users(user_id, user_lastname, user_firstname, 'active')
                bot.send_message(user_id, 'Привет👋\n\nМеня зовут Валерий! И я приватный vpn-бот.\n\nМеня нет в публичном пространстве, нет в GooglePlay, AppStore, а это означает только одно - меня не смогут забанить и с моей помощью ты всегда сможешь посещать заблокированные ресурсы, а так же быть уверенными в том, что тебя не забанят и твои данные никому не продадут 💵', parse_mode='Markdown', reply_markup=markup.more())
            else:
                bot.send_message(user_id, 'Привет!😊 Я робот - Валера. Чем я могу помочь?', parse_mode='Markdown', reply_markup=markup.help())

##
## Обработчик команды /subscribes
##
@bot.message_handler(func=lambda message: message.chat.type == 'private', commands=['subscribes'])
def subscribes(message):
    # Основные переменные
    user_id = message.chat.id
    user_lastname = message.from_user.last_name
    user_firstname = message.from_user.first_name
    text = message.text
    #Проверяем, есть ли подписка
    subscribe = mysql.select_active_subcribes_in_subcribes(user_id)['count']
    if subscribe > 0:
        #Запрашиваем дату окнчания подписки
        subscribe = mysql.select_subcribe_subscribe_datetime_end_in_subscribes(user_id)['subscribe_datetime_end']
        bot.send_message(user_id, f'✅ Твоя подписка активна и истекает: {subscribe}', parse_mode='Markdown')  
        ###
        ###Запрашиваем сколько дней осталось
        ###
    else:
        bot.send_message(user_id, f'‼️ Похоже, что у тебя нет активной подписки. Давай это исправим 😉', parse_mode='Markdown', reply_markup=markup.buy_without_trial())  

##
## Обработчик команды /howto
##
@bot.message_handler(func=lambda message: message.chat.type == 'private', commands=['howto'])
def howto(message):
    # Основные переменные
    user_id = message.chat.id
    user_lastname = message.from_user.last_name
    user_firstname = message.from_user.first_name
    text = message.text
    bot.send_message(user_id, f'✅ Я приготовил несколько инструкций по настройке моего VPN-сервиса на твоих гаджетах для разных платформ, выбери свою:', parse_mode='Markdown', reply_markup=markup.instructions())  


##
## Обработчик команды /faq
##
@bot.message_handler(func=lambda message: message.chat.type == 'private', commands=['faq'])
def faq(message):
    # Основные переменные
    user_id = message.chat.id
    user_lastname = message.from_user.last_name
    user_firstname = message.from_user.first_name
    text = message.text
    bot.send_message(user_id, 'Выбери вопрос ⏩', parse_mode='Markdown', reply_markup=markup.faq_catalog())

##
## Обработчик команды /trial
##
@bot.message_handler(func=lambda message: message.chat.type == 'private', commands=['trial'])
def faq(message):
    # Основные переменные
    user_id = message.chat.id
    user_lastname = message.from_user.last_name
    user_firstname = message.from_user.first_name
    text = message.text
    bot.send_message(user_id, 'Я приготовил для тебя несколько тарифов\n\n‼️*FREE пробный период 3 дня*‼️\nЭто для того, что бы ты мог понять, насколько я хорош.\n\n А затем:\n\n➡️ На 1 месяц за *490 ₽*\n\n➡️ На 3 месяца за *1 250 ₽* _(экономия 15%)_\n\n➡️ На 12 месяцев за *4 990 ₽* _(2 месяца в подарок)_', parse_mode='Markdown',reply_markup=markup.buy_with_trial())

##
## Обработчик команды /subscribe
##
@bot.message_handler(func=lambda message: message.chat.type == 'private', commands=['subscribe'])
def subscribe(message):
    # Основные переменные
    user_id = message.chat.id
    bot.send_message(user_id, 'Выбери тариф ⏩', parse_mode='Markdown', reply_markup=markup.catalog())



##
## Обработчик команды /support
##
@bot.message_handler(func=lambda message: message.chat.type == 'private', commands=['support'])
def support(message):
    # Основные переменные
    user_id = message.chat.id
    user_lastname = message.from_user.last_name
    user_firstname = message.from_user.first_name
    text = message.text
    bot.send_message(user_id, f'⚠️Форма обратной связи в настоящее время находиться в разработке.\n\nПо всем вопросам, ты можешь обратиться к нам на почту support@getmyvpn.ru\n\nИнструкции по настройке для любых платформ есть в моём разделе "Как настроить"', parse_mode='Markdown', reply_markup=markup.howto())  

#Запуск бота
bot.polling() 