import asyncio
from app.consumer_service.base_consumer import BaseConsumer
from app import config

class CustomerAConsumer(BaseConsumer):
    def __init__(self):
        super().__init__(config.CUSTOMER_A, "customer-a")

# async def start():
#     consumer = CustomerAConsumer()
#     await consumer.start_workers()

# if __name__ == "__main__":
#     asyncio.run(start())