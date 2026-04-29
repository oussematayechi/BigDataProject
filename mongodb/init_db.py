from pymongo import MongoClient
import pandas as pd
import os

def initialize_database():
    # Use absolute path relative to script location
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    patients_path = os.path.join(base_dir, 'data', 'patients.csv')
    devices_path = os.path.join(base_dir, 'data', 'devices.csv')
    
    client = MongoClient('mongodb://admin:admin123@localhost:27017/')
    db = client['patient_monitoring']
    
    # Load and insert patients
    if os.path.exists(patients_path):
        patients_df = pd.read_csv(patients_path)
        db.patients.drop()
        db.patients.insert_many(patients_df.to_dict('records'))
        print(f"Inserted {len(patients_df)} patients")
    else:
        print(f"Warning: {patients_path} not found")
    
    # Load and insert devices
    if os.path.exists(devices_path):
        devices_df = pd.read_csv(devices_path)
        db.devices.drop()
        db.devices.insert_many(devices_df.to_dict('records'))
        print(f"Inserted {len(devices_df)} devices")
    else:
        print(f"Warning: {devices_path} not found")
    
    # Create indexes
    db.patients.create_index("patientId", unique=True)
    db.devices.create_index("deviceId", unique=True)
    db.processed_readings.create_index([("patientId", 1), ("timestamp", -1)])
    db.processed_readings.create_index("alertLevel")
    
    print("Database initialized with indexes")
    client.close()

if __name__ == "__main__":
    initialize_database()