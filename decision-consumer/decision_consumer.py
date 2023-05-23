import os
import time
import json
import logging
from kafka import KafkaConsumer
from kafka.errors import KafkaError


# Read environment variables
decision_topic = os.getenv('DECISION_KAFKA_TOPIC', 'decision-topic')
bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')

# Set up Kafka producer
consumer = KafkaConsumer(decision_topic, bootstrap_servers=bootstrap_servers)

# Set up logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# Set up logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

def consume_decision():
    # Consume messages
    for message in consumer:
        try:
            # Extract headers
            headers = dict(message.headers)

            # Extract payload
            payload = message.value.decode('utf-8')

            # Parse JSON payload
            data = json.loads(payload)

            # Log JSON and headers on a single line
            log_message = f'Payload: {data} - Headers: {headers}'
            logging.info(log_message)
            
            timestamp = int(time.time() * 1000)  # Current timestamp in milliseconds
            start_timestamp = int(headers.get("timestamp").decode("utf-8") )
            logging.info(f'Delivered in {timestamp - start_timestamp} ms.')

        except Exception as e:
            logging.error(f'Error processing message: {e}')


# Set up main function
def main():
    # Log bootstrap servers and image topic
    logging.info(f'Using Kafka bootstrap servers: {bootstrap_servers}')
    logging.info(f'Consuming from Kafka topic: {decision_topic}')

    consume_decision()
    consumer


if __name__ == '__main__':
    main()
