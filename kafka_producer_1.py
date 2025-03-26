"""
kafka_producer_1.py
This module provides functionality for producing and sending messages to a Kafka topic.
It includes a Kafka producer configuration, message serialization, and utility functions
for reading JSON files and sending messages to a Kafka topic.
Modules:
    - kafka: KafkaProducer for producing messages to Kafka.
    - json: For JSON serialization and deserialization.
    - time: For introducing delays between message sends.
    - random: For generating random delays.
    - my_secrets: For securely importing sensitive credentials.
Functions:
    - json_serializer(data): Serializes a Python object into a JSON-formatted byte string.
    - send_message(topic, message): Sends a message to the specified Kafka topic.
    - read_json_file(file_path): Reads a JSON file and returns its contents as a dictionary.
Usage:
    This script can be executed directly to read play-by-play data from a JSON file and
    send it to a specified Kafka topic. The producer is configured to use SASL_SSL for
    secure communication with the Kafka broker.
"""
import json
from time import sleep
from kafka import KafkaProducer
from my_secrets import sasl_plain_password

def json_serializer(data):
    """
    Serializes a Python object into a JSON-formatted byte string.

    Args:
        data (any): The Python object to be serialized.

    Returns:
        bytes: The JSON-encoded representation of the input data as a UTF-8 byte string.
    """
    return json.dumps(data).encode('utf-8')

producer = KafkaProducer(
    bootstrap_servers=['bigdata520-alt.servicebus.windows.net:9093'],
    value_serializer=json_serializer,
    security_protocol='SASL_SSL',
    sasl_mechanism='PLAIN',
    sasl_plain_username='$ConnectionString',
    sasl_plain_password=sasl_plain_password

)


def send_message(topic, message):
    """
    Sends a message to the specified Kafka topic.

    Args:
        topic (str): The name of the Kafka topic to which the message will be sent.
        message (str): The message to be sent to the Kafka topic.

    Returns:
        None
    """
    producer.send(topic, message)
    producer.flush()


def read_json_file(file_path: str) -> dict:
    """
    Reads a JSON file and returns its contents as a dictionary.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        dict: The contents of the JSON file.
    """
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data['game']['actions']


if __name__ == "__main__":
    topic_name = 'danrod'


    # FIXME (2025-03-25): Make this code walk the directory and send all files to the topic
    for id in range(14, 24):
        print(id)

        pbp_file_path = f'./play-by-play-data/play_by_play_data_00224010{id}.json'

        pbp_data = read_json_file(pbp_file_path)

        for id, action in enumerate(pbp_data):
            print(action)

            send_message(topic_name, action)
            print(f"Message sent to topic {topic_name}")
            # sleep(randint(1, 5))
            sleep(0.1)
