#!/usr/bin/env python
import pika

credentials = pika.PlainCredentials("avani", "avani")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
		"192.168.1.10",
		5672,
		"/",
		credentials,
		heartbeat=10,
		blocked_connection_timeout=10,
	))
channel = connection.channel()

channel.queue_declare(queue='hello')

channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()