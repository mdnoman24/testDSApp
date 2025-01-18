import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks
from redis_om import get_redis_connection,HashModel
from starlette.requests import Request
import requests

app = FastAPI(debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://127.0.0.1:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)

redis=get_redis_connection(
    host='redis-10857.c328.europe-west3-1.gce.redns.redis-cloud.com',
    port=10857,
    password='Noman@1538',
    decode_responses=True
)


class Order(HashModel):
    id: str
    price: float
    quantity: int  
    fee : float
    total : float
    status : str  # pending, paid, failed

    class Meta:
        database = redis

@app.get("/orders/{pk}")
def get_order(pk: str):
    order = Order.get(pk)
    redis.xadd('refund_order', order.dict(), '*')
    return order
@app.get("/orders")
def all_orders():
    return [Order.get(pk) for pk in Order.all_pks()]

@app.post('/orders')
async def create_order(request: Request, background_task: BackgroundTasks): #id,quantity

    body = await request.json()

    req = requests.get('http://127.0.0.1:8000/products/%s' % body['id'])
    product = req.json()
    order = Order(
        id=body['id'],
        price=product['price'],
        quantity=body['quantity'],
        fee=0.1 * product['price'],
        total=product['price']*body['quantity']*1.1,
        status='pending'
    )
    order.save()
    background_task.add_task(order_completed, order)
    return order

def order_completed(order: Order):
    time.sleep(5)
    order.status = 'paid'
    order.save()
    redis.xadd('order_completed', order.dict(),'*')
