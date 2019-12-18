import pika
import sys
import time


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', credentials=pika.PlainCredentials('root','myPassword')))
channel = connection.channel()

channel.exchange_declare(exchange='time', exchange_type='fanout')


while(True):
    # time.sleep(1)
    # localtime = time.localtime()
    # message = time.strftime("%I:%M:%S %p", localtime)
    message = input('> ')
    channel.basic_publish(exchange='time', routing_key='', body=message)
    print(" [x] Sent %r" % message)

connection.close()