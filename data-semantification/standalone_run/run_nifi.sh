#!/bin/bash

# Define container name
CONTAINER_NAME=nifi

# Define ports
# Default NiFi web interface port is 8080
HOST_PORT=8080
CONTAINER_PORT=8080

# Check if the NiFi container is already running
if [ $(docker ps -q -f name=^/${CONTAINER_NAME}$ | wc -l) -gt 0 ]; then
    echo "Stopping and removing existing NiFi container..."
    docker stop ${CONTAINER_NAME}
    docker rm ${CONTAINER_NAME}
fi

echo "Starting Apache NiFi as a standalone container..."

# Run Apache NiFi container
docker run -d --name ${CONTAINER_NAME} -p ${HOST_PORT}:${CONTAINER_PORT} -e NIFI_WEB_HTTP_PORT=${CONTAINER_PORT} apache/nifi:latest

echo "Apache NiFi is starting up. It might take a few minutes for NiFi to be fully operational."
echo "Once ready, you can access the NiFi web interface by navigating to http://localhost:${HOST_PORT}/nifi in your web browser."

