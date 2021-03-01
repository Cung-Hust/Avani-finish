import socket
import os
import pika
import _thread
import time

# os.system('fuser -k 1234/tcp')
ServerSideSocket = socket.socket()
host = "192.168.1.5"
port = 1234
ThreadCount = 0

try:
    ServerSideSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print("Socket is listening..")
ServerSideSocket.listen(20)


def multi_threaded_client(connection):
    credentials = pika.PlainCredentials("avani", "avani")
    while True:
        data = connection.recv(10)
        if not data:
            break
        try:
            rabbit_connection = pika.BlockingConnection(
                pika.ConnectionParameters("192.168.1.6", 5672, "/", credentials)
            )
            channel = rabbit_connection.channel()
            channel.queue_declare(queue="0201")
            channel.basic_publish(exchange="", routing_key="0201", body=data)
            print(" [x] Data sent: ")
            # connection.close()
        except:
            # save file
            print("Error: Connect to RabbitMQ failed !!!")
            file = open("data-test.txt", "a")
            data_save = (
                time.strftime("%H:%M:%S", time.localtime())
                + " -- "
                + str(data.decode("utf-8"))  #
            )

            print(data_save)
            file.write(data_save)

            # Close file
            # file.close()
            # print(data_save)


while True:
    try:
        while True:
            Client, address = ServerSideSocket.accept()
            _thread.start_new_thread(multi_threaded_client, (Client,))
    except KeyboardInterrupt:
        ServerSideSocket.close()
