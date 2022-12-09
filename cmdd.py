import tkinter as tk
from socket import socket, AF_INET, SOCK_STREAM
from tkinter import messagebox as mb
from colorama import init, Fore
init(autoreset=False)

# Осуществлять выход в локальную сеть как сервер?
isConnect = False

# Время для анимации плавного вывода. По умолчанию 50
TIME_TO_SCROLL = 50

if isConnect:
    HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
    PORT = 10000  # Port to listen on (non-privileged ports are > 1023)

    s = socket(AF_INET, SOCK_STREAM)  # Создается сокет протокола TCP
    s.bind(('localhost', PORT))  # Присваиваем ему порт 10000
    s.listen(10)  # Максимальное количество одновременных запросов
    print(f'Запрос на соединение\nПорт: {PORT}\nАдрес: {HOST}')
    client, addr = s.accept()  # акцептим запрос на соединение


def send(data):
    client.send(data.encode('utf-8'))  # передаем данные, предварительно упаковав их в байты


root = tk.Tk()
root.geometry('400x300')
root['bg'] = 'cyan'
root.title('Cmd')

inputTextVar = tk.StringVar(root)

outputText = tk.Text(root, height=11, width=45, state=tk.DISABLED)
outputText.place(x=20, y=100)

inputText = tk.Entry(root, textvariable=inputTextVar, width=50)
inputText.place(x=20, y=30)

COMMANDS_WIFI = ('wifi',)

def run(commandIn):  # Распределитель команд если не kill
    command = commandIn.split()
    command, *args = command

    if command in COMMANDS_WIFI and isConnect == False: # Проверяем, есть ли подключение для особых команд
        return 'ERR: Для данной команды необходин доступ в localhost'

    if command == 'kill':  # Принудительно закрываем приложение
        if isConnect: # Если подключались к сети
            s.close() # Закрываем соединение
        kill(1)       # Закрываем приложение

    if command[0] == '>':  # Ожидание перед выполнением команды (Beta)
        root.after(int(command[1:]) * 1000)
        command, *args = args
    return connect(command, *args)  # Выполняем команду


def connect(command, *args):  # Обработка команд
    if command == 'shampoo':
        try:
            via = args[0]
            mark = args[1]
            ml = args[2]
            flush = args[3]
        except Exception:
            return 'SyntaxError'
        if not checkCommand('shampoo', *args):  #
            return 'SyntaxError'

        if flush == 'true':
            return f'FLUSHED SHAMPOO via {mark}, {ml} Ml'
        else:
            return f'RUN SHAMPOO -> {mark}, {ml} Ml'

    elif command == 'connect':
        try:
            ip = args[0]
            user = args[1]
        except Exception:
            return 'SyntaxError'
        if not checkCommand('connect', *args):
            return 'connection refused! Incorrect IPv4 Adress'
        return f'connecting to {user} via IPv4: {ip}'

    elif command == 'cls':
        outputText.configure(state='normal')
        outputText.delete(1.0, tk.END)
        outputText.configure(state='disabled')
        inputText.delete(0, tk.END) 
        inputText.focus()
        return ''

    elif command == 'wifi':
        try:
            user = 'uff'      # Пользователь
            action = args[0]  # on / off
            time = args[1]    # Время, на которое отключиться wifi
            wait = args[2]    # Сколько ждать перед отключение wifi
        except Exception:     # Пример:     wifi off 2 0
            return 'ERR: Синтаксис'

        if user != 'dima': # Проверяем пользователя (Он один)
            return f'{user} не найден'

        if action == 'on': # Включить wifi
            send('on 0')
            return f'WiFi user={user} enabled'

        elif action == 'off': # Отключить wifi
            root.after(int(wait)*1000)       # Секунды -> миллисекунды
            print(f'Wait: {int(wait)*1000}') # Выводим сколько ждать
            send(f'off {time}')              # Посылаем запрос на отключение
            return f'WiFi user={user} disabled'

        return 'Что-то пошло не так'

    else:
        return 'IncorrectCommandError'


def checkCommand(cmd, *args):  # Проверка правильности введёной команды
    if cmd == 'shampoo':
        via = args[0]
        mark = args[1]
        ml = args[2]
        flush = args[3]
        return True if via == 'via' and flush == 'true' or flush == 'false' else False

    elif cmd == 'connect':
        try:
            ip = args[0]
            user = args[1]
            q = ip.split('.')
            for w in q:
                w = int(w)
                if not w <= 255 and w >= 0:
                    return False
        except Exception:
            return False
        return True


def kill(event):  # Выход
    exit(144)


def beautifulPrint(text):  # Красивый вывод
    for letter in text:
        root.after(TIME_TO_SCROLL)
        write(letter)
        root.update()
    write('\n')


def write(text):  # Запись в текстовое поле
    outputText.configure(state=tk.NORMAL)
    outputText.insert(tk.END, text)
    outputText.configure(state=tk.DISABLED)


def start(event=None):  # Запуск комманды
    command = inputTextVar.get()
    if len(command) == 0:
        output = 'EmptyStringError'
    else:
        output = run(command)
    beautifulPrint(output)


tk.Button(root, bg='cyan', text='Enter', command=start).place(x=345, y=25)
root.bind('<Alt_L>', start)
root.bind('<Return>', start)
root.bind('<Escape>', kill)


def on_closing():
    if isConnect:
        if mb.askyesno("Предупреждение", "После выхода связь с клиентом не получится восстановить\nВыйти?"):
            print(f'{Fore.RED}Отключение')
            root.destroy()
    else:
        print(f'{Fore.RED}Отключение')
        root.destroy()
    


root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
