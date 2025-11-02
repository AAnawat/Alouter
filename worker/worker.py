import pika
import os
import datetime

from config.rabbitConfig import config as rabbit_config
from database import router_db
from bson import json_util
from ansible import get_interface, get_performance, get_log


interface_collection = router_db["interface"]
performance_collection = router_db["performance"]
log_collection = router_db["log"]


def handle_interface(ch, method, properties, body):
    message = json_util.loads(body)

    interfaces = get_interface(
        message["host"],
        message["username"],
        message["password"],
        message["name"],
    )

    current = datetime.datetime.now(datetime.timezone.utc).isoformat()
    performance_collection.insert_one(
        {"router_ip": message["host"], "timestamp": current, "interfaces": interfaces}
    )


def handle_performance(ch, method, properties, body):
    message = json_util.loads(body)

    performance = get_performance(
        message["host"],
        message["username"],
        message["password"],
        message["name"],
    )

    current = datetime.datetime.now(datetime.timezone.utc).isoformat()
    performance_collection.insert_one(
        {"router_ip": message["host"], "timestamp": current, "performance": performance}
    )


def handle_log(ch, method, properties, body):
    message = {
        "host": "10.2.17.21",
        "username": "admin",
        "password": "cisco",
        "name": "Router1",
    }

    log_file = get_log(
        message["host"],
        message["username"],
        message["password"],
        message["name"],
    )

    if log_file != "":
        current = datetime.datetime.now(datetime.timezone.utc).isoformat()
        log_collection.insert_one(
            {"router_ip": message["host"], "timestamp": current, "log": log_file}
        )


def worker():
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=rabbit_config["host"],
                credentials=pika.PlainCredentials(
                    rabbit_config["username"], rabbit_config["password"]
                ),
            )
        )
        channel = connection.channel()

        channel.queue_declare(queue="interface_queue", durable=True)
        channel.queue_declare(queue="performance_queue", durable=True)
        channel.queue_declare(queue="log_queue", durable=True)

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(
            queue="interface_queue", on_message_callback=handle_interface, auto_ack=True
        )
        channel.basic_consume(
            queue="performance_queue",
            on_message_callback=handle_performance,
            auto_ack=True,
        )
        channel.basic_consume(
            queue="log_queue", on_message_callback=handle_log, auto_ack=True
        )

        channel.start_consuming()
        print(" [*] Waiting for messages. To exit press CTRL+C")

    except KeyboardInterrupt:
        print(" [*] Stopping worker...")
    except Exception as e:
        print(f" [!] An error occurred: {e}")


if __name__ == "__main__":
    worker()
