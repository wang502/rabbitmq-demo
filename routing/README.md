### Routing in RabbitMQ Message Broker

#### What is routing
- A routing key is a binding key between a exchange and a message queue
- The purpose of setting up routing key is to let worker make option to consume from a specific queue. Since we can have many queues at the same time, if we want to consume a specific queue, we do basic consume with the routing key binding to that queue.

#### What is routing_key
A routing_key is a relation between a specific exchange and a queue.

#### Code
In the ```amqp.py```, when in the ```init_queue()``` method, is declares exchanges, queues, and then bind the exchanges with queues, using
```python
chan.queue_bind(routing_key=key,
                queue = q,
                exchange = self.exchange)
```
In this example, the binding relationship is:
```
excahnge       |  routing_key | queue name  
binding_demo   |  ERROR       | errors
binding_demo   |  DEBUG       | debugs
binding_demo   |  INFO        | infos
```
therefore,
- when we publish a message to the broker, we give it exchange as well as routing_key, so the message will be added to the queue that is binded with the given exchange.
```python
chan.basic_publish(exchange=exchange,
                   routing_key=routing_key,
                   body=body)
```

- when we consume a message from the broker, we provide the queue name and the worker
```python
chan.basic_consume(worker,
                   queue = queue)
```
