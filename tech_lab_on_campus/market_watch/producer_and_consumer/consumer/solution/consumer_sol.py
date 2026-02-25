import pika
import os

from consumer_interface import mqConsumerInterface

class mqConsumer(mqConsumerInterface):
    def __init__(self, binding_key: str, exchange_name: str, queue_name: str, **kwargs) -> None:
        self.queue_name = queue_name
        self.exchange_name = exchange_name
        self.binding_key = binding_key
        self.message_handler = kwargs.get('message_handler', None)

        self.setupRMQConnection()

    def setupRMQConnection(self) -> None:
        con_params = pika.URLParameters(os.environ['AMQP_URL'])
        self.connection = pika.BlockingConnection(parameters=con_params)
        self.channel = self.connection.channel()

        self.channel.exchange_declare(exchange=self.exchange_name, exchange_type='direct')
        self.channel.queue_declare(queue=self.queue_name)

        self.channel.queue_bind(exchange=self.exchange_name, queue=self.queue_name, routing_key=self.binding_key)

        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.on_message_callback, auto_ack=False)

    def on_message_callback(self, channel, method_frame, header_frame, body) -> None:
        if self.message_handler:
            self.message_handler(body)
        else:
            print(f"Received message: {body}")
        
        self.channel.basic_ack(delivery_tag=method_frame.delivery_tag, multiple=False)


    def startConsuming(self) -> None:
        print('Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    def __del__(self) -> None:
        print("Closing RMQ connection on destruction")
        if hasattr(self, 'channel') and self.channel.is_open:
            self.channel.close()
            
        if hasattr(self, 'connection') and self.connection.is_open:
            self.connection.close()
