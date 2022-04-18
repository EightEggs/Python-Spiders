import pika

MAX_PRIORITY = 100
TOTAL = 10
QUEUE_NAME = 'scrape_queue'

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue=QUEUE_NAME, durable=True, arguments={
                      'x-max-priority': MAX_PRIORITY})

for i in range(1, TOTAL + 1):
    url = f'https://ssr1.scrape.center/detail/{i}'
    channel.basic_publish(exchange='', routing_key=QUEUE_NAME,
                          properties=pika.BasicProperties(delivery_mode=2), body=url)
    print(f'Put Request: {url}')
