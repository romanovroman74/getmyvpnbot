from types import resolve_bases
import pymysql
import config
import re
from datetime import date, datetime, timedelta

#Функция подключения к БД
def getConnection():
    connection = pymysql.connect(host=config.mysql_host,
                                 user=config.mysql_user,
                                 password=config.mysql_pw,
                                 db=config.mysql_db,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor,
                                 autocommit=True)
    return connection



########
######## ЗАПРОСЫ
########

#user_id in users
def select_user_id_in_users(user_id):
    connection = getConnection()
    with connection.cursor() as cursor:
        sql = "SELECT COUNT(*) as count FROM users WHERE user_id = %s"
        cursor.execute(sql, user_id)
        data = cursor.fetchone()
        return data

#user_id in subscribes
def select_subscribe_status_in_subscribes(user_id):
    connection = getConnection()
    with connection.cursor() as cursor:
        sql = "SELECT COUNT(*) as count FROM subscribes WHERE user_id = %s AND subscribe_status = 'active'"
        cursor.execute(sql, user_id)
        data = cursor.fetchone()
        return data

#user_id in trials
def select_user_id_in_trials(user_id):
    connection = getConnection()
    with connection.cursor() as cursor:
        sql = "SELECT COUNT(*) as count FROM trials WHERE user_id = %s"
        cursor.execute(sql, user_id)
        data = cursor.fetchone()
        return data

#active_trial_status in trials
def select_active_trial_status_in_trials(user_id):
    connection = getConnection()
    with connection.cursor() as cursor:
        sql = "SELECT COUNT(*) as count FROM trials WHERE user_id = %s AND trial_status = 'active'"
        cursor.execute(sql, user_id)
        data = cursor.fetchone()
        return data

#user_id in vpn_users
def select_user_id_in_vpn_users(user_id):
    connection = getConnection()
    with connection.cursor() as cursor:
        sql = "SELECT COUNT(*) as count FROM vpn_users WHERE user_id = %s"
        cursor.execute(sql, user_id)
        data = cursor.fetchone()
        return data


#vpn_pass in vpn_users
def select_vpn_pass_in_vpn_users(user_id):
    connection = getConnection()
    with connection.cursor() as cursor:
        sql = "SELECT vpn_pass FROM vpn_users WHERE user_id = %s"
        cursor.execute(sql, user_id)
        data = cursor.fetchone()
        return data

#vpn_user_status in vpn_users
def select_vpn_user_status_in_vpn_users(user_id):
    connection = getConnection()
    with connection.cursor() as cursor:
        sql = "SELECT vpn_user_status FROM vpn_users WHERE user_id = %s"
        cursor.execute(sql, user_id)
        data = cursor.fetchone()
        return data


#formed_order_id in orders
def select_formed_order_id_in_orders(user_id):
    connection = getConnection()
    with connection.cursor() as cursor:
        sql = "SELECT MAX(id) FROM orders WHERE user_id = %s"
        cursor.execute(sql, user_id)
        data = cursor.fetchone()
        #row = [item['id'] for item in data]
        return data


#user_id in subscribes
def select_user_id_in_subscribes(user_id):
    connection = getConnection()
    with connection.cursor() as cursor:
        sql = "SELECT COUNT(*) as count FROM subscribes WHERE user_id = %s"
        cursor.execute(sql, user_id)
        data = cursor.fetchone()
        return data

#subscribe_id in subscribes
def select_subscribe_id_in_subscribes(user_id):
    connection = getConnection()
    with connection.cursor() as cursor:
        sql = "SELECT id FROM subscribes WHERE user_id = %s"
        cursor.execute(sql, user_id)
        data = cursor.fetchone()
        return data

#subscribe_status in subscribes
def select_subscribe_status_in_subscribes(user_id):
    connection = getConnection()
    with connection.cursor() as cursor:
        sql = "SELECT subscribe_status FROM subscribes WHERE user_id = %s"
        cursor.execute(sql, user_id)
        data = cursor.fetchall()
        return data

#subcribe_period in orders
def select_subcribe_period_in_orders(order_id):
    connection = getConnection()
    with connection.cursor() as cursor:
        sql = "SELECT subcribe_period FROM orders WHERE id = %s"
        cursor.execute(sql, order_id)
        data = cursor.fetchone()
        return data

#subcribe_datetime_end in subscribes
def select_subcribe_subscribe_datetime_end_in_subscribes(user_id):
    connection = getConnection()
    with connection.cursor() as cursor:
        sql = "SELECT subscribe_datetime_end FROM subscribes WHERE user_id = %s"
        cursor.execute(sql, user_id)
        data = cursor.fetchone()
        return data


#subcribe_status in subscribes
def select_subcribe_subscribe_status_in_subscribes(user_id):
    connection = getConnection()
    with connection.cursor() as cursor:
        sql = "SELECT subscribe_status FROM subscribes WHERE user_id = %s"
        cursor.execute(sql, user_id)
        data = cursor.fetchone()
        return data


#active_subcribe in subcribes
def select_active_subcribes_in_subcribes(user_id):
    connection = getConnection()
    with connection.cursor() as cursor:
        sql = "SELECT COUNT(*) as count FROM subscribes WHERE user_id = %s AND subscribe_status = 'active'"
        cursor.execute(sql, user_id)
        data = cursor.fetchone()
        return data

########
######## ЗАПИСИ
########

#write user_id in users
def write_user_id_in_users(user_id, surname, name, status):
    connection = getConnection()
    with connection.cursor() as cursor:
            sql = "INSERT INTO users(user_id, surname, name, status) VALUES (%s, %s, %s, %s)"
            val = user_id, surname, name, status
            cursor.execute(sql, val)

#write user_id in trials
def write_null_trial_in_trials(user_id, trial_status):
    connection = getConnection()
    with connection.cursor() as cursor:
            sql = "INSERT INTO trials(user_id, trial_status, trial_datetime_begin, trial_datetime_end) VALUES (%s, %s, NOW(), DATE_ADD(NOW(), INTERVAL 3 DAY))"
            val = user_id, trial_status
            cursor.execute(sql, val)

#write user_id in vpn_users
def write_user_id_in_vpn_users(user_id, vpn_user_status, vpn_user_id, vpn_pass):
    connection = getConnection()
    with connection.cursor() as cursor:
            sql = "INSERT INTO vpn_users(user_id, vpn_user_status, vpn_user_id, vpn_pass) VALUES (%s, %s, %s, %s)"
            val = user_id, vpn_user_status, vpn_user_id, vpn_pass
            cursor.execute(sql, val)

#write user_id in orders
def write_user_id_in_orders(user_id, order_status, order_item, subcribe_period, order_amount):
    connection = getConnection()
    with connection.cursor() as cursor:
            sql = "INSERT INTO orders(user_id, order_datetime, order_status, order_item, subcribe_period, order_amount) VALUES (%s, NOW(), %s, %s, %s, %s)"
            val = user_id, order_status, order_item, subcribe_period, order_amount
            cursor.execute(sql, val)

#write user_id in subscribes
def write_user_id_in_subscribes(user_id, subscribe_period, subscribe_period2):
    period = subscribe_period
    connection = getConnection()
    with connection.cursor() as cursor:
            sql = "INSERT INTO subscribes(user_id, subscribe_period, subscribe_status, subscribe_datetime_begin, subscribe_datetime_end) VALUES (%s, %s, 'active', NOW(), DATE_ADD(NOW(), INTERVAL %s MONTH))"
            val = user_id, subscribe_period, subscribe_period2
            cursor.execute(sql, val)

########
######## ОБНОВЛЕНИЕ
########
#trial_status in trials
def update_trial_status_in_trials(trial_status, user_id):
    connection = getConnection()
    with connection.cursor() as cursor:
            sql = "UPDATE trials SET trial_status = %s WHERE user_id = %s"
            val = trial_status, user_id
            cursor.execute(sql, val)

#order_status in orders
def update_order_status_in_orders(order_id):
    connection = getConnection()
    with connection.cursor() as cursor:
            sql = "UPDATE orders SET order_status = 'paid' WHERE id = %s"
            val = order_id
            cursor.execute(sql, val)

#subscription_datetime_end in subscriptions
#ДОПИСАТЬ ДОБАВЛЕНИЕ ДАТЫ К ЗНАЧЕНИЮ subscription_datetime_end а не к NOW
def update_subscription_datetime_end_in_subscriptions(month, subscribe_id):
    connection = getConnection()
    with connection.cursor() as cursor:
            sql = "UPDATE subscribes SET subscribe_datetime_end = DATE_ADD(NOW(), INTERVAL %s MONTH) WHERE id = %s"
            val = month, subscribe_id
            cursor.execute(sql, val)

update_subscription_datetime_end_in_subscriptions(1, 41)

#subscibe_status in subscribes
def update_subscribe_status_in_subscribes(subscribe_id):
    connection = getConnection()
    with connection.cursor() as cursor:
            sql = "UPDATE subscribes SET subscribe_status = 'active' WHERE id = %s"
            val = subscribe_id
            cursor.execute(sql, val)

def update_vpn_user_status_in_vpn_users(user_id):
    connection = getConnection()
    with connection.cursor() as cursor:
            sql = "UPDATE vpn_users SET vpn_user_status = 'active' WHERE user_id = %s"
            val = user_id
            cursor.execute(sql, val)

########
######## УДАЛЕНИЕ
########

#formed_order_id in orders
def delete_formed_order_id_in_orders(user_id):
    connection = getConnection()
    with connection.cursor() as cursor:
        sql = "DELETE FROM orders WHERE user_id = %s AND order_status = 'formed'"
        cursor.execute(sql, user_id)
        data = cursor.fetchone()
        return data






#Запись пользователя в таблицу users




#Функция проверки НАЛИЧИЯ записи о АКТИВНОЙ ПОДПИСКЕ в таблице users
def checkUsersubcribe_active(user_id):
    connection = getConnection()
    with connection.cursor() as cursor:
        sql = "SELECT COUNT(*) as count FROM users WHERE user_id = %s AND subscription IS NOT NULL"
        cursor.execute(sql, user_id)
        data = cursor.fetchone()
        return data




#Функция записи информации о НАЧАТОМ ПЕРИОДЕ ТРИАЛ в таблицу users
def setUsertrial(user_id):
    connection = getConnection()
    with connection.cursor() as cursor:
            sql = "UPDATE users SET trial_state = 'active', subscription = 'trial', subscription_date_end = DATE_ADD(NOW(), INTERVAL 3 DAY) WHERE user_id = %s"
            cursor.execute(sql, user_id)
            data = cursor.fetchone()
            return data


#Функция проверки НАЛИЧИЯ записи о АДМИНЕ в таблице admins
def checkAdmin(user_id):
    connection = getConnection()
    with connection.cursor() as cursor:
        sql = "SELECT COUNT(*) as count FROM admins WHERE user_id = %s"
        cursor.execute(sql, user_id)
        data = cursor.fetchone()
        return data
        

#Функция записи информации о АДМИНЕ в таблицу admins
def writeAdmin(user_id, surname, name, status):
    connection = getConnection()
    with connection.cursor() as cursor:
            sql = "INSERT INTO admins(user_id, surname, name, status) VALUES (%s, %s, %s, %s)"
            val = user_id, surname, name,'active'
            cursor.execute(sql, val)

#Функция запроса о НАЛИЧИИ ЗАПИСИ О ДИАЛОГЕ из таблицы dialogs
def getDialogstatus(user_id):
    connection = getConnection()
    with connection.cursor() as cursor:
        sql = "SELECT COUNT(*) as count FROM dialogs WHERE user_id = %s"
        cursor.execute(sql, user_id)
        data = cursor.fetchone()
        return data

#Функция запроса о НАЛИЧИИ ЗАПИСИ О ДИАЛОГЕ С АДМИНОМ из таблицы dialogs
def getDialogadminstatus(user_id):
    connection = getConnection()
    with connection.cursor() as cursor:
        sql = "SELECT COUNT(*) as count FROM dialogs WHERE user_id = %s AND status = 'admin' AND admin_id IS NOT NULL"
        cursor.execute(sql, user_id)
        data = cursor.fetchone()
        return data

#Функция записи о ДИАЛОГЕ в таблицу users
def writeDialog(user_id, status, date):
    connection = getConnection()
    with connection.cursor() as cursor:
            sql = "INSERT INTO dialogs(user_id, status, date) VALUES (%s, %s, %s)"
            val = user_id, status, date
            cursor.execute(sql, val)

#Функция удаления информации о КОНСУЛЬИРУЮЩЕМ в таблицу users
def delChat(user_id):
    connection = getConnection()
    with connection.cursor() as cursor:
            sql = "UPDATE users SET adminchat_id = NULL WHERE user_id = %s"
            val = user_id
            cursor.execute(sql, val)


#Функция запроса о СТАТУСЕ пользователя из таблицы users
def getUserstatus(user_id):
    connection = getConnection()
    with connection.cursor() as cursor:
            sql = "SELECT status FROM users WHERE user_id = %s"
            cursor.execute(sql, user_id)
            data = cursor.fetchone()
            return data

#Функция запроса о ID пользователя из таблицы users
def getIDstatus(user_id):
    connection = getConnection()
    with connection.cursor() as cursor:
            sql = "SELECT host_id FROM users WHERE user_id = %s"
            cursor.execute(sql, user_id)
            data = cursor.fetchone()
            return data

#Функция запроса информации о статусе пользователе из таблицы users
def getUserstatus(user_id):
    connection = getConnection()
    with connection.cursor() as cursor:
            sql = "SELECT status FROM users WHERE user_id = %s"
            cursor.execute(sql, user_id)
            data = cursor.fetchone()
            return data

#Функция получения забанненых пользователей и их user_id
def getUserban():
    connection = getConnection()
    with connection.cursor() as cursor:
            sql = "SELECT * from users WHERE status = 'banned'"
            cursor.execute(sql)
            data = cursor.fetchone()
            return data

#Функция бана пользователя
def setUserban(user_id):
    connection = getConnection()
    with connection.cursor() as cursor:
            sql = "UPDATE users SET status = 'banned' WHERE user_id = %s"
            cursor.execute(sql, user_id)
            data = cursor.fetchone()
            return data

#Функция анбана пользователя
def setUserunban(user_id):
    connection = getConnection()
    with connection.cursor() as cursor:
            sql = "UPDATE users SET status = 'active' WHERE user_id = %s"
            cursor.execute(sql, user_id)
            data = cursor.fetchone()
            return data

# Фунукция записи ПОЛЬЗОВАТЕЛЬСКИХ СООБЩЕНИЙ в таблицу history;
def writeUsermessage(user_id, message_text, datetime):
    connection = getConnection()
    with connection.cursor() as cursor:
            sql = "INSERT INTO history(user_id, message_text, date) VALUES (%s, %s, %s)"
            val = user_id, message_text, datetime
            cursor.execute(sql, val)

# Функия получения текущего времени
def getTime():
    format = "%Y-%m-%d %H:%M:%S"
    current_time_in_utc = datetime.utcnow()
    data = current_time_in_utc + timedelta(hours=5)
    return data.strftime(format)

# Функция поиска ID в сообщении
def numFilter(user_id):
    connection = getConnection()
    with connection.cursor() as cursor:
        sql = "SELECT message_text FROM user_messages WHERE user_id = %s"
        cursor.execute(sql, user_id)
        data = cursor.fetchall()
        row = [item['message_text'] for item in data]
        for i in row.split:
           result=int(filter(str.isdigit, i))
           print(result)

