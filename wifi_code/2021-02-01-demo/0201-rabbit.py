import sys
import pika

credentials = pika.PlainCredentials(username="avani", password="avani")
parameters = pika.ConnectionParameters(
    host="192.168.0.5", port=5672, virtual_host="/", credentials=credentials
)

connection = pika.BlockingConnection(parameters=parameters)
channel = connection.channel()

channel.queue_declare(queue="hello")

channel.basic_publish(exchange="", routing_key="hello", body="hello")
print("Sent!")
connection.close()