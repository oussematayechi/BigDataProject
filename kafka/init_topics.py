from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError
import time

def create_topics():
    time.sleep(5)
    admin_client = KafkaAdminClient(
        bootstrap_servers="localhost:9092",
        client_id='topic_creator'
    )
    topics = [
        NewTopic(name="patient.heartrate", num_partitions=3, replication_factor=1),
        NewTopic(name="patient.temperature", num_partitions=3, replication_factor=1),
        NewTopic(name="patient.oxygen", num_partitions=3, replication_factor=1),
        NewTopic(name="patient.bloodpressure", num_partitions=3, replication_factor=1),
        NewTopic(name="patient.respiratoryrate", num_partitions=3, replication_factor=1),
        NewTopic(name="patient.alerts.critical", num_partitions=1, replication_factor=1),
        NewTopic(name="patient.alerts.warning", num_partitions=1, replication_factor=1)
    ]
    for topic in topics:
        try:
            admin_client.create_topics(new_topics=[topic], validate_only=False)
            print(f"Topic created: {topic.name}")
        except TopicAlreadyExistsError:
            print(f"Topic already exists: {topic.name}")
    admin_client.close()

if __name__ == "__main__":
    create_topics()