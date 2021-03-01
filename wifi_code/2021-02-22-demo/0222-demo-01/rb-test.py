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

def initial_rb_connect(data):
    try:
        rb_connnection = pika.BlockingConnection(
            pika.ConnectionParameters(
                "192.168.1.4",
                5672,
                "/",
                credentials,
                heartbeat=0,
                blocked_connection_timeout=0,
            )
        )
        channel = rb_connnection.channel()
        channel.queue_declare(queue="data")
        channel.basic_publish(exchange="", routing_key="data", body=data)
        return rb_connnection
    except:
        return False

def try_rb_connect():
    try:
        rb_connnection = pika.BlockingConnection(
            pika.ConnectionParameters(
                "192.168.1.3",
                # "localhost",
                5672,
                "/",
                credentials,
                heartbeat_interval=0,
                blocked_connection_timeout=1,
            )
        )
        channel = rb_connnection.channel()
        channel.queue_declare(queue="err-data")
        return rb_connnection
    except:
        return False

def process_data(tcp_connnection):
    while True:
        data = tcp_connnection.recv(38).decode()
        err_data = time.strftime("%H:%M:%S", time.localtime()) + data
        file = open("data-test.txt", "a")
        if not data:
            break        
        print(data)
        
        rb_connected = initial_rb_connect(data)
        if rb_connected == False:
            print("Connect fail !")
            # file = open("data-test.txt", "a")
            print(err_data)
            file.write(err_data)
        else:            
            print("Connect OK, send : ", data)


def scan_data(f):
    rb_connected = try_rb_connect()
    if rb_connected == True:
        err_data = f.readline()
        channel.basic_publish(
            exchange="", routing_key="err_data", body=err_data
        )
        print(" [x] Data sent: ", err_data)


while True:
    try:
        while True:
            # Client, address = ServerSideSocket.accept()
            f = open("data-test.txt", "r")
            # _thread.start_new_thread(process_data, (Client, ))
            _thread.start_new_thread(scan_data, (f,))
            scan_data(f)
    finally:
        ServerSideSocket.close()