import socket
import os
import pika
import _thread
import time

# os.system('fuser -k 1234/tcp')
ServerSideSocket = socket.socket()
host = "192.168.1.3"
port = 1234
ThreadCount = 0

# credentials = pika.PlainCredentials("avani", "avani")

try:
    ServerSideSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print("Socket is listening..")
ServerSideSocket.listen(20)


def multi_threaded_client(connection):
    i = 1
    while True:
        data = connection.recv(1024)
        if not data:
            break
        i = i + 1
        # Open file
        file = open("wifi_data.txt", "a")
        data_save = (
            str(i)
            + " -- "
            + time.strftime("%H:%M:%S", time.localtime())
            + " -- "
            + str(data.decode("utf-8"))
        )
        # data_save = "Hello"
        file.write(data_save)

        # Close file
        file.close()
        print(data)


while True:
    try:
        while True:
            Client, address = ServerSideSocket.accept()
            _thread.start_new_thread(multi_threaded_client, (Client,))
    except KeyboardInterrupt:
        ServerSideSocket.close()
