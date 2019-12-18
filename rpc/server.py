import pika
import json


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', credentials=pika.PlainCredentials('root','myPassword')))

channel = connection.channel()

channel.queue_declare(queue='json')
channel.queue_declare(queue='csv')

def find_in_json(body):
    tmp = json.loads(body)
    rtn = []
    with open('../data/cars.json', 'r') as f:
        content = ''.join(f.readlines())
        cars = json.loads(content)
        for each in cars:
            if 'model' in tmp.keys() and 'brand' in tmp.keys():
                if each.get('brand') == tmp.get('brand') and each.get('model') == tmp.get('model'):
                    rtn.append(each)
            if 'brand' in tmp.keys() and 'model' not in tmp.keys():
                if each.get('brand') == tmp.get('brand'):
                    rtn.append(each)
            if 'brand' not in tmp.keys() and 'model' in tmp.keys():
                if each.get('model') == tmp.get('model'):
                    rtn.append(each)
    return json.dumps(rtn)

def on_json_request(ch, method, props, body):
    b = body.decode('UTF-8')
    print(" [.] find_in_json(%s)" % b)
    response = find_in_json(b)
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

def find_in_csv(body):
    tmp = json.loads(body)
    rtn = ""
    with open('../data/cars.csv', 'r') as f:
        content = ''.join(f.readlines())
        first = True
        for each in content.split('\n'):
            if first:
                rtn += each + '\n'
                first = False
                continue
            eList = each.split(',')
            if 'model' in tmp.keys() and 'brand' in tmp.keys():
                if eList[1] == tmp.get('brand') and eList[2] == tmp.get('model'):
                    rtn += each + '\n'
            if 'brand' in tmp.keys() and 'model' not in tmp.keys():
                if eList[1] == tmp.get('brand'):
                    rtn += each + '\n'
            if 'brand' not in tmp.keys() and 'model' in tmp.keys():
                if eList[2] == tmp.get('model'):
                    rtn += each + '\n'
    return rtn

def on_csv_request(ch, method, props, body):
    b = body.decode('UTF-8')
    print(" [.] find_in_csv(%s)" % b)
    response = find_in_csv(b)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)



channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='json', on_message_callback=on_json_request)
channel.basic_consume(queue='csv', on_message_callback=on_csv_request)

print(" [x] Awaiting RPC requests")
channel.start_consuming()