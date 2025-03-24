import os

env_var = os.getenv('AZURE_EVENT_HUBS_SASL_PLAIN_PASSWORD')
sasl_plain_password = env_var[1:-1]
