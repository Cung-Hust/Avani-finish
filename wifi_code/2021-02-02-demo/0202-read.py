import pika
import sys


def scan_data():
    f = open("data-test.txt", "r")
    credentials = pika.PlainCredentials("avani", "avani")
    while True:
        err_data = f.readline()
        if err_data != "":
            print("Data: ", err_data)
            try:
                rabbit_connection = pika.BlockingConnection(
                    pika.ConnectionParameters("192.168.1.8", 5672, "/", credentials)
                )
                channel = rabbit_connection.channel()
                channel.queue_declare(queue="err_data")
                channel.basic_publish(
                    exchange="", routing_key="err_data", body=err_data
                )
                print(" [x] Data sent: ", err_data)
            except:
                print("Error!!!")
                pass


try:
    while True:
        scan_data()
finally:
    print("Fail!!!")