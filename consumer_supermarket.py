from confluent_kafka import Consumer, KafkaError
import json
import psycopg2
from pprint import pprint
import sys
import redis

connection = psycopg2.connect(
    user="postgres",
    password="admin",
    host="127.0.0.1",
    port="5432",
    database="supermarkets_project",

)

redis_host = "127.0.0.1"
redis_port = 6379
redis_db_number = 0

redis_client = redis.Redis(
    host=redis_host,
    port=redis_port,
    db=redis_db_number,
    decode_responses=True,
)


def consume_messages(topic_name: str):
    consumer_conf = {
        'bootstrap.servers': '[::1]:9092',
        'group.id': 'grup4',
        #'auto.offset.reset': 'earliest'  # Consumption begins from the start of partition
    }

    consumer = Consumer(consumer_conf)

    consumer.subscribe([topic_name])

    try:
        while True:

            msg = consumer.poll(1.0)

            if msg is None:
                continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(f"Error: {msg.error()}")
                    # TODO: Send notification to someone,

                    break

            # TODO: We have the data, let's do something with it
            process_message(msg.value().decode('utf-8'))

    except KeyboardInterrupt:
        # TODO: Handle gracefully non-consumed messages
        pass
    finally:
        consumer.close()

def process_message(message: str):
    message = json.loads(message)
    records = list(yield_records(message))
    notif_record = get_notif_record(message, "Success!!")

    insert_query = """
            INSERT INTO orders 
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    insert_notif_query = """
            INSERT INTO notifications 
            VALUES(%s, %s, %s, %s)
    """
    try:
        cursor = connection.cursor()
        cursor.executemany(insert_query, records)
        cursor.execute(insert_notif_query, notif_record)   
        connection.commit()
        try:
            redis_client.set(name=message["order_id"], value='1')
        except:
            ...
            # TODO delete queries (compensating)
    except:
        connection.rollback()

def get_notif_record(message, custom_notification):
    return (message["order_id"], 
    message["report"]["sms"], 
    message["report"]["email"],
    custom_notification)

def yield_records(message):

    upside = message["order_id"], message["store_name"], message["customer_id"], message["user_location"]
    bottom = message["total_price"], message["timestamp"]
    for item in message["items"]:
        yield upside + (item["category"], item["item_id"], item["name"], item["price"]) + bottom


if __name__ == "__main__":

    topic_name_from_args = sys.argv[1]

    create_partition_query = f"""
            CREATE TABLE IF NOT EXISTS orders_{topic_name_from_args.lower()}
            PARTITION OF orders
            FOR VALUES IN (%s);
    """

    cursor = connection.cursor()
    cursor.execute(create_partition_query, (topic_name_from_args,))

    connection.commit()


    consume_messages(topic_name_from_args)
    connection.close()