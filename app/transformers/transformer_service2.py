import os
from datetime import datetime
from schemas.validation.schema_validator import validate_against_schema
from app import config

schema_path = config.PROJECT_ROOT + "/schemas/external/customer-b/"

def transform_user(record):
    transformed = {
        "type": "user",
        "userId": record.get("id"),
        "fullName": record.get("name", ""),
        "email": record.get("email"),
        "isActive": record.get("state", "active") == "active",
        "consumer": "customer_B",
        "processedAt": datetime.now().isoformat()
    }
    
    return transformed

def transform_ticket(record):
    transformed = {
        "type": "ticket",
        "id": record.get("ticket_id"),
        "title": record.get("title"),
        "status": record.get("status"),
        "priorityLevel": record.get("priority", "Medium"),
        "assigneeId": record.get("assignee_id"),
        "consumer": "customer_B",
        "processedAt": datetime.now().isoformat()
    }
    
    return transformed

def transform_order(record):
    # Handle case where primary_key might be None
    primary_key = record.get("primary_key") or {}
    
    transformed = {
        "type": "order",
        "orderId": primary_key.get("order_id"),
        "userId": record.get("user_id"),
        "amount": float(record.get("amount", 0)),
        "currency": record.get("currency", "USD"),
        "status": record.get("status", "pending"),
        "placedAt": None,
        "consumer": "customer_B",
        "processedAt": datetime.now().isoformat()
    }
    
    return transformed

def to_external(record):
    # Extract data based on event type and table
    table = record.get("table")
    event_type = record.get("event_type")
    full_schema_path = schema_path+table+".json"
    # Get the actual data from 'after' field for INSERT/UPDATE, 'before' for DELETE
    if event_type in ["INSERT", "UPDATE"] and "after" in record:
        data = record["after"]
    elif event_type == "DELETE" and "before" in record:
        data = record["before"]
    else:
        # Fallback to direct record data
        data = record
    
    # Add table type to data for transformation
    data["type"] = table
    # Pass primary_key for orders
    if "primary_key" in record:
        data["primary_key"] = record["primary_key"]
    
    if table == "users":
        transformed = transform_user(data)
    elif table == "tickets":
        transformed = transform_ticket(data)
    elif table == "orders":
        transformed = transform_order(data)
    else:
        raise ValueError(f"Unsupported table type: {table}")
    
    is_valid, error_msg = validate_against_schema(full_schema_path, transformed)
    
    if not is_valid:
        raise ValueError(f"Output validation failed for customer-b {table}: {error_msg}")
    
    return transformed
