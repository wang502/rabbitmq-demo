import pika
import os
import urlparse

host = os.environ.get('RABBITMQ_HOST')
port = int(os.environ.get('RABBITMQ_PRODUCERS_PORT'))
credentials = pika.PlainCredentials(os.environ.get('RABBITMQ_USER'), os.environ.get('RABBITMQ_PASSWORD'))
virtual_host = os.environ.get('RABBITMQ_VIRTUAL_HOST')
connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port,virtual_host=virtual_host, credentials=credentials))
channel = connection.channel()
channel.queue_declare(queue='hello')
channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')

print(" [X] Sent 'Hello World!'")
connection.close()
