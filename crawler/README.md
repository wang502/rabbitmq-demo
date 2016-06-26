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
