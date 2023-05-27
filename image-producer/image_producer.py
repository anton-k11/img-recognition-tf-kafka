import os
import time
import logging
from kafka import KafkaProducer
from kafka.errors import KafkaError
from pathlib import Path

# Read environment variables
img_dir = os.getenv('IMG_DIRECTORY', '/home/pictures/')
img_topic = os.getenv('IMG_KAFKA_TOPIC', 'image-topic')
producer_id = os.getenv('HOSTNAME')
bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')


# Set up Kafka producer
producer = KafkaProducer(
    bootstrap_servers=bootstrap_servers,
    value_serializer=None,
    max_request_size=6000000
)

# Set up logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

i=0

# Set up function to read and send images
def send_image(filename):
    try:
        with open(filename, 'rb') as file:
            file_bytes = file.read()

            # Create Kafka message with image bytes and header
            timestamp = int(time.time() * 1000)  # Current timestamp in milliseconds
            headers = [
                ('timestamp', str(timestamp).encode('utf-8')),
                ('producer_id', str(producer_id).encode('utf-8'))
            ]

            global i
            i=i+1
            key = str(f'a{i}').encode('utf-8')
            # Send message to Kafka topic with headers
            metadata_future = producer.send(img_topic, 
                                            key=key,
                                            value=file_bytes,
                                            headers=headers
                                            )
            metadata = metadata_future.get(timeout=10)

            logging.info(f'Sent image {filename} to Kafka topic {img_topic}, with {headers}. with {metadata}')
    except KafkaError as e:
        logging.error(f'Error sending image {filename} to Kafka topic {img_topic}: {e}')
    except Exception as e:
        logging.error(f'Error reading image {filename}: {e}')

# Set up main function
def main():
    logging.info(f'Reading images from directory: {img_dir}')

    # Log bootstrap servers and image topic
    logging.info(f'Using Kafka bootstrap servers: {bootstrap_servers}')
    logging.info(f'Sending images to Kafka topic: {img_topic}')

    while True:
        # Loop through images in directory and send them to Kafka topic
        for filename in os.listdir(img_dir):
            if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
                send_image(Path(img_dir)/filename)
                time.sleep(0.5)  # Pause for 1 second between each image
        producer.flush()

    # Close Kafka producer
    producer.close()

if __name__ == '__main__':
    main()
