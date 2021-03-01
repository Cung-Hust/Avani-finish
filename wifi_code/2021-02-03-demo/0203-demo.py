from datetime import datetime
import socket
import os
import pika
import _thread
import time

# os.system('fuser -k 1234/tcp')
ServerSideSocket = socket.socket()
host = '192.168.1.10'
port = 1234
ThreadCount = 0

credentials = pika.PlainCredentials('avani', 'avani')

try:
    ServerSideSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Socket is listening..')
ServerSideSocket.listen(20)


def process_data(connection):
    while True:
        data = connection.recv(38).decode()  # type of data:bytes
        err_data = time.strftime("%H:%M:%S", time.localtime()) + data
        if not data:
            break
        try:
            credentials = pika.PlainCredentials("avani", "avani")
            Connected = pika.BlockingConnection(
                pika.ConnectionParameters(
                    "192.168.1.10",
                    5672,
                    "/",
                    credentials,
                    heartbeat_interval=1,
                    blocked_connection_timeout=10,
                )
            )
            channel = Connected.channel()
            channel.queue_declare(queue="data")
            channel.basic_publish(exchange="", routing_key="data", body=data)
            print("Processing ok: ", data)

        except:
            print("Error: Connect to RabbitMQ failed !!!")
            file = open("data-test.txt", "a")
            # err_data = time.strftime("%H:%M:%S", time.localtime()) + data
            print(err_data)
            file.write(err_data)


def scan_data(f):
    # f = open("data-test.txt", "r")
    credentials = pika.PlainCredentials("avani", "avani")
    rabbit_connection = pika.BlockingConnection(
        pika.ConnectionParameters("192.168.1.10", 5672, "/", credentials)
    )
    channel = rabbit_connection.channel()

    event.wait(60)

    while True:
        err_data = f.readline()
        if err_data != "":
            # print("Data: ", err_data)
            try:
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
        # scan_data(f)
finally:
    ServerSideSocket.close()