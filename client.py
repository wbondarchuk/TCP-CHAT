import socket
import threading

# Выбор ника
nickname = input("Choose your nickname: ")

# Подключение к серверу
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))


# Прослушивание сервера и отправка ников
def receive():
    while True:
        try:
            # Получение сообщения от сервера
            # Если 'NICK' отправляем Nickname
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            # Закрываем соединение при ошибке
            print("An error occured!")
            client.close()
            break


# Отправка сообщений на сервер
def write():
    while True:
        message = '{}: {}'.format(nickname, input(''))
        client.send(message.encode('ascii'))


# Запуск потоков для прослушивания и записи
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()

