# Record-to-Record Synchronization Service

A multi customer data synchronisation service, which transforms internal data changes and delivers it to external data systems in appropriate data formats.

The system is working on python, and utilises Kafka for message queuing, and AWS DynamoDB simulation for data storage.

## Prerequisites

- Python 3.12
- Kafka
- Git

## Setup

1. Clone the repository
2. Create a virtual environment and activate it - `python3 -m venv venv && source venv/bin/activate`
3. Install dependencies - `pip install -r requirements.txt`
4. Download and setup Kafka in your local system. - https://kafka.apache.org/downloads
5. Start the zookeeper and Kafka server on default ports.
6. Create the three required topics

bin/kafka-topics.sh --create --topic users \
  --bootstrap-server localhost:9092 \
  --partitions 3 \
  --replication-factor 1

bin/kafka-topics.sh --create --topic tickets \
  --bootstrap-server localhost:9092 \
  --partitions 3 \
  --replication-factor 1

bin/kafka-topics.sh --create --topic orders \
  --bootstrap-server localhost:9092 \
  --partitions 3 \
  --replication-factor 1


Now you are set to run the system and check functionalities

Option 1.

Run the startup.sh script - `./startup.sh`

This shell script will start 

1. Sync Service API on port 3000 
This is the API to which the internal data changes are sent, via trigger set up in the internal system. Could be via DynamoDB stream or Postgres trigger. [ This will be API Gateway routed to this service ].It pushes all events to a kafka queue.

2. Multi-Customer Consumer Service
This service consumes the events from the kafka queue and transforms the data to the required format and pushes data to Dynamo Db for consumption by External APIs.

3. DynamoDB Polling Service
This service mimics an external API which can poll DynamoDB for data using offset, or can push the data by reading and pushing it to external APIs. The rate limit and fetching from will be handled by this microservice.

4. The system functionality is tested by a python script which sends CRUD event like data to the Sync Service API. You can see the consumption logs by external sevice in logs/polling_service.log.


Option 2.

Individual services can be run as follows

python -m app.sync_service.main &
python -m app.receiver.polling_service &
<!-- python -m app.receiver.external_server & -->
python -m app.consumer_service.multi_customer_service &

And test with Curl commands

  # 2. Insert user
  curl -X POST http://localhost:3000/sync \
    -H "Content-Type: application/json" \
    -d '{"event_type":"INSERT","table":"users","timestamp":"2025-07-19T10:00:00Z","primary_key":{"id":1},"after":{"id":1,"name":"Ash Ketchup","email":"ash.ketchup@pokemon.com","created_at":"2025-07-19T10:00:00Z","updated_at":"2025-07-19T10:00:00Z"}}'

  # 3. Insert ticket  
  curl -X POST http://localhost:3000/sync \
    -H "Content-Type: application/json" \
    -d '{"event_type":"INSERT","table":"tickets","timestamp":"2025-07-19T09:00:00Z","primary_key":{"ticket_id":"TKT-1001"},"after":{"ticket_id":"TKT-1001","title":"Task 1","status":"Open","assignee_id":1,"priority":"High"}}'

  # 4. Insert order (Customer B only)
  curl -X POST http://localhost:3000/sync \
    -H "Content-Type: application/json" \
    -d '{"event_type":"INSERT","table":"orders","timestamp":"2025-07-19T08:00:00Z","primary_key":{"order_id":"ORD-1001"},"after":{"order_id":"ORD-1001","user_id":1,"amount":10,"currency":"USD","status":"pending"}}'


# Run Unit Tests

python -m pytest -v

Major Components in System

sync_service        
REST API for CRUD Trigger events. This will be API Gateway routed to this service. It pushes all events to a kafka queue.

consumer_service      
Kafka consumers which consume events from kafka, transform data and push to DynamoDB

transformers          
Data transformation is achieved here for each customer here, implemented with factory pattern and each customer has its own transformer. Ideally this should be move to dynamic transformers by reading transformation rules from a database as JSON. 

helpers               
Utilities for Kafka and DynamoDB

receiver              
Acts as polling/push service for external APIs

schemas
Schemas for input and output validation 
internal     ->         # Input validation schemas
external     ->         # Output validation schemas
validation   ->         # Schema validator

tests                   
Unit tests

requirements.txt           
Python dependencies  
startup.sh  
startup script


test_populate.py           
System test via api

SYSTEM_DESIGN.pdf
Architecture documentation






