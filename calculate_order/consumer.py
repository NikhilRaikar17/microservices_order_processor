import pika, json

params = pika.URLParameters('amqps://kzevgcua:bCcYfIw0tFS3Zq4Fso_qo7_AvQ6dlQNP@rat.rmq2.cloudamqp.com/kzevgcua')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='calculate_order_service')

def callback(ch,method,properties,body):
    print("recieved")
    print(body)

channel.basic_consume(queue='calculate_order_service',on_message_callback=callback)

print("started consuming")

channel.start_consuming()
channel.close()