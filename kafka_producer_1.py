"""
This module is a Kafka producer script designed to send JSON-serialized messages
to a specified Kafka topic. It reads play-by-play data from JSON files, processes
the data, and sends it to a Kafka topic for further consumption.
The script includes the following functionalities:
- Serialization of Python objects into JSON-formatted byte strings.
- Configuration of a Kafka producer with SASL_SSL security protocol.
- Sending messages to a Kafka topic.
- Reading and parsing JSON files containing game actions.
Usage:
- Update the `GAME_IDs` list in the `game_ids` module with the desired game IDs.
- Ensure the play-by-play JSON files are available in the specified directory.
- Run the script to send the data to the Kafka topic.
Dependencies:
- kafka-python: A library for working with Apache Kafka.
- my_secrets: A module containing sensitive information like the SASL password.
- game_ids: A module containing a list of game IDs to process.
Note:
- Replace the placeholder Kafka server and topic names with actual values.
- Ensure proper security measures are in place to protect sensitive information.

"""
import json
from time import sleep
from kafka import KafkaProducer
from my_secrets import sasl_plain_password
from game_ids import GAME_IDs

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


def send_message(topic: str, message: dict) -> None:
    """
    Sends a message to the specified Kafka topic.

    Args:
        topic (str): The name of the Kafka topic to which the message will be sent.
        message (dict): The message to be sent to the Kafka topic.

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
    with open(file_path, 'r', encoding="utf-8") as file:
        data = json.load(file)
    return data['game']['actions']


if __name__ == "__main__":
    TOPIC_NAME = "danrod"

    for game_id in GAME_IDs:
        print(game_id)

        PBP_FILE_PATH = f'./play-by-play-data/play_by_play_data_{game_id}.json'

        pbp_data = read_json_file(PBP_FILE_PATH)
        # k = 0
        for idx, action in enumerate(pbp_data):
            print(action)

            send_message(TOPIC_NAME, action)
            # k += 1
            # message = {'key': k, 'value': action}
            # producer.send(TOPIC_NAME, message)


            print(f"Data for game_id {game_id} sent to topic {TOPIC_NAME}.")

            # sleep(randint(1, 5))
            # sleep(0.1)
