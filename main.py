from fastapi import FastAPI, HTTPException, BackgroundTasks
import uvicorn
from models import Order, OrderStatus
from pprint import pprint
from uuid import uuid4
import json
from confluent_kafka import Producer
import redis


redis_host = "127.0.0.1"
redis_port = 6379
redis_db_number = 0

redis_client = redis.Redis(
    host=redis_host,
    port=redis_port,
    db=redis_db_number,
    decode_responses=True,
)


def delivery_report(err, msg):
    if err is not None:
        # TODO: Something happened on a Kafka side, please investigate
        # TODO: Get detailed error, log it, get message which was not delivered, write it to temp storage
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to topic: {msg.topic()} offset:[{msg.offset()}]')


producer_conf = {
    'bootstrap.servers': '[::1]:9092',
}

producer = Producer(producer_conf)


app = FastAPI(title="Markets Data")


def produce_to_kafka(topic_name, order, order_id):
    try:
        producer.produce(topic_name, value=order)
        redis_client.set(name=order_id, value='0', ex=30)
    except Exception as ex:
        print(str(ex))
        raise HTTPException(status_code=500, detail="Something went wrong, try again")
    finally:
        producer.flush()  # Wait for any outstanding messages to be delivered


@app.post("/orders", response_model=OrderStatus, tags=["POST Methods"])
async def process_order(order: Order, background_tasks: BackgroundTasks):

    order = order.model_dump()

    topic_name = order["user_location"]
    order_id = str(uuid4())
    check_status = f"http://[::1]:8002/orders/{order_id}"
    status = "Accepted, Wait for further processing"

    order["order_id"] = order_id

    order = json.dumps(order)

    background_tasks.add_task(produce_to_kafka, topic_name, order, order_id)


    return {
        "order_id": order_id,
        "status": status,
        "check_status": check_status
    }


if __name__ == '__main__':
    uvicorn.run('main:app', host="::1", port=8001, reload=True)

