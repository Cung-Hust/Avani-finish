import pika
import time


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='err-data')

a_file = open('data-test.txt', 'r')
Lines = a_file.readlines()
a_file.close()
 
count = 0
# Strips the newline character
try:
    new_file = open("data-test.txt", "w")
    for line in Lines:
        if line != "\n":
            count += 1    
            channel.basic_publish(exchange='', routing_key='err-data', body=line)
            print("Line{}: {}".format(count, line.strip()))
            if line.strip("\n") != line:
            # Delete "line2" from new_file
                new_file.write(line)
except:
    connection.close()