import pika
import os
import sys
import logging

class ConnectionManager:
    def __init__(self, q_type, exchange, ex_type):
        self.q_type = q_type
        self.ex_type = ex_type
        self.exchange = exchange
        self.connection = None
        self.channel = None
        if q_type == "PRODUCER":
            self.port = int(os.environ.get('RABBITMQ_PRODUCERS_PORT'))
        else:
            self.port = int(os.environ.get('RABBITMQ_CONSUMERS_PORT'))

    def get_connection(self):
        while not self.connection:
            try:
                self.connection = pika.BlockingConnection(
                    pika.ConnectionParameters(
                        host = os.environ.get('RABBITMQ_HOST'),
                        virtual_host = os.environ.get('RABBITMQ_VIRTUAL_HOST'),
                        credentials = pika.PlainCredentials(os.environ.get('RABBITMQ_USER'), os.environ.get('RABBITMQ_PASSWORD')),
                        port = self.port)
                )
            except Exception as e:
                logging.debug(e)

    def get_channel(self):
        if not self.channel:
            self.get_connection()
        chan = self.connection.channel()
        return chan

    def init_queue(self, d):
    # declare exchange and queues
    # binding exchange and queues based on queue-routing_key pairs in d
        chan = self.get_channel()
        chan.exchange_declare(exchange = self.exchange,
                              type = self.ex_type,
                              durable = False,
                              auto_delete = True)

        queues = d.keys()
        for queue in queues:
            chan.queue_declare(queue=queue,
                               durable =False,
                               auto_delete = True)

        for q, key in d.items():
            chan.queue_bind(routing_key=key,
                            queue = q,
                            exchange = self.exchange)

    def publish(self, exchange, routing_key, body):
        chan = self.get_channel()
        chan.basic_publish(exchange=exchange,
                           routing_key=routing_key,
                           body=body)

    def consume(self, queue, worker):
        chan = self.get_channel()
        chan.basic_consume(worker,
                           queue = queue)
        chan.start_consuming()
