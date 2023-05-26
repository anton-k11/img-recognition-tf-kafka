# For GPU implmentation nvidia driver must be installed on the host and
# nvidia-container-runtime should installed and configured properly
#FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu20.04

FROM ubuntu:20.04

# Install necessary dependencies apt-get update &&
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    openjdk-17-jre-headless

# Set the working directory inside the container
WORKDIR /app

# Copy the built Spring Boot artifact to the container
COPY build/libs/ml-img-recognition.jar .

# Expose the default Spring Boot port
EXPOSE 8080

# Define the command to run the Spring Boot application
CMD ["java", "-jar", "ml-img-recognition.jar"]
