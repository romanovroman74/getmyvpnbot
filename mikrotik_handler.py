import config
import netmiko
import random
from netmiko import ConnectHandler
import mysql_handler as mysql

#Подключаемся к микротику
mikrotik_router_1 = {
'device_type': 'mikrotik_routeros',
'host': '65.21.7.81',
'port': '22',
'username': 'vpnbot',
'password': 'ZAgu3hXkfA6n'
}

#Функция создания и сброса нового vpn-пользователя на mikrotik
def write_vpn_user(user_id):
    #Словарь для пароля
    chars = list('wabcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')  
    #Задаем длину пароля
    length = 8
    #Генерируем пароль из словаря
    random.shuffle(chars)
    #Получаем переменную с паролем
    pasw = ''.join([random.choice(chars) for x in range(length)])
    ssh_cli = ConnectHandler(**mikrotik_router_1)
    #Удаляем впн-пользователя, если есть таковой
    command1 = ssh_cli.send_command(f"/ppp/secret remove [/ppp/secret find name={user_id}]")
    print(command1)
    #Создаём пользователя
    command2 = ssh_cli.send_command(f"ppp secret/add name={user_id} password={pasw} service=l2tp profile=l2tp")
    print(command2)
    ssh_cli.disconnect()
    return pasw

#Функция удаления  vpn-пользователя с mikrotik
def del_vpn_user(user_id):
    ssh_cli = ConnectHandler(**mikrotik_router_1)
    #Удаляем впн-пользователя, если есть таковой
    command1 = ssh_cli.send_command(f"/ppp/secret remove [/ppp/secret find name={user_id}]")
    print(command1)
    ssh_cli.disconnect()

#Функция включения  vpn-пользователя на mikrotik
def enable_vpn_user(user_id):
    ssh_cli = ConnectHandler(**mikrotik_router_1)
    #Включаем впн-пользователя, если есть таковой
    command1 = ssh_cli.send_command(f"/ppp/secret enable [/ppp/secret find name={user_id}]")
    print(command1)
    ssh_cli.disconnect()


#Функция выключения  vpn-пользователя на mikrotik
def disable_vpn_user(user_id):
    ssh_cli = ConnectHandler(**mikrotik_router_1)
    #Включаем впн-пользователя, если есть таковой
    command1 = ssh_cli.send_command(f"/ppp/secret disable [/ppp/secret find name={user_id}]")
    print(command1)
    ssh_cli.disconnect()
    