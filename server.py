import socket
import threading

# Данные подключения
host = '127.0.0.1'
port = 55555

# Инициализация сервера
# Создаем сокет
# AF_INET и SOCK_STREAM это константы семейства адресов и типа сокета (это дефолтные значения, но есть другие)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Привязывает сокет к адресу
server.bind((host, port))
# Переводит сервер в режим приема соединений (в скобочках можно указать
# количество соединений которые сервер будет принимать)
server.listen()

# Списки для клиентов и никнеймов
clients = []
nicknames = []


# Отправка сообщений всем подключенным пользователям
def broadcast(message):
    for client in clients:
        client.send(message)


# Обработка сообщений от клиентов
def handle(client):
    while True:
        try:
            # Broadcasting сообщений
            message = client.recv(1024)
            broadcast(message)
        except:
            # Удаление и закрытие клиентов
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break


# Функция приема / прослушивания
def receive():
    while True:
        # Принять подключение
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Запрос и сохранение никнеймов
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        # Печать и передача никнейма
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        # Начать обработку потока для клиента
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


receive()
