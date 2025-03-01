""" This file is used to connect to the Redis database. """
from redis_om import get_redis_connection

redis=get_redis_connection(
    host='redis-10857.c328.europe-west3-1.gce.redns.redis-cloud.com',
    port=10857,
    password='Noman@1538',
    decode_responses=True
)
