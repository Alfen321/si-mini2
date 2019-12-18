import pika
import time
import json

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', credentials=pika.PlainCredentials('root','myPassword')))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)
    
def add_car(body):
    tmp = json.loads(body)
    with open('../data/cars.json', 'r') as f:
        content = ''.join(f.readlines())
    
    cars = json.loads(content)
    cars.append(tmp)

    with open('../data/cars.json', 'w') as f:
        f.writelines(json.dumps(cars))

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    add_car(body.decode('UTF-8'))
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)

channel.start_consuming()