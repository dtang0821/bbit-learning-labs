import os
import pika
from producer_interface import mqProducerInterface
class mqProducer(mqProducerInterface):
    def __init__(self, exchange_name: str, routing_key: str):
        self.exchange_name = exchange_name
        self.routing_key = routing_key
        self.setupRMQConnection()

    def setupRMQConnection():
        con_params = pika.URLParameters(os.environ["AMPQ_URL"])
        self.connection = pika.BlockingConnection(parameters = con_params)
        self.channel = self.connection.channel()

    def publishOrder(self, message: str):
        self.channel.basic_publish(
            exchange = self.exchange_name,
            routing_key = self.routing_key,
            body = message
        )
        self.channel.close()
        self.connection.close()
        
    
