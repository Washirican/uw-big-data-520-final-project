from kafka import KafkaProducer
import json
from my_secrets import sasl_plain_password
from tutorial_data_faker import get_registered_user
from time import sleep

def json_serializer(data):
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
    producer.send(topic, message)
    producer.flush()


if __name__ == "__main__":
    # TODO (2025-03-23): Send message key
    while 1==1:
        register_user = get_registered_user()
        send_message('danrod', register_user)
        sleep(3)


