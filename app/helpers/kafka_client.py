import json
import asyncio
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from app import config

async def send_message(topic, message):
    producer = AIOKafkaProducer(
        bootstrap_servers=config.KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )
    try:
        await producer.start()
        await producer.send_and_wait(topic, message)
    except Exception as e:
        print(f"Error with message to {topic}: {e}")
        #Decide if a critical error or we can continue with other messages
        #Decide if we need to stop the application and notify External system our system is down
        raise
    finally:
        await producer.stop()

async def consume_messages(topics, group_id):
    consumer = AIOKafkaConsumer(
        *topics,
        bootstrap_servers=config.KAFKA_BOOTSTRAP_SERVERS,
        group_id=group_id,
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='latest',
        enable_auto_commit=False
    )
    
    await consumer.start()
    return consumer

async def commit_message(consumer):
    await consumer.commit()