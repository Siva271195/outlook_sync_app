import pytest
from datetime import datetime
from app.transformers.transform_factory import TransformFactory
from app.transformers import transformer_service1, transformer_service2


class TestCustomerATransformer:
    
    def test_user_insert_transformation(self):
        input_data = {
            "event_type": "INSERT",
            "table": "users",
            "after": {
                "id": 1,
                "name": "Ash Ketchup",
                "email": "ash@pokemon.com"
            }
        }
        
        result = TransformFactory.transform_message("transformer_service1", input_data)
        
        assert result["id"] == 1
        assert result["fullName"] == "Ash Ketchup"
        assert result["email"] == "ash@pokemon.com"
        assert result["status"] == "active"
        assert result["consumer"] == "customer_A"
        assert "processedAt" in result
    

    def test_ticket_transformation(self):
        input_data = {
            "event_type": "INSERT",
            "table": "tickets",
            "after": {
                "ticket_id": "TKT-001",
                "title": "Test Ticket",
                "status": "Open",
                "assignee_id": 123
            }
        }
        
        result = TransformFactory.transform_message("transformer_service1", input_data)
        
        assert result["ticketId"] == "TKT-001"
        assert result["title"] == "Test Ticket" 
        assert result["status"] == "Open"
        assert result["assignee"] == 123
        assert result["consumer"] == "customer_A"
    
    def test_unsupported_table_raises_error(self):
        input_data = {
            "event_type": "INSERT",
            "table": "unsupported_table",
            "after": {"id": 1}
        }
        
        with pytest.raises(ValueError, match="Customer A does not support table type"):
            TransformFactory.transform_message("transformer_service1", input_data)


class TestCustomerBTransformer:
    
    def test_user_transformation(self):
        input_data = {
            "event_type": "INSERT",
            "table": "users",
            "after": {
                "id": 100,
                "name": "Pikachu",
                "email": "pikachu@pokemon.com",
                "state": "active"
            }
        }
        
        result = TransformFactory.transform_message("transformer_service2", input_data)
        
        assert result["type"] == "user"
        assert result["userId"] == 100
        assert result["fullName"] == "Pikachu"
        assert result["email"] == "pikachu@pokemon.com"
        assert result["isActive"] is True  # state "active" -> True
        assert result["consumer"] == "customer_B"
    
    def test_ticket_transformation(self):
        input_data = {
            "event_type": "INSERT",
            "table": "tickets",
            "after": {
                "ticket_id": "TKT-002",
                "title": "Customer B Ticket",
                "status": "In Progress",
                "priority": "High",
                "assignee_id": 456
            }
        }
        
        result = TransformFactory.transform_message("transformer_service2", input_data)
        
        assert result["type"] == "ticket"
        assert result["id"] == "TKT-002"
        assert result["title"] == "Customer B Ticket"
        assert result["status"] == "In Progress"
        assert result["priorityLevel"] == "High"
        assert result["assigneeId"] == 456
        assert result["consumer"] == "customer_B"
    
    def test_order_transformation(self):
        """Test order transformation for Customer B"""
        input_data = {
            "event_type": "INSERT",
            "table": "orders",
            "primary_key": {"order_id": "ORD-123"},
            "after": {
                "user_id": 789,
                "amount": "99.99",
                "currency": "EUR",
                "status": "paid"
            }
        }
        
        result = TransformFactory.transform_message("transformer_service2", input_data)
        
        assert result["type"] == "order"
        assert result["orderId"] == "ORD-123"  # from primary_key
        assert result["userId"] == 789
        assert result["amount"] == 99.99  # converted to float
        assert result["currency"] == "EUR"
        assert result["status"] == "paid"
        assert result["consumer"] == "customer_B"