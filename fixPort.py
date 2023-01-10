from os import system

PORT = 10000

def fix():
    system(f'netstat -o | findstr :{PORT}')  # Ищем процесс, который использует наш порт
    q = input('PID-->')  # Ввести PID процесса
    system(f'taskkill -pid {q} /f')  # Завершаем этот процесс

fix()