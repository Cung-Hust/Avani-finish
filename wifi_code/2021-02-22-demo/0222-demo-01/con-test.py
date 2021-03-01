import socket
import os
import pika
import _thread
import time
from datetime import datetime

credentials = pika.PlainCredentials('avani', 'avani')

def initial_rb_connect():
    try:
        rb_connnection = pika.BlockingConnection(
            pika.ConnectionParameters(
                "192.168.0.3",
                5672,
                "/",
                credentials,
                heartbeat=0,
                socket_timeout= 1,
            )
        )
        return rb_connnection
    except:
        return False

try:
    while True:
        con = initial_rb_connect()
        if con == False:
            print("Connect error")
        else:
            print("Connect OK ")
except KeyboardInterrupt:
    print("Fail")
    pass