import socket
import os
import pika
import _thread
import time

# os.system('fuser -k 1234/tcp')

ServerSideSocket = socket.socket()
host = "192.168.0.2"
port = 1234
ThreadCount = 0

try:
    ServerSideSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print("Socket is listening..")
ServerSideSocket.listen(20)

# --- Task 1: data processing ---
# -------------------------------


def process_data(connection):
    credentials = pika.PlainCredentials("avani", "avani")
    while True:
        data = connection.recv(38)
        if not data:
            break
        try:
            rabbit_connection = pika.BlockingConnection(
                pika.ConnectionParameters("192.168.1.3", 5672, "/", credentials)
            )
            channel = rabbit_connection.channel()
            channel.queue_declare(queue="data")
            channel.basic_publish(exchange="", routing_key="data", body=data)
            print(" [x] Data sent: ")
            # connection.close()
        except:
            # save file
            print("Error: Connect to RabbitMQ failed !!!")
            file = open("data-test.txt", "a")
            data_save = (
                time.strftime("%H:%M:%S", time.localtime())
                + " -- "
                + str(data)  # .decode("utf-8")
            )
            file.write(data_save)

            # Close file
            # file.close()
            print(data)
            # print("-------------------------------")
            # print(data_save)
            # print("\n\n")


# --- Task 1: data scanning ---
# -----------------------------


def scan_data(f):
    # f = open("data-test.txt", "r")
    credentials = pika.PlainCredentials("avani", "avani")
    while True:
        err_data = f.readline()
        if err_data != "":
            # print("Data: ", err_data)
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


while True:
    try:
        while True:
            Client, address = ServerSideSocket.accept()
            _thread.start_new_thread(process_data, (Client,))
            f = open("data-test.txt", "r")
            _thread.start_new_thread(scan_data, (f,))
    except KeyboardInterrupt:
        ServerSideSocket.close()
