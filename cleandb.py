from types import resolve_bases
import pymysql
import config


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

def delfromdb(table, user_id):
    connection = getConnection()
    with connection.cursor() as cursor:
        sql = f"DELETE FROM {table} WHERE user_id = {user_id}"
        val = table, user_id
        cursor.execute(sql)
        data = cursor.fetchone()
        return data

#id = 366851392
id = 95033122
#id = 366851392
delfromdb('orders', id)
delfromdb('promocodes', id)
delfromdb('subscribes', id)
delfromdb('trials', id)
delfromdb('users', id)
delfromdb('vpn_users', id)
