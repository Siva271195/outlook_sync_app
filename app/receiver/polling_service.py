#This is a mock polling/pushing service to poll messages from DynamoDB and push them to external services
# We can also write this as a consumer to read new event data and push it to external services
# RATE LIMIT AND FETCHING FROM LAST OFFSET NEED TO BE HANDLED BY THIS MICROSERVICE
import asyncio
from app.helpers.mock_dynamodb_client import mock_dynamodb_client
from app.RateLimitterService.LeakyBucket import LeakyBucket

# refresh every 3 second
leaky_bucket = LeakyBucket(capacity=3, refresh_rate=3)  

CUSTOMER_A_INTERVAL = 1   
CUSTOMER_A_BATCH_SIZE = 5

CUSTOMER_B_INTERVAL = 15  
CUSTOMER_B_BATCH_SIZE = 10

async def poll_customer_a():
    customer_name = "customer-a"
    last_offset = 0
    
    while True:
        try:
            # print("Fetch customer-a messages...")
            messages = await mock_dynamodb_client.get_pending_messages(
                customer_name=customer_name,
                start_offset=last_offset,
                limit=CUSTOMER_A_BATCH_SIZE
            )
            # print(messages)
            item_count, success = leaky_bucket.add(messages)
            print(f" Attempted: {len(messages)} , item accessed: {item_count} , Success: {success} , Current Capacity: {leaky_bucket.get_current_capacity()}")
            
            if not success:
                print("Bucket full skip record")
                await asyncio.sleep(CUSTOMER_A_INTERVAL)
                continue
            i=0
            while(i<item_count):
                message = messages[i]
                offset = message['offset']
                table = message['table']
                data = message['transformedData']
                print(f"Printing data Offset {offset} | Table: {table} | Data: {data}")
                last_offset = max(last_offset, offset)
                i+=1
            await asyncio.sleep(CUSTOMER_A_INTERVAL)
            
        except Exception as e:
            print("error in polling", e)
            await asyncio.sleep(CUSTOMER_A_INTERVAL)

async def poll_customer_b():
    customer_name = "customer-b"
    last_offset = 0
    
    while True:
        try:
            print("Fetch customer-b messages...")
            messages = await mock_dynamodb_client.get_pending_messages(
                customer_name=customer_name,
                start_offset=last_offset,
                limit=CUSTOMER_B_BATCH_SIZE
            )
            # print(messages)
            if messages:
                print(f"\n=== CUSTOMER B - Found {len(messages)} messages ===")
                for message in messages:
                    offset = message['offset']
                    table = message['table']
                    data = message['transformedData']
                    
                    print(f"Offset {offset} | Table: {table} | Data: {data}")
                    last_offset = max(last_offset, offset)
            
            await asyncio.sleep(CUSTOMER_B_INTERVAL)
            
        except Exception as e:
            print("error in polling", e)
            await asyncio.sleep(CUSTOMER_B_INTERVAL)

async def main():
    print("Starting DynamoDB Polling/Pushing Service")
    print(f"Customer A: {CUSTOMER_A_INTERVAL}s interval, {CUSTOMER_A_BATCH_SIZE} records")
    await asyncio.gather(
        poll_customer_a()
    )

if __name__ == "__main__":
    asyncio.run(main())