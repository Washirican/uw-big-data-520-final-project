from kafka import KafkaProducer
import json
from data_faker import get_registered_user
from time import sleep
import os

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
    topic_name = 'danrod'
    # message = {'key': 'value'}
    # send_message(topic_name, message)
    # print(f"Message sent to topic {topic_name}")
    pbp_file_path = './game-play-by-play-data/game_play_by_play_data_0022401014.json'

    pbp_data = read_json_file(pbp_file_path)

    for id, action in enumerate(pbp_data):
        print(action)

    # while 1==1:
        # user = get_registered_user()
        send_message(topic_name, action)
        print(f"Message sent to topic {topic_name}")
        # TODO (2025-03-22): Set random sleep time.
        sleep(2)