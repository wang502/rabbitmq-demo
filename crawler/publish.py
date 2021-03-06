# author: Seth Wang
# email: sethwang199418@gmail.com
# Part of RabbitMQ-Demo project
# /crawler/publish.py
# Publish list of urls to message broker
################################################

import pika
import os
import sys
from amqp.amqp import *

# set up connection and channel to RabbitMQ server
conn = ConnectionManager('PRODUCER', 'crawler')
conn.get_connection()
conn.init_queue()
chan = conn.get_channel()

BASE_URL = 'https://angel.co/'

names = []
with open('names.txt') as fp:
    for line in fp:
        names.append(line.split('. ')[1][:-1])

for name in names:
    url = BASE_URL + name
    chan.basic_publish(exchange='', routing_key=conn.queue, body=url, properties=pika.BasicProperties(
                         delivery_mode = 2, # make message persistent
                      ))
    print("url: %r sent to task queue" % url)
chan.close()
