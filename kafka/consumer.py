from kafka import KafkaConsumer
from pymongo import MongoClient
import json
from datetime import datetime
import threading

# MongoDB connection
mongo_client = MongoClient("mongodb://admin:admin123@localhost:27017/")
db = mongo_client["patient_monitoring"]

# Kafka Consumer
consumer = KafkaConsumer(
    'patient.heartrate',
    'patient.temperature',
    'patient.oxygen',
    'patient.bloodpressure',
    'patient.respiratoryrate',
    'patient.alerts.critical',
    'patient.alerts.warning',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda v: json.loads(v.decode('utf-8')),
    group_id='patient-monitoring-group',
    auto_offset_reset='earliest'
)

print("✅ Consumer started. Listening for messages...")

for message in consumer:
    topic = message.topic
    data = message.value
    data['received_at'] = datetime.now().isoformat()
    data['kafka_topic'] = topic

    # Route to correct MongoDB collection
    if 'heartrate' in topic:
        db.heartrate.insert_one(data)
    elif 'temperature' in topic:
        db.temperature.insert_one(data)
    elif 'oxygen' in topic:
        db.oxygen.insert_one(data)
    elif 'bloodpressure' in topic:
        db.bloodpressure.insert_one(data)
    elif 'respiratoryrate' in topic:
        db.respiratoryrate.insert_one(data)
    elif 'critical' in topic:
        db.alerts_critical.insert_one(data)
    elif 'warning' in topic:
        db.alerts_warning.insert_one(data)

    print(f"📥 [{topic}] Patient {data.get('patientId','?')} - "
          f"{data.get('metric','?')}: {data.get('value','?')} "
          f"({data.get('alertLevel','?')})")