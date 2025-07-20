#This is the base consumer class for all customer consumers
#This is resposnible for transforming Internal Data to External Data and storing it in DynamoDB
#It also commits the offset of the message to Kafka
#It also handles error processing and retry logic
import asyncio
import uuid
from app.helpers import kafka_client
from app.helpers.mock_dynamodb_client import mock_dynamodb_client
from app.transformers.transform_factory import TransformFactory
from app import config


class BaseConsumer:
    def __init__(self, customer_config, customer_name):
        self.customer_name = customer_name
        self.topics = customer_config["topics"]
        self.consumer_group = customer_config["consumer_group"]
        self.transformer_name = customer_config["transformer"]
        self.webhook_url = customer_config["webhook_url"]
    
    async def store_to_dynamodb(self, transformed_data, topic, worker_id):
        message_id = str(uuid.uuid4())
        success = await mock_dynamodb_client.store_message(
            customer_name=self.customer_name,
            table=topic,
            message_id=message_id,
            transformed_data=transformed_data
        )
        
        if success:
            print(f"{self.customer_name} worker {worker_id} stored {topic} message {message_id} to DynamoDB")
            return True
        else:
            print(f"{self.customer_name} worker {worker_id} failed to store {topic} message to DynamoDB")
            return False
    
    async def process_single_message(self, msg, worker_id, consumer):
        try:
            record = msg.value
            record["table"] = msg.topic
            transformed_data = TransformFactory.transform_message(self.transformer_name, record)
            
            success = await self.store_to_dynamodb(transformed_data, msg.topic, worker_id)
            
            if success:
                await kafka_client.commit_message(consumer)
            else:
                print(f"Failed to store message to DynamoDB")
                await self.retry_and_store_error_for_analysis(msg, worker_id, consumer)
        except ValueError as e:
            if "validation failed" in str(e).lower():
                print(f"Validation error for message: {e}")
                await self.retry_and_store_error_for_analysis(msg, worker_id, consumer)
            else:
                print(f"Value error processing message: {e}")
                await self.retry_and_store_error_for_analysis(msg, worker_id, consumer)
                
        except Exception as e:
            print(f"Error processing message: {e}")
            await self.retry_and_store_error_for_analysis(msg, worker_id, consumer)
    
    async def consume_messages(self, worker_id):
        consumer = await kafka_client.consume_messages(self.topics, self.consumer_group)
        print(f"{self.customer_name} consumeing messages")
        
        try:
            async for msg in consumer:
                await self.process_single_message(msg, worker_id, consumer)
        except Exception as e:
            print(f"Error in {self.customer_name} consumer: {e}")
        finally:
            await consumer.stop()

    async def start_workers(self, num_workers=None):
        if num_workers is None:
            num_workers = config.CONCURRENT_WORKERS
            
        print(f"Starting {num_workers} workers for {self.customer_name}")
        workers = [
            asyncio.create_task(self.consume_messages(i))
            for i in range(num_workers)
        ]
        await asyncio.gather(*workers)

    async def retry_and_store_error_for_analysis(self, msg, worker_id, consumer):
        print("Error processing message")
        # WE HAVE TO IMPLEMENT RETRY LOGIC
        # SET UP ALERT AND INFORM SYSTEM
        # STORE ERROR IN DB, or another queue to retry later
        #Decide if a crytical error or we can continue with other messages
        #Decide if we need to stop the application and notify External system our system is down
        
