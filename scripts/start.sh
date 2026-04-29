#!/bin/bash

echo "Starting Docker containers..."
docker-compose up -d

echo "Waiting for services to be ready..."
sleep 30

echo "Creating Kafka topics..."
python kafka/init_topics.py

echo "Initializing MongoDB..."
python mongodb/init_db.py

echo "Starting data generator..."
python kafka/producer.py

echo "System is running!"
echo "Access:"
echo "- MongoDB Express: http://localhost:8081"
echo "- Spark Master: http://localhost:8080"