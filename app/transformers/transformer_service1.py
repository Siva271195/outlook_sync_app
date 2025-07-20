import os
from datetime import datetime
from schemas.validation.schema_validator import validate_against_schema
from app import config

schema_path = config.PROJECT_ROOT + "/schemas/external/customer-a/"

def to_external(record):
    table = record.get("table")
    event_type = record.get("event_type")
    
    if event_type in ["INSERT", "UPDATE"] and "after" in record:
        data = record["after"]
    elif event_type == "DELETE" and "before" in record:
        data = record["before"]
    else:
        data = record
    full_schema_path = schema_path+table+".json"
    if table == "users":
        transformed = transform_user(data)
    elif table == "tickets":
        transformed = transform_ticket(data)
    else:
        raise ValueError(f"Customer A does not support table type: {table}")
    
    is_valid, error_msg = validate_against_schema(full_schema_path, transformed)
    
    if not is_valid:
        raise ValueError(f"Output validation failed for customer-a {table}: {error_msg}")
    
    return transformed
 

def transform_user(record):
    transformed = {
        "id": record.get("id"),
        "fullName": record.get("name", ""),
        "email": record.get("email"),
        "status": "active",
        "consumer": "customer_A",
        "processedAt": datetime.now().isoformat()
    }
    return transformed

def transform_ticket(record):
    transformed = {
        "ticketId": record.get("ticket_id"),
        "title": record.get("title"),
        "status": record.get("status"),
        "assignee": record.get("assignee_id"),
        "consumer": "customer_A",
        "processedAt": datetime.now().isoformat()
    }
    return transformed