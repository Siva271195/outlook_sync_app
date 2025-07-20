#This starts 2 consumer service for customer A and customer B
import asyncio
from app.consumer_service.customer_a_consumer import CustomerAConsumer
from app.consumer_service.customer_b_consumer import CustomerBConsumer

async def main():
    print("Starting multi-customer sync consumer service to process the stream data")
    customer_a_consumer = CustomerAConsumer()
    customer_b_consumer = CustomerBConsumer()
    await asyncio.gather(
        customer_a_consumer.start_workers(),
        customer_b_consumer.start_workers()
    )

if __name__ == "__main__":
    asyncio.run(main())