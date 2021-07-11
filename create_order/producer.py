import pika, json

params = pika.URLParameters('amqps://kzevgcua:bCcYfIw0tFS3Zq4Fso_qo7_AvQ6dlQNP@rat.rmq2.cloudamqp.com/kzevgcua')

connection = pika.BlockingConnection(params)

channel = connection.channel()


def publish(body):
    channel.basic_publish(exchange='', routing_key='calculate_order_service', body=body)