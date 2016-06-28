import pika
import os
import sys

# type denotes whether it is producer or consumer queue
class ConnectionManager:
    def __init__(self, q_type, queue):
        self.connection = None
        self.channel = None
        self.queue = queue
        self.q_type = q_type
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
                        port = self.port
                    )
                 )
            except Exception as e:
                print("Error connecting to %s %d port" %(self.host, self.port))

            return self.connection

    def close_connection(self):
        self.connection.close()

    def get_channel(self):
        if not self.connection:
            self.connection = None
            self.channel = None
            self.get_connection()

        if not self.channel:
            self.channel = self.connection.channel()
        return self.channel

    def init_queue(self):
        chan = self.get_channel()
        chan.queue_declare(queue=self.queue,durable=True)
