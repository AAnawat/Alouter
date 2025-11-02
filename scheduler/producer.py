import pika

from config.rabbitConfig import config as rabbit_config


connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=rabbit_config["host"],
        credentials=pika.PlainCredentials(
            username=rabbit_config["username"], password=rabbit_config["password"]
        ),
    )
)
channel = connection.channel()

channel.queue_declare(queue="interface_queue", durable=True)
channel.queue_declare(queue="performance_queue", durable=True)
channel.queue_declare(queue="log_queue", durable=True)
