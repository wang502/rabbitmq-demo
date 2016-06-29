from amqp.amqp import *
import sys

q_type = "PRODUCER"
exchange = "routing_demo"
ex_type = "direct"
# queue - routing_key pairs
dic = {"ERROR":"errors", "DEBUG": "debugs", "INFO": "infos"}

conn = ConnectionManager(q_type, exchange, ex_type)
conn.get_connection()
conn.init_queue(dic)

routing_key = sys.argv[1]
message = sys.argv[2]
conn.publish(exchange, routing_key, message)
