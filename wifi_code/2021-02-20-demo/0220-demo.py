# import socket programming library 
import socket  
from _thread import *
import threading 
import pika
import time

print_lock = threading.Lock() 

# initial connect rabbit
connection = None
def check_connect():
	credentials = pika.PlainCredentials('avani', 'avani')
	global connection
	if connection != None:
		if connection.is_open:
			return connection
	try:	
		connection = pika.BlockingConnection(
			pika.ConnectionParameters(
				"192.168.1.3",
				5672,
				"/",
				credentials,
				heartbeat=0,
				blocked_connection_timeout=1,
			)
		)
				
		channel_1 = connection.channel()
		channel_2 = connection.channel()

		channel_1.queue_declare(queue='data')
		channel_2.queue_declare(queue='err-data')

		return connection, channel_1, channel_2
	except:
		return None

# initial write data to file
# file = open("data-test.txt", "a")
# if file == None:
# 	print("error")
# file.write("hello")

# thread function 
def threaded(c, addr):
	file = open("data-test.txt", "a")
	global connection
	while True: 

		# data received from client 
		tcp_data = c.recv(1024)
		error_data = time.strftime("%H:%M:%S", time.localtime()) + tcp_data.decode('ascii')
		if not tcp_data: 
			print('Not data from ', addr) 
			
			# lock released on exit 
			print_lock.release()
			break

		print(error_data)
		connection = check_connect()
		if connection == None:
			print("Connect failed !!!")
			print(error_data)
			file.write(error_data)

			# file.write("hello Cung")
			# file.close()
		else:
			if connection.is_open:
				print("Connect rabbit OK")
				channel_1.basic_publish(exchange='', routing_key='data', body=tcp_data)
			else:
				print("open fail")
	# connection closed 
	c.close() 



# handle error data





def Main():
	global file
	host = "192.168.1.3"
	port = 1234
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	s.bind((host, port)) 
	print("socket binded to port", port) 

	# put the socket into listening mode 
	s.listen(24) 
	print("socket is listening") 
	# a forever loop until client wants to exit 
	while True: 

		# establish connection with client 
		c, addr = s.accept() 

		# lock acquired by client 
		# print_lock.acquire()
		print('Connected to :', addr[0], ':', addr[1]) 

		# Start a new thread and return its identifier 
		start_new_thread(threaded, (c,addr[0])) 
	s.close()
	file.close()


if __name__ == '__main__':
	Main() 
