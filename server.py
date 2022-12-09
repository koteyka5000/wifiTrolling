from socket import *

print('START 1')
HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 10000  # Port to listen on (non-privileged ports are > 1023)

s = socket(AF_INET, SOCK_STREAM)  # Создается сокет протокола TCP
s.bind(('localhost', PORT))  # Присваиваем ему порт 10000
s.listen(10)  # Максимальное количество одновременных запросов

client, addr = s.accept()  # акцептим запрос на соединение


def send_to_server(q):
    client.send(q.encode('utf-8'))  # передаем данные, предварительно упаковав их в байты

while 1:
    send_to_server(input('-> '))
