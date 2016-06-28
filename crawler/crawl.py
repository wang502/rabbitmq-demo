import pika
from bs4 import BeautifulSoup
import httplib2
import os

host = os.environ.get('RABBITMQ_HOST')
port = int(os.environ.get('RABBITMQ_CONSUMERS_PORT'))
credentials = pika.PlainCredentials(os.environ.get('RABBITMQ_USER'), os.environ.get('RABBITMQ_PASSWORD'))
virtual_host = os.environ.get('RABBITMQ_VIRTUAL_HOST')

connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port,virtual_host=virtual_host, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='crawler')

# consume the url messages and crawl
def crawl(ch, method, properties, body):
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

channel.basic_consume(crawl,
                   queue='crawler',
                   no_ack=True)

print(" [*] Waiting for URL to crawl. To exit press CTRL+C")
channel.start_consuming()
