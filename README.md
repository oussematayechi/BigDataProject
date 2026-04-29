🏥 IoT Patient Monitoring System (Big Data Project)
📌 Overview

This project implements a real-time IoT-based patient monitoring system using a modern Big Data pipeline. It simulates medical sensor data, streams it through distributed systems, processes it in real time, and triggers alerts when abnormal health conditions are detected.

The system is fully containerized using Docker and follows an end-to-end data pipeline architecture.

🎯 Objectives
Build a complete Big Data pipeline
Simulate IoT healthcare data
Process streaming data using Apache Spark
Store data in MongoDB
Trigger real-time alerts based on thresholds
🏗️ Architecture
IoT Data Generator (Python)
        ↓
     Kafka (Streaming)
        ↓
 Spark Streaming Processing
        ↓
 ┌───────────────┬───────────────┐
 ↓                               ↓
MongoDB (Storage)         Alert System (Kafka / Logs)
🛠️ Tech Stack
Apache Kafka – Data streaming
Apache Spark – Real-time processing
MongoDB – Data storage
Docker & Docker Compose – Containerization
Python – Data simulation & processing
📂 Project Structure
iot-patient-monitoring/
├── docker-compose.yml       # Container orchestration
├── .env                     # Environment variables
├── README.md                # Project documentation
│
├── data/
│   ├── generate_data.py     # IoT data simulator
│   └── patients.csv         # Sample dataset
│
├── kafka/
│   ├── init_topics.py       # Kafka topic creation
│   ├── producer.py          # Data producer
│   └── consumer.py          # Data consumer
│
├── spark/
│   ├── Dockerfile           # Spark container config
│   ├── spark_processor.py   # Streaming + alert logic
│   └── requirements.txt     # Python dependencies
│
├── mongodb/
│   ├── init_db.py           # Database initialization
│   └── queries.js           # Useful queries
│
└── scripts/
    ├── start.sh             # Start system
    └── demo.sh              # Demo automation
📊 Dataset
Synthetic IoT patient data generated using Python
Each record contains:
timestamp
patientId
deviceId
metric (HeartRate, Temperature, etc.)
value
unit
⚙️ Installation & Setup
1️⃣ Clone the repository
git clone https://github.com/oussematayechi/BigDataProject.git
cd BigDataProject
2️⃣ Start Docker services
docker-compose up -d
3️⃣ Initialize Kafka topics
python kafka/init_topics.py
4️⃣ Start data producer
python kafka/producer.py
5️⃣ Run Spark Streaming job
docker exec -it spark-container spark-submit spark/spark_processor.py
🚨 Alert System

The system detects abnormal patient conditions based on thresholds:

Metric	Normal	Warning	Critical
HeartRate	60–100 bpm	<50 or >120	<40 or >150
Temperature	36–37.2 °C	>38	>39.5 or <35
Oxygen Level	95–100 %	<93	<90
Blood Pressure	80–120 mmHg	>130	>180 or <70
Respiratory Rate	12–20	<10 or >24	<8 or >30

Alerts are:

Stored in MongoDB
Sent to Kafka topics
Logged in real time
🗄️ MongoDB Collections
patients
sensor_readings
devices
▶️ Demo

Run the demo script:

bash scripts/demo.sh
📸 Screenshots (Optional)

Add screenshots of:

Docker containers running
Kafka messages
MongoDB data
Alerts
👨‍💻 Author
Oussema Tayechi et Jaziri Mohamed Ali
Embedded Telecommunications Engineering Student
ENISo – Tunisia 🇹🇳
📜 License

This project is for academic purposes .
