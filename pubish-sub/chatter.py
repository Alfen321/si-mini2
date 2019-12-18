import pika
import sys
import threading

connection2 = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', credentials=pika.PlainCredentials('root','myPassword')))
channel2 = connection2.channel()

channel2.exchange_declare(exchange=sys.argv[1], exchange_type='fanout')

def receive_command():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', credentials=pika.PlainCredentials('root','myPassword')))
    channel = connection.channel()

    channel.exchange_declare(exchange=sys.argv[1], exchange_type='fanout')

    result = channel.queue_declare(queue=sys.argv[2], auto_delete=True)
    channel.queue_bind(exchange=sys.argv[1], queue=sys.argv[2])

    def callback(ch, method, properties, body):
        print(" received: %r" % body.decode('UTF-8'))

    channel.basic_consume(
        queue=sys.argv[2], on_message_callback=callback, auto_ack=True)

    channel.start_consuming()


if __name__ == "__main__":
    t_msg = threading.Thread(target=receive_command)
    t_msg.start()
    t_msg.join(0)

    while(True):
        message = input('')
        channel2.basic_publish(exchange=sys.argv[1], routing_key='', body=sys.argv[2] + ': ' + message)