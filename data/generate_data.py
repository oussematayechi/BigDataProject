import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from faker import Faker

fake = Faker()

# Patient data
patients = []
for i in range(1, 16):  # 15 patients
    patient = {
        'patientId': f'P-{i:04d}',
        'name': fake.name(),
        'dateOfBirth': fake.date_of_birth(minimum_age=18, maximum_age=90).isoformat(),
        'gender': random.choice(['M', 'F']),
        'ward': random.choice(['Cardiology', 'ICU', 'General', 'Pediatrics', 'Neurology']),
        'medicalHistory': random.sample(['hypertension', 'diabetes', 'asthma', 'none'], 
                                        random.randint(0, 2)),
        'assignedDevices': []
    }
    patients.append(patient)

# Save patients
pd.DataFrame(patients).to_csv('patients.csv', index=False)

# Generate sensor readings
def generate_sensor_data(num_records=10000):
    metrics = {
        'HeartRate': {'normal': (60, 100), 'warning': ((50, 60), (100, 120)), 
                      'critical': ((0, 40), (150, 200)), 'unit': 'bpm'},
        'Temperature': {'normal': (36.1, 37.2), 'warning': ((37.2, 38.0),),
                        'critical': ((39.5, 42), (35, 36.1)), 'unit': '°C'},
        'OxygenLevel': {'normal': (95, 100), 'warning': ((93, 95),),
                        'critical': ((0, 90),), 'unit': 'SpO2 %'},
        'BloodPressure': {'normal': (80, 120), 'warning': ((120, 130),),
                          'critical': ((180, 250), (0, 70)), 'unit': 'mmHg'},
        'RespiratoryRate': {'normal': (12, 20), 'warning': ((10, 12), (20, 24)),
                           'critical': ((0, 8), (30, 50)), 'unit': 'breaths/min'}
    }
    
    readings = []
    devices = []
    
    for i in range(num_records):
        patient = random.choice(patients)
        metric = random.choice(list(metrics.keys()))
        metric_config = metrics[metric]
        
        # Determine alert level
        rand = random.random()
        if rand < 0.7:  # 70% normal
            value = random.uniform(*metric_config['normal'])
            alert = 'normal'
        elif rand < 0.9:  # 20% warning
            warning_range = random.choice(metric_config['warning'])
            value = random.uniform(*warning_range)
            alert = 'warning'
        else:  # 10% critical
            critical_range = random.choice(metric_config['critical'])
            value = random.uniform(*critical_range)
            alert = 'critical'
        
        reading = {
            'timestamp': (datetime.now() - timedelta(days=random.randint(0, 30),
                                                    hours=random.randint(0, 23),
                                                    minutes=random.randint(0, 59))).isoformat() + 'Z',
            'patientId': patient['patientId'],
            'deviceId': f"DEV-{metric[:2].upper()}-{random.randint(1, 20):03d}",
            'metric': metric,
            'value': round(value, 1),
            'unit': metric_config['unit'],
            'alertLevel': alert
        }
        readings.append(reading)
        
        # Add device info
        device = {
            'deviceId': reading['deviceId'],
            'type': f"{metric}Monitor",
            'manufacturer': random.choice(['Philips', 'GE', 'Siemens', 'Medtronic']),
            'capabilities': [metric],
            'patientId': patient['patientId'],
            'installedAt': datetime.now().isoformat() + 'Z'
        }
        devices.append(device)
    
    return readings, list({d['deviceId']: d for d in devices}.values())

if __name__ == "__main__":
    readings, devices = generate_sensor_data(10000)
    pd.DataFrame(readings).to_csv('sensor_readings.csv', index=False)
    pd.DataFrame(devices).to_csv('devices.csv', index=False)
    print("Dataset generated: 10000 readings, 15 patients, unique devices")