from kafka import KafkaProducer
import json
from data_faker import get_registered_user
from time import sleep
import os
from random import randint

def json_serializer(data):
    return json.dumps(data).encode('utf-8')

producer = KafkaProducer(
    bootstrap_servers=['bigdata520-alt.servicebus.windows.net:9093'],
    value_serializer=json_serializer,
    security_protocol='SASL_SSL',
    sasl_mechanism='PLAIN',
    sasl_plain_username='$ConnectionString',

    # FIXME (2025-03-22): How to get environment variable value?
    sasl_plain_password=os.getenv('AZURE_EVENT_HUBS_SASL_PLAIN_PASSWORD')

)

def send_message(topic, message):
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
    # TODO (2025-03-23): Make a single script stream data from multiple games. Or create multiple streaming scripts.
    topic_name = 'danrod'

    pbp_file_path = './play-by-play-data/play_by_play_data_0022401014.json'

    pbp_data = read_json_file(pbp_file_path)

    for id, action in enumerate(pbp_data):
        print(action)

        send_message(topic_name, action)
        print(f"Message sent to topic {topic_name}")
        sleep(randint(1, 5))
