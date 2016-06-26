## Simple RabbitMQ task queue demo
### Setup
- install pika (RabbitMQ python client) ```pip install pika```
- setup a remote RabbitMQ server (for example, from Heroku)

### To Use
- Specify the ```host```, ```port```, ```credentials``` and ```virtual_host``` variables to make connection. [connection details](https://pika.readthedocs.io/en/0.9.6/connecting.html)
- ```python send.py``` send a message "Hello World!" to the RabbitMQ task queue
- ```python receive.py``` consume messages from the RabbitMQ and print the message "Hello World!"

### Change Tasks
The current task is to simply print the broker message "Hello World!", to change the task you want the worker to execute, change ```callback()``` function in ```receive.py```
