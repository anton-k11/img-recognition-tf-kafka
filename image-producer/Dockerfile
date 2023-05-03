FROM python:3.12.0a7-bullseye

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY image_producer.py .

# Set environment variables
#ENV IMG_KAFKA_TOPIC="image-topic"
#ENV KAFKA_BOOTSTRAP_SERVERS="localhost:9092"

# Run application
CMD ["python", "image_producer.py"]
