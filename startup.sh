#!/bin/bash
source venv/bin/activate

rm -rf logs
mkdir -p logs

echo "Multi-Customer Kafka Sync Service"
echo "============================================"
echo ""
echo "PREREQUISITES:"
echo "1. Install dependencies: pip install -r requirements.txt"
echo "2. Kafka must be running on localhost:9092"
echo "3. Create these Kafka topics:"
echo "   kafka-topics --create --topic users --bootstrap-server localhost:9092"
echo "   kafka-topics --create --topic tickets --bootstrap-server localhost:9092" 
echo "   kafka-topics --create --topic orders --bootstrap-server localhost:9092"
echo ""
echo "Starting services..."

echo "Starting Sync Service API on port 3000..."
python -m app.sync_service.main > logs/sync_service.log 2>&1 &
SYNC_PID=$!

echo "Starting DynamoDB Polling Service..."
python -m app.receiver.polling_service > logs/polling_service.log 2>&1 &
POLLING_PID=$!

sleep 2

echo "Starting Multi-Customer Consumer Service..."
python -m app.consumer_service.multi_customer_service > logs/consumers.log 2>&1 &
CONSUMER_PID=$!

echo "All services started:"
echo "Sync Service API (PID: $SYNC_PID)"
echo "DynamoDB Polling Service (PID: $POLLING_PID)"
echo "Multi-Customer Consumers (PID: $CONSUMER_PID)"
echo ""
echo "Monitor logs:"
echo "Sync Service: tail -f logs/sync_service.log"
echo "Consumers: tail -f logs/consumers.log"
echo "Polling Service: tail -f logs/polling_service.log"
echo ""
echo "Check DynamoDB Tables:"
echo " CMD : cat /tmp/dynamodb.json"
echo ""
echo "Populating test data..."
python test_populate.py &
POPULATE_PID=$!

echo ""
echo "Press Ctrl+C to stop all services"

cleanup() {
    echo "Stopping all services..."
    kill $SYNC_PID $POLLING_PID $CONSUMER_PID $POPULATE_PID 2>/dev/null
    echo "Services stopped"
    exit
}

# Set trap to cleanup on script exit
trap cleanup INT TERM

# Wait for all processes
wait $SYNC_PID $POLLING_PID $CONSUMER_PID