import socket
import os
import pika
import _thread
import time
from datetime import datetime
import threading


event = threading.Event()


def scan_data(f):
    event.wait(6)

    while True:
        err_data = f.readline()
        if err_data != "":
            try:
                print(err_data)
            except:
                pass


try:
    while True:
        f = open("data-test.txt", "r")
        scan_data(f)
finally:
    pass