### Task Queue for Crawler

#### About
The publisher reads in an array of names and publish to RabbitMQ. Then the subscriber(crawl.py in this case) consumes the task queue and parse the targeted url

#### Benifit of using task queue
- For heavy computing task like crawl web pages, using task queue like RabbitMQ to achieve pub/sub can reduce the pressure of the machine.
- When the workers are deployed in several machines, it can reduce the job latencies. Since the pub/sub is asynchronous, each action will not affect each other.

#### To Run
- Firstly, type ```python publish.py```. This will publish an array of urls to the job queue.
- Then do ```python crawl.py``` to consume all urls and crawl the web pages. You will see the content being printed.
- To add more workers, open a new terminal and do ```python crawl.py```. You will see each worker do their jobs individually.

#### Difference between with ```no_ack=True``` and without
```python
chan.basic_consume(crawl,
                   queue='crawler'
                   )
```
Enables acknowledgement, so when the worker fails, the data in the queue is not lost. Since the data will be deleted only when it receives acknowledgement back from the worker, which tells the queue that the job has been done

```python
chan.basic_consume(crawl,
                   queue='crawler'
                   no_ack=True)
```
Disables acknowledgement, so when the worker fails on the first data, the data will be lost.
