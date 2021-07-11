import pika,requests,jsonify

params = pika.URLParameters('amqps://kzevgcua:bCcYfIw0tFS3Zq4Fso_qo7_AvQ6dlQNP@rat.rmq2.cloudamqp.com/kzevgcua')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='calculate_order_service')

def callback(ch,method,properties,body):
    print(int(body))
    req = requests.get(f'http://docker.for.mac.localhost:5001/exec_price/{int(body)}')

channel.basic_consume(queue='calculate_order_service',on_message_callback=callback,auto_ack=True)

print("started consuming")

channel.start_consuming()
channel.close()