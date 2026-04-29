from kafka import KafkaProducer
import json
import pandas as pd
import time
from datetime import datetime
import os

class IoTSensorProducer:
    def __init__(self):
        self.producer = KafkaProducer(
    		bootstrap_servers='localhost:9092',
    		value_serializer=lambda v: json.dumps(v).encode('utf-8')
	)
        self.topic_mapping = {
            'HeartRate': 'patient.heartrate',
            'Temperature': 'patient.temperature',
            'OxygenLevel': 'patient.oxygen',
            'BloodPressure': 'patient.bloodpressure',
            'RespiratoryRate': 'patient.respiratoryrate'
        }
    
    def send_reading(self, reading):
        topic = self.topic_mapping.get(reading['metric'])
        if topic:
            future = self.producer.send(topic, reading)
            self.producer.flush()
            return future
        return None
    
    def stream_from_csv(self, csv_file, delay=1):
        if not os.path.exists(csv_file):
            print(f"Error: {csv_file} not found. Run data/generate_data.py first.")
            return
        data = pd.read_csv(csv_file)
        print(f"Streaming {len(data)} readings to Kafka...")
        
        for idx, row in data.iterrows():
            reading = row.to_dict()
            reading['timestamp'] = datetime.now().isoformat() + 'Z'
            
            # Convert numpy types
            for k, v in reading.items():
                if hasattr(v, 'item'):
                    reading[k] = v.item()
            
            self.send_reading(reading)
            
            # Inject synthetic critical alert for demo every 500 records
            if idx % 500 == 0 and idx > 0:
                critical_reading = reading.copy()
                critical_reading['value'] = 200.0
                critical_reading['metric'] = 'HeartRate'
                critical_reading['alertLevel'] = 'critical'
                self.send_reading(critical_reading)
                print(f"⚠️  Injected CRITICAL alert at record {idx}")
            
            print(f"Sent: {reading['patientId']} - {reading['metric']}: {reading['value']} ({reading['alertLevel']})")
            time.sleep(delay)
        
        self.producer.close()

if __name__ == "__main__":
    producer = IoTSensorProducer()
    producer.stream_from_csv('data/sensor_readings.csv', delay=0.5)