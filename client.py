# Права администратора обязательны
from socket import socket, AF_INET, SOCK_STREAM
from os import system
from time import sleep


# > Настройки

# > Ethernet / Беспроводная сеть 
CONNECTION_TYPE = "Ethernet"

# Не трогать
HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 10000  # Port to listen on (non-privileged ports are > 1023)
s = socket(AF_INET, SOCK_STREAM)  # создаем аналогичный сокет, как у сервера
succesfulConnected = False
count = 1

while not succesfulConnected:
    try:
        s.connect(('localhost', PORT))  # коннектимся с сервером
    except ConnectionRefusedError:
        pass
    else:
        succesfulConnected = True
    count += 1
print('\n')

def enable():
    system(f'netsh interface set interface "{CONNECTION_TYPE}" enabled')


def disable():
    system(f'netsh interface set interface "{CONNECTION_TYPE}" disabled')

while True:
    tm = s.recv(1024)  # Принимаем не более 1024 байта данных
    text = tm.decode("utf-8")  # Отправляли в байтах -> Делаем текст
    command, time = text.split()  # Разделяем полученное на команду и аргументы
    if command == "on":
        enable()
    elif command == "off":
        disable()
        if time != '0':
            sleep(int(time))
            enable()
    elif command == 'e':
        s.close()  # Закрыть подключение
        exit()