import os


def get_kafka_brokers():
    return os.environ.get('KAFKA_BROKERS', 'localhost:29092')
