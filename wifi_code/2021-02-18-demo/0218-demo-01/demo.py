import socket
import os
import pika
import _thread
import time
from datetime import datetime

# os.system('fuser -k 1234/tcp')
ServerSideSocket = socket.socket()
host = '192.168.1.3'
port = 1234
ThreadCount = 0

credentials = pika.PlainCredentials('avani', 'avani')

try:
    ServerSideSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Socket is listening..')
ServerSideSocket.listen(20)

Connected = None
channel = None

def initial_connect():
    global Connected
    credentials = pika.PlainCredentials("avani", "avani")

    tryConnect = False
    if Connected == None:
        tryConnect = True
    else:
        if not (Connected.is_open == True):
            tryConnect = True

    if tryConnect:
        try:
            Connected = pika.BlockingConnection(
                pika.ConnectionParameters(
                    "192.168.1.13",
                    5672,
                    "/",
                    credentials,
                    heartbeat=10,
                    blocked_connection_timeout=10,
                )
            )
            return Connected
        except:
            return None
    else:
        return Connected

def process_data(connection):
    global channel
    while True:
        data = connection.recv(38).decode()  # type of data:bytes
        err_data = time.strftime("%H:%M:%S", time.localtime()) + data
        if not data:
            break
        
        Connected = initial_connect()
        if not (Connected == None): 
            # if channel == None:
            channel = Connected.channel()
            channel.queue_declare(queue="data")
            channel.basic_publish(exchange="", routing_key="data", body=data)
            print("Processing ok: ", data)
        else:
            print("Error: Connect to RabbitMQ failed !!!")
            file = open("data-test.txt", "a")
            # err_data = time.strftime("%H:%M:%S", time.localtime()) + data
            print(err_data)
            file.write(err_data)

def scan_data(f):
    # f = open("data-test.txt", "r")
    credentials = pika.PlainCredentials("avani", "avani")
    rabbit_connection = pika.BlockingConnection(
        pika.ConnectionParameters("192.168.1.3", 5672, "/", credentials)
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

while True:
    try:
        while True:
            Client, address = ServerSideSocket.accept()
            _thread.start_new_thread(process_data, (Client, ))
    finally:
        ServerSideSocket.close()