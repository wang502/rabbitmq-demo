import pika
import os
from amqp import *
import json

conn = ConnectionManager("PRODUCER", "hello")
conn.get_connection()
conn.init_queue()
chan = conn.get_channel()
chan.basic_publish(exchange='',
                   routing_key="hello",
                   body=json.dumps({"word":"hello world!"})
                   )
chan.close()

print(" [X] Sent 'Hello World!'")
