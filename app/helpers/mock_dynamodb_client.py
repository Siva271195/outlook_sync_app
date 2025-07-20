import json
import os
from datetime import datetime
from typing import Dict, List, Any


class MockDynamoDBClient:
    def __init__(self):
        self.data_file = '/tmp/mock_dynamodb_data.json'
        self.load_data()

    def load_data(self):
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.tables = data.get('tables', {
                        'sync-service-customer-a': {},
                        'sync-service-customer-b': {}
                    })
                    self.counters = data.get('counters', {
                        'customer-a': 0,
                        'customer-b': 0
                    })
                    for table_name in self.tables:
                        self.tables[table_name] = {int(k): v for k, v in self.tables[table_name].items()}
            else:
                self.tables = {
                    'sync-service-customer-a': {},
                    'sync-service-customer-b': {}
                }
                self.counters = {
                    'customer-a': 0,
                    'customer-b': 0
                }
        except Exception as e:
            print(f"Error with Dynamo DB: {e}")

    def save_data(self):
        try:
            data = {
                'tables': self.tables,
                'counters': self.counters
            }
            with open(self.data_file, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Error with Dynamo DB: {e}")
            
    def get_table_name(self, customer_name: str):
        return f"sync-service-{customer_name}"
    
    def get_next_offset(self, customer_id: str):
        self.counters[customer_id] += 1
        return self.counters[customer_id]
    
    async def store_message(self, customer_name: str, table: str, message_id: str, transformed_data: dict) -> bool:
        try:
            table_name = self.get_table_name(customer_name)
            offset = self.get_next_offset(customer_name)
            item = {
                'offset': offset,
                'messageId': message_id,
                'customerId': customer_name,
                'table': table,
                'transformedData': transformed_data,
                'status': 'pending',
                'attempts': 0,
                'createdAt': datetime.utcnow().isoformat(),
                'updatedAt': datetime.utcnow().isoformat(),
                'errorMessage': None
            }
            self.tables[table_name][offset] = item
            self.save_data() 
            print("Table contents ---table_name", table_name, "  ",self.tables[table_name])
            return True
            
        except Exception as e:
            print("error in dynamoDB", e)
            return False
    
    async def get_pending_messages(self, customer_name: str, start_offset: int = 0, limit: int = 50):
        try:
            self.load_data() 
            table_name = self.get_table_name(customer_name)
            table_data = self.tables.get(table_name, {})
            print(f"{customer_name} has {len(table_data)} total messages, start_offset={start_offset}")
            pending_messages = []
            for offset, item in sorted(table_data.items()):
                if offset > start_offset and item['status'] == 'pending':
                    pending_messages.append(item)
                    if len(pending_messages) >= limit:
                        break
            print(f" {len(pending_messages)} pending messages for {customer_name}")
            return pending_messages
            
        except Exception as e:
            print("error in dynamoDB", e)
            return []
    
    async def update_message_status(self, customer_name: str, offset: int, status: str, error_message: str = None, attempts: int = None):
        try:
            #Need to implement update and fetch new data
            return True
        except Exception as e:
            print(f"Mock error updating message status for {customer_name}: {e}")
            return False

mock_dynamodb_client = MockDynamoDBClient()