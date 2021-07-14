import pika,requests
from application.OrderProcessorApi.api.OrderInfo import ExecutionPriceClient

params = pika.URLParameters('amqps://kzevgcua:bCcYfIw0tFS3Zq4Fso_qo7_AvQ6dlQNP@rat.rmq2.cloudamqp.com/kzevgcua')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='process_orders')

def callback(ch,method,properties,body):
    order_id = int(body)
    ExecutionPriceClient.calculate(order_id)

channel.basic_consume(queue='process_orders',on_message_callback=callback,auto_ack=True)

print("Starting Queue")

channel.start_consuming()
channel.close()