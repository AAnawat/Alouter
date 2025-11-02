import pika
import time

from config.rabbitConfig import config as rabbit_config
print(rabbit_config)

for _ in range(10):
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=rabbit_config["host"],
                credentials=pika.PlainCredentials(
                    username=rabbit_config["username"],
                    password=rabbit_config["password"]
                )
            )
        )
        break
    except pika.exceptions.AMQPConnectionError:
        print("RabbitMQ not ready, retrying...")
        time.sleep(3)
channel = connection.channel()

channel.queue_declare(queue="interface_queue", durable=True)
channel.queue_declare(queue="performance_queue", durable=True)
channel.queue_declare(queue="log_queue", durable=True)
