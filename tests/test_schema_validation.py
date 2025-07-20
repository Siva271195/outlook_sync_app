
import pytest
import os
from schemas.validation.schema_validator import validate_against_schema
from app import config


class TestSchemaValidation:
    
    def test_valid_customer_a_user_schema(self):
        schema_path = f"{config.PROJECT_ROOT}/schemas/external/customer-a/users.json"
        
        valid_data = {
            "id": 1,
            "fullName": "Test User",
            "email": "test@example.com",
            "status": "active",
            "consumer": "customer_A",
            "processedAt": "2025-07-20T10:00:00"
        }
        
        is_valid, error_msg = validate_against_schema(schema_path, valid_data)
        
        assert is_valid is True
        assert error_msg is None
    
    def test_invalid_customer_a_user_schema(self):
        schema_path = f"{config.PROJECT_ROOT}/schemas/external/customer-a/users.json"
        
        invalid_data = {
            "fullName": "Test User",
            "email": "test@example.com",
            "status": "active",
            "consumer": "customer_A",
            "processedAt": "2025-07-20T10:00:00"
        }
        
        is_valid, error_msg = validate_against_schema(schema_path, invalid_data)
        
        assert is_valid is False
        assert error_msg is not None
        assert "'id' is a required property" in error_msg
    
    def test_valid_customer_b_user_schema(self):
        schema_path = f"{config.PROJECT_ROOT}/schemas/external/customer-b/users.json"
        
        valid_data = {
            "type": "user",
            "userId": 100,
            "fullName": "Customer B User",
            "email": "userb@example.com",
            "isActive": True,
            "consumer": "customer_B",
            "processedAt": "2025-07-20T10:00:00"
        }
        
        is_valid, error_msg = validate_against_schema(schema_path, valid_data)
        
        assert is_valid is True
        assert error_msg is None
    
    def test_valid_customer_a_ticket_schema(self):
        schema_path = f"{config.PROJECT_ROOT}/schemas/external/customer-a/tickets.json"
        
        valid_data = {
            "ticketId": "TKT-001",
            "title": "Test Ticket",
            "status": "Open",
            "assignee": 123,
            "consumer": "customer_A",
            "processedAt": "2025-07-20T10:00:00"
        }
        
        is_valid, error_msg = validate_against_schema(schema_path, valid_data)
        
        assert is_valid is True
        assert error_msg is None
    
    def test_valid_customer_b_order_schema(self):
        schema_path = f"{config.PROJECT_ROOT}/schemas/external/customer-b/orders.json"
        
        valid_data = {
            "type": "order",
            "orderId": "ORD-001", 
            "userId": 456,
            "amount": 99.99,
            "currency": "USD",
            "status": "paid",
            "placedAt": None,
            "consumer": "customer_B",
            "processedAt": "2025-07-20T10:00:00"
        }
        
        is_valid, error_msg = validate_against_schema(schema_path, valid_data)
        
        assert is_valid is True
        assert error_msg is None
    
    def test_nonexistent_schema_file(self):
        schema_path = "/path/to/nonexistent/schema.json"
        
        test_data = {"id": 1}
        is_valid, error_msg = validate_against_schema(schema_path, test_data)
        
        assert is_valid is False
        assert error_msg is not None
        assert "Schema file not found" in error_msg
    
    def test_valid_internal_user_schema(self):
        """Test valid internal user data passes validation"""
        schema_path = f"{config.PROJECT_ROOT}/schemas/internal/users.json"
        
        valid_data = {
            "event_type": "INSERT",
            "table": "users",
            "timestamp": "2025-07-20T10:00:00Z",
            "primary_key": {"id": 1},
            "after": {
                "id": 1,
                "name": "Test User",
                "email": "test@example.com"
            }
        }
        
        is_valid, error_msg = validate_against_schema(schema_path, valid_data)
        
        assert is_valid is True
        assert error_msg is None   