import asyncio
from app.consumer_service.base_consumer import BaseConsumer
from app import config

class CustomerBConsumer(BaseConsumer):
    def __init__(self):
        super().__init__(config.CUSTOMER_B, "customer-b")