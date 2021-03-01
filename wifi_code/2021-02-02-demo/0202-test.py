import socket
import os
import pika
import _thread
import time
from datetime import datetime

# os.system('fuser -k 1234/tcp')
ServerSideSocket = socket.socket()
host = "192.168.0.2"
port = 1234
ThreadCount = 0

credentials = pika.PlainCredentials("avani", "avani")

try:
    ServerSideSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print("Socket is listening..")
ServerSideSocket.listen(20)


def process_data(connection):
    while True:
        data = connection.recv(37).decode()  # type of data:bytes
        # print(type(data))
        if not data:
            break
        # print(data)
        try:
            Connected = pika.BlockingConnection(
                pika.ConnectionParameters("192.168.1.3", 5672, "/", credentials)
            )
            channel = Connected.channel()
            channel.queue_declare(queue="data")
            channel.basic_publish(exchange="", routing_key="data", body=data)
        except:
            print("Error: Connect to RabbitMQ failed !!!")
            file = open("data-test.txt", "a")
            err_data = time.strftime("%H:%M:%S", time.localtime()) + data
            print(err_data)
            file.write(err_data)


def scan_data(f):
    # f = open("data-test.txt", "r")
    # credentials = pika.PlainCredentials("avani", "avani")
    while True:
        err_data = f.readline()
        if err_data != "":
            print("Data: ", err_data)
            try:
                rabbit_connection = pika.BlockingConnection(
                    pika.ConnectionParameters("192.168.0.2", 5672, "/", credentials)
                )
                channel = rabbit_connection.channel()
                channel.queue_declare(queue="err_data")
                channel.basic_publish(
                    exchange="", routing_key="err_data", body=err_data
                )
                print(" [x] Data sent: ", err_data)
            except:
                pass


try:
    while True:
        Client, address = ServerSideSocket.accept()
        f = open("data-test.txt", "r")
        _thread.start_new_thread(process_data, (Client,))
        _thread.start_new_thread(scan_data, (f,))
finally:
    ServerSideSocket.close()