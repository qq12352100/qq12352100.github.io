'''
pip install kafka-python
'''
# producer.py
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

topic = 'test-topic'
message = {'hello': 'world', 'from': 'python'}

print(f"Sending message to {topic}: {message}")
producer.send(topic, value=message)
producer.flush()
print("Message sent!")