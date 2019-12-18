import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', credentials=pika.PlainCredentials('root','myPassword')))
channel = connection.channel()

channel.exchange_declare(exchange=sys.argv[1], exchange_type='fanout')

result = channel.queue_declare(queue=sys.argv[1], exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='time', queue=queue_name)

def callback(ch, method, properties, body):
    print(" [x] %r" % body)

channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()

print('nope')