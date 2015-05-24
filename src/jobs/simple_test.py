#!/usr/bin/env python
import random
import threading, logging, time

from kafka.client import KafkaClient
from kafka.consumer import SimpleConsumer
from kafka.producer import SimpleProducer

class Producer(threading.Thread):
    daemon = True

    def __init__(self, queue_host, queue_port, topic):
        
        threading.Thread.__init__(self)

        self.queue_port = queue_port
        self.queue_host = queue_host
        self.topic = topic
        self.client = KafkaClient(queue_host + ':' + str(queue_port))
        self._test_messages = [ '0 (first first message)',
                                'First message, only test',
                                'Second message, only test',
                                '3rd message, only test',
                                '4th message, only test',
                                '5th message, only test',
                                '6th message, only test',
                                '7th message, only test',
                                '8th message, only test',
                                '10th message, only test']


    def run(self):
        while True:

            randomized = random.randint(0, 9)

            message = self._test_messages[randomized]
            
            producer = SimpleProducer(self.client)
            producer.send_messages(self.topic, 
                                   message)

            logging.info('Sent message: ' + message)

            time.sleep(2)


class Consumer(threading.Thread):
    daemon = True

    def __init__( self, queue_host, queue_port, topic):
        
        threading.Thread.__init__(self)

        self.queue_port = queue_port
        self.queue_host = queue_host
        self.topic = topic

    def run(self):

        client = KafkaClient(self.queue_host + ":" + str(self.queue_port))
        consumer = SimpleConsumer(client, "test-group", self.topic)

        for message in consumer:
            logging.info(message)


def main():

    boot2docker = '192.168.59.103'

    threads = [
        Producer(boot2docker, 9092, 'test'),
        Consumer(boot2docker, 9092, 'test')
    ]

    for t in threads:
        t.start()

    while True:
        pass

if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
        level=logging.INFO
        )
    main()