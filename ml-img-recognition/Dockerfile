ARG BASE_IMAGE=ubuntu:20.04
FROM $BASE_IMAGE

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
