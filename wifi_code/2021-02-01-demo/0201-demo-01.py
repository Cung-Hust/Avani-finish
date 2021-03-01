import _thread
import time
import pika


def multi_threaded_client():
    credentials = pika.PlainCredentials("avani", "avani")
    data = "00001--00--001--002:...->\n"

    # send to rabbitmq
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters("192.168.1.3", 5672, "/", credentials)
        )
        channel = connection.channel()

        channel.queue_declare(queue="0201")
        channel.basic_publish(exchange="", routing_key="0201", body=data)
        print(" [x] Sent: ", data)
        connection.close()
    except:
        # save file
        print("Error: Connect to RabbitMQ failed !!!")
        file = open("data-test.txt", "a")
        file.write(data)
        # Close file
        # file.close()
        # print(data)

    time.sleep(1)


while True:
    # try:
    multi_threaded_client()
    # except:
    # print("Error!!!")
