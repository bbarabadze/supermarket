from fastapi import FastAPI, HTTPException
import uvicorn
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

app = FastAPI(title="Check Order")


@app.get("/orders/{order_id}", tags=["GET Methods"])
async def get_artist(order_id: str) -> dict:

    status = redis_client.get(order_id)

    if status is None:
        status = "Failed"
    elif status == '0':
        status = "Pending"
    elif status == '1':
        status = "Success"
    else:
        ... #TODO
        #raise HTTPException()

    return {"order_id": order_id, "status": status}


if __name__ == '__main__':
    uvicorn.run('api_redis_get:app', host="::1", port=8002, reload=True)