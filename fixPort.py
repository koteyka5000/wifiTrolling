from os import system

PORT = 10000

def fix():
    print(system(f'netstat -ano | findstr :{PORT}'))  # Ищем процесс, который использует наш порт
    q = input('PID-->')  # Ввести PID процесса
    system(f'taskkill -pid {q} /f')  # Завершаем этот процесс

fix()