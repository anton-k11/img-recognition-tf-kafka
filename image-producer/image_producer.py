import os
import time
import logging
from kafka import KafkaProducer
from kafka.errors import KafkaError
from PIL import Image

# Read environment variables
img_topic = os.getenv('IMG_KAFKA_TOPIC', 'image-topic')
bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')

# Set up Kafka producer
producer = KafkaProducer(bootstrap_servers=bootstrap_servers)

# Set up image directory
img_dir = 'path/to/image/folder/'

# Set up logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# Set up function to read and send images
def send_image(filename):
    try:
        # Read image
        img = Image.open(os.path.join(img_dir, filename))

        # Convert image to bytes
        img_bytes = img.tobytes()

        # Create Kafka message with image bytes and header
        timestamp = int(time.time() * 1000)  # Current timestamp in milliseconds
        message = img_bytes
        headers = [
            ('timestamp', str(timestamp).encode('utf-8'))
        ]

        # Send message to Kafka topic with headers
        producer.send(img_topic, value=message, headers=headers)

        logging.info(f'Sent image {filename} to Kafka topic {img_topic}.')
    except KafkaError as e:
        logging.error(f'Error sending image {filename} to Kafka topic {img_topic}: {e}')
    except Exception as e:
        logging.error(f'Error reading image {filename}: {e}')

# Set up main function
def main():
    # Log bootstrap servers and image topic
    logging.info(f'Using Kafka bootstrap servers: {bootstrap_servers}')
    logging.info(f'Sending images to Kafka topic: {img_topic}')

    # Loop through images in directory and send them to Kafka topic
    for filename in os.listdir(img_dir):
        if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
            send_image(filename)
            time.sleep(1)  # Pause for 1 second between each image

    # Close Kafka producer
    producer.close()

if __name__ == '__main__':
    main()
