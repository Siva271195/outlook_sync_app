import os

# project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"

# DynamoDB
ENVIRONMENT = os.environ.get('ENV', 'local')
DYNAMODB_ENDPOINT = 'http://localhost:4566' 
AWS_REGION = 'us-east-1'
AWS_ACCESS_KEY = 'test' 
AWS_SECRET_KEY = 'test' 
SYNC_TOPIC = "sync-request-topic"
DEST_TOPIC = "destination-topic"
WEBHOOK_URL = "http://localhost:8000/webhook"
CONCURRENT_WORKERS = 1
CONSUMER_GROUP_ID = "sync-service-group"

# Customer specific configurations
CUSTOMER_A = {
    "name": "customer_a",
    "topics": ["users", "tickets"],
    "consumer_group": "customer-a-group",
    "transformer": "transformer_service1",
    "webhook_url": "http://localhost:8000/customer-a/webhook"
}

CUSTOMER_B = {
    "name": "customer_b", 
    "topics": ["users", "tickets", "orders"],
    "consumer_group": "customer-b-group",
    "transformer": "transformer_service2",
    "webhook_url": "http://localhost:8000/customer-b/webhook"
}