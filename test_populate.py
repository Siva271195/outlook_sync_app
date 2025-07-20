#!/usr/bin/env python3
import requests
import json
import time

SYNC_API_URL = "http://localhost:3000/sync"

# Test data
test_data = [
    # Users
    {
        "event_type": "INSERT",
        "table": "users",
        "timestamp": "2025-07-19T10:00:00Z",
        "primary_key": {"id": 1},
        "after": {
            "id": 1,
            "name": "Ash Ketchup",
            "email": "ash.ketchup@pokemon.com"
        }
    },
    {
        "event_type": "INSERT",
        "table": "users",
        "timestamp": "2025-07-19T10:05:00Z",
        "primary_key": {"id": 2},
        "after": {
            "id": 2,
            "name": "Misty",
            "email": "misty@pokemon.com"
        }
    },
    {
        "event_type": "UPDATE",
        "table": "users",
        "timestamp": "2025-07-19T11:00:00Z",
        "primary_key": {"id": 1},
        "before": {
            "name": "Ash Ketchup",
            "email": "ash.ketchup@pokemon.com"
        },
        "after": {
            "id": 1,
            "name": "Ash Ketchup MAX",
            "email": "ash.ketchup.max@pokemon.com"
        }
    },
    # Tickets
    {
        "event_type": "INSERT",
        "table": "tickets",
        "timestamp": "2025-07-19T09:00:00Z",
        "primary_key": {"ticket_id": "TKT-1001"},
        "after": {
            "ticket_id": "TKT-1001",
            "title": "Task 1",
            "status": "Open",
            "assignee_id": 1,
            "priority": "High"
        }
    },
    {
        "event_type": "UPDATE",
        "table": "tickets",
        "timestamp": "2025-07-19T14:00:00Z",
        "primary_key": {"ticket_id": "TKT-1001"},
        "before": {
            "ticket_id": "TKT-1001",
            "title": "Task 1",
            "status": "Open",
            "assignee_id": 1,
            "priority": "High"
        },
        "after": {
            "ticket_id": "TKT-1001",
            "title": "Task 1",
            "status": "In Progress",
            "assignee_id": 2,
            "priority": "High"
        }
    },
    # Orders
    {
        "event_type": "INSERT",
        "table": "orders",
        "timestamp": "2025-07-19T08:00:00Z",
        "primary_key": {"order_id": "ORD-1001"},
        "after": {
            "order_id": "ORD-1001",
            "user_id": 1,
            "amount": 10,
            "currency": "USD",
            "status": "pending"
        }
    },
    {
        "event_type": "UPDATE",
        "table": "orders",
        "timestamp": "2025-07-19T10:00:00Z",
        "primary_key": {"order_id": "ORD-1001"},
        "before": {
            "order_id": "ORD-1001",
            "user_id": 1,
            "amount": 10,
            "currency": "USD",
            "status": "pending"
        },
        "after": {
            "order_id": "ORD-1001",
            "user_id": 1,
            "amount": 10,
            "currency": "USD",
            "status": "paid"
        }
    }
]

def main():
    print("Sending test data...")
    time.sleep(5)
    
    for i, data in enumerate(test_data, 1):
        table = data["table"] 
        event = data["event_type"]
        print(f"Sending {i}: {table} {event}")
        
        try:
            resp = requests.post(SYNC_API_URL, json=data)
            print(f"Response: {resp.status_code}")
        except Exception as e:
            print(f"Failed: {e}")
        
        time.sleep(1)
    
    print("Done!")

if __name__ == "__main__":
    main()