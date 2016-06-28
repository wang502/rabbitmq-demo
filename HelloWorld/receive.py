import pika
import os
from amqp import *
import json

conn = ConnectionManager("CONSUMER", 'hello')
conn.get_connection()
conn.init_queue()
chan = conn.get_channel()

def callback(ch, method, properties, body):
    d = json.loads(body)
    print(" [X] Received %r" %(d.get("word")))

chan.basic_consume(callback,
                   queue='hello',
                  )

print(" [*] Waiting for messages. To exit press CTRL+C")
chan.start_consuming()
