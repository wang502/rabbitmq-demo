import pika
import os

host = os.environ.get('RABBITMQ_HOST')
port = int(os.environ.get('RABBITMQ_CONSUMERS_PORT'))
credentials = pika.PlainCredentials(os.environ.get('RABBITMQ_USER'), os.environ.get('RABBITMQ_PASSWORD'))
virtual_host = os.environ.get('RABBITMQ_VIRTUAL_HOST')

connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port,virtual_host=virtual_host, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='hello')

def callback(ch, method, properties, body):
    print(" [X] Received %r" % body)

channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True)

print(" [*] Waiting for messages. To exit press CTRL+C")
channel.start_consuming()
