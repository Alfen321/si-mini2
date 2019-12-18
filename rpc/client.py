import pika
import uuid
import sys


class RpcClient(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host='localhost', credentials=pika.PlainCredentials('root','myPassword')))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key=sys.argv[1],
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return self.response.decode('UTF-8')


rpc = RpcClient()

print(f' [x] Requesting {sys.argv[1]}')
response = rpc.call("{\"brand\": \"Audi\"}")
print(response)