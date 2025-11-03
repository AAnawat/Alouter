import time

from bson import json_util
from database import router_db
from producer import connection, channel


credential_collection = router_db["credential"]


def scheduler():
    try:

        INTERVAL = 30
        next_run = time.monotonic()
        count = 0

        while True:
            now = time.time()
            now_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now))
            ms = int((now % 1) * 1000)
            now_str_with_ms = f"{now_str}.{ms:03d}"
            print(f"[{now_str_with_ms}] run #{count}")

            router_credentials = credential_collection.find({})
            for cred in router_credentials:
                body = json_util.dumps(cred).encode("utf-8")

                channel.basic_publish(
                    exchange="", routing_key="interface_queue", body=body
                )

                channel.basic_publish(
                    exchange="", routing_key="performance_queue", body=body
                )

                if count % 4 == 0:
                    channel.basic_publish(
                        exchange="", routing_key="log_queue", body=body
                    )

            count += 1
            next_run += INTERVAL
            time.sleep(max(0.0, next_run - time.monotonic()))

    except KeyboardInterrupt:
        print("Scheduler stopped by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        connection.close()


if __name__ == "__main__":
    scheduler()
