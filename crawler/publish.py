import pika
import os
import sys

host = os.environ.get('RABBITMQ_HOST')
port = int(os.environ.get('RABBITMQ_PRODUCERS_PORT'))
credentials = pika.PlainCredentials(os.environ.get('RABBITMQ_USER'), os.environ.get('RABBITMQ_PASSWORD'))
virtual_host = os.environ.get('RABBITMQ_VIRTUAL_HOST')

connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port,virtual_host=virtual_host, credentials=credentials))
channel = connection.channel()
channel.queue_declare(queue='crawler')
BASE_URL = 'https://angel.co/'

names = []
with open('names.txt') as fp:
    for line in fp:
        names.append(line.split('. ')[1][:-1])

if __name__ == "__main__":
    for name in names:
        url = BASE_URL + name
        channel.basic_publish(exchange='', routing_key='crawler', body=url)
        print("url: %r sent to task queue" % url)
    connection.close()
