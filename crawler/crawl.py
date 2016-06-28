import pika
from bs4 import BeautifulSoup
import httplib2
import os
from amqp.amqp import *

conn = ConnectionManager('CONSUMER', 'crawler')
conn.get_connection()
conn.init_queue()
chan = conn.get_channel()

# consume the url messages and crawl
def crawl(ch, method, properties, body):
    d = {}
    print(d["a"])
    print(" [*] URL to consume: %r"% body)
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = { 'User-Agent' : user_agent }
    http = httplib2.Http()

    status, response = http.request(body, 'GET', None, headers)
    soup = BeautifulSoup(response)
    investors = {}
    company = body.split('/')[-1]
    for a in soup.find_all("a", {"class":"startup-link"}):
        name = a.get_text()
        if name != "":
            investors[name] = a.get('href')
    c = {"name":company, "investors":investors}
    print(" [*] result: " + str(c) + "\n")

chan.basic_consume(crawl,
                   queue='crawler'
                   )

print(" [*] Waiting for URL to crawl. To exit press CTRL+C")
chan.start_consuming()
