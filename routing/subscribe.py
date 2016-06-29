from amqp.amqp import *
import sys

q_type = "CONSUMER"
exchange = "routing_demo"
ex_type = "direct"
# queue - routing_key pairs
dic = {"ERROR":"errors", "DEBUG": "debugs", "INFO": "infos"}

conn = ConnectionManager(q_type, exchange, ex_type)
conn.get_connection()
conn.init_queue(dic)
print(" [*] Waiting for Messages. To exit press CTRL+C")

def worker(ch, method, properties, body):
    print body

conn.consume("ERROR", worker)
