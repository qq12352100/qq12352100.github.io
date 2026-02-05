'''
pip install kafka-python
'''
# consumer.py
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'test-topic',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',  # 从头开始读
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("Waiting for messages...")
for message in consumer:
    print(f"Received: {message.value}")