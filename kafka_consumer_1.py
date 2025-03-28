"""
Kafka Consumer Module
This module provides functionality to consume messages from a Kafka topic
using the `KafkaConsumer` class from the `kafka-python` library. It includes
a custom JSON deserializer for processing message payloads.
Functions:
    json_deserializer(data): Deserializes a JSON-formatted byte string into
    a Python object.
Usage:
    This module is designed to connect to a Kafka broker, authenticate using
    SASL/PLAIN, and consume messages from a specified topic.
Dependencies:
    - kafka-python
    - my_secrets (for sensitive credentials)
    - json
"""

import json

from kafka import KafkaConsumer

from my_secrets import sasl_plain_password


def json_deserializer(data):
    """
    Deserializes a JSON-formatted byte string into a Python object.

    Args:
        data (bytes): The JSON-encoded byte string.

    Returns:
        any: The Python object represented by the JSON data.
    """
    return json.loads(data.decode('utf-8'))

# Define Kafka consumer
consumer = KafkaConsumer(
    "danrod",  # Replace with your topic name
    bootstrap_servers=['bigdata520-alt.servicebus.windows.net:9093'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=json_deserializer,
    security_protocol='SASL_SSL',
    sasl_mechanism='PLAIN',
    sasl_plain_username='$ConnectionString',
    sasl_plain_password=sasl_plain_password
)

# Consume messages
try:
    print("Starting Kafka consumer...")
    for message in consumer:
        print(f"Received message: {message.value}")
except KeyboardInterrupt:
    print("Kafka consumer stopped.")
finally:
    consumer.close()
