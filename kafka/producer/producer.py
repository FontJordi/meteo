from kafka import KafkaProducer
import json
import threading
import time
import random

class MadeUpAPI:
    """
    A class representing a made-up API for generating fake data.
    """
    def __init__(self):
        """
        Constructor method initializing the MadeUpAPI object.
        """
        self.values = [random.random() for _ in range(10)]  # Correct usage of random.random()
    
    def data_generator(self):
        """
        Method for generating fake data.

        Returns:
        - list: A list of dictionaries containing fake data.
        """
        self.keys = [random.randint(1,8) for _ in range(10)]
        self.timestamps = [time.time() for _ in range(10)]
        data = []
        for ts, key, val in zip(self.timestamps, self.keys, self.values):
            data.append({"fakeTimestamp": ts, "fakeKey": key, "fakeValue": val})
        return data
        

class MyProducer:
    """
    A class for producing data to a Kafka topic using KafkaProducer.
    """
    def __init__(self, brokers, topic):
        """
        Constructor method initializing the MyProducer object.

        Args:
        - brokers (list): List of Kafka broker addresses.
        - topic (str): The Kafka topic to which data will be produced.
        """
        self.producer = KafkaProducer(bootstrap_servers=brokers,
                                      value_serializer=lambda x: x)
        self.topic = topic
        self.api = MadeUpAPI()

    def fetch_and_send_data(self):
        """
        Method for fetching and sending data to Kafka brokers.
        """
        while True:
            # Fetch data from madeUp API
            data = self.api.data_generator()
            print(data)
            # Send data to Kafka brokers
            for timekeyvalue in data:
                print(timekeyvalue)
                key = str(timekeyvalue['fakeKey']).encode('utf-8')  # Convert key to bytes
                value = json.dumps(timekeyvalue).encode('utf-8')
                self.producer.send(topic=self.topic, key=key, value=value)
            
            # Sleep for some time before fetching data again
            time.sleep(10)

if __name__ == "__main__":
    # Define Kafka brokers and topic
    brokers = ['localhost:9092', 'localhost:9093', 'localhost:9094']
    topic = 'my-topic-2'

    # Create an instance of KafkaProducer
    opensky_producer = MyProducer(brokers, topic)

    # Start the producer
    opensky_producer.fetch_and_send_data() 