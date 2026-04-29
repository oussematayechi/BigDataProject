# 🏥 IoT Patient Monitoring System – Big Data Pipeline

[![License](https://img.shields.io/badge/License-Academic%20Use-blue.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-24.0+-blue)](https://docker.com)
[![Kafka](https://img.shields.io/badge/Kafka-3.5+-black)](https://kafka.apache.org)
[![Spark](https://img.shields.io/badge/Spark-3.4+-orange)](https://spark.apache.org)
[![MongoDB](https://img.shields.io/badge/MongoDB-7.0+-green)](https://mongodb.com)

## 📌 Overview
Real-time IoT-based patient monitoring system using Kafka, Spark Streaming, and MongoDB. Simulates medical sensor data, detects anomalies, and triggers alerts.

## 🎯 Objectives
- Build a complete Big Data pipeline for healthcare IoT
- Simulate realistic medical sensor data
- Stream data using **Apache Kafka**
- Process streaming data with **Apache Spark Structured Streaming**
- Store historical data in **MongoDB**
- Trigger **real‑time alerts** based on clinical thresholds

## 🏗️ Architecture
```
IoT Data Generator (Python) → Kafka → Spark Streaming → MongoDB (Storage)
                                                      → Alert System (Kafka/Logs)
```

## 🛠️ Tech Stack
| Component | Technology |
|-----------|-------------|
| Stream Processing | Apache Spark 3.4 |
| Message Broker | Apache Kafka 3.5 |
| Storage | MongoDB 7.0 |
| Containerization | Docker & Compose |
| Simulation | Python 3.9+ |

## 📂 Project Structure
```
iot-patient-monitoring/
├── docker-compose.yml
├── .env
├── README.md
├── data/
│   ├── generate_data.py
│   └── patients.csv
├── kafka/
│   ├── init_topics.py
│   ├── producer.py
│   └── consumer.py
├── spark/
│   ├── Dockerfile
│   ├── spark_processor.py
│   └── requirements.txt
├── mongodb/
│   ├── init_db.py
│   └── queries.js
└── scripts/
    ├── start.sh
    └── demo.sh
```

## 📊 Dataset (Synthetic)
Each sensor record contains:
- `timestamp` (ISO 8601)
- `patientId`
- `deviceId`
- `metric` (HeartRate, Temperature, OxygenLevel, BloodPressure, RespiratoryRate)
- `value` (float)
- `unit`

Generated at ~10 records/second.

## ⚙️ Installation & Setup

### Prerequisites
- Docker ≥ 24.0
- Docker Compose ≥ 2.20
- Python 3.9+

### Steps
```bash
git clone https://github.com/oussematayechi/BigDataProject
cd iot-patient-monitoring
docker-compose up -d
docker exec -it kafka-broker python /kafka/init_topics.py
docker exec -it mongodb python /mongodb/init_db.py
docker exec -d kafka-broker python /kafka/producer.py
docker exec -it spark-master spark-submit /spark/spark_processor.py
```

> 💡 Use `bash scripts/start.sh` to automate all steps.

## 🚨 Alert System
Thresholds for abnormal detection:

| Metric | Normal | Warning | Critical |
|--------|--------|---------|----------|
| HeartRate | 60–100 bpm | <50 or >120 | <40 or >150 |
| Temperature | 36–37.2 °C | >38 | >39.5 or <35 |
| OxygenLevel | 95–100 % | <93 | <90 |
| BloodPressure | 80–120 mmHg | >130 | >180 or <70 |
| RespiratoryRate | 12–20 | <10 or >24 | <8 or >30 |

Alerts are:
- Stored in MongoDB `alerts` collection
- Published to Kafka topic `alerts`
- Printed in Spark logs

## 🗄️ MongoDB Collections
- `patients` – registry of patients
- `sensor_readings` – all historical telemetry
- `alerts` – triggered anomalies

## ▶️ Demo
```bash
bash scripts/demo.sh
```

## 👨‍💻 Author
Oussema Tayechi & Mohamed Ali Jaziri
*Embedded Telecommunications Engineering Student*
ENISo – Tunisia 🇹🇳

## 📜 License
This project is for **academic purposes only**.
© 2026