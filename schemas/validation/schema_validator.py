import json
import os
from jsonschema import validate, ValidationError

def validate_against_schema(schema_path: str, data: dict):
    try:
        with open(schema_path, 'r') as f:
            schema = json.load(f)
        validate(instance=data, schema=schema)
        return True, None
    except FileNotFoundError:
        error_msg = f"Schema file not found: {schema_path}"
        return False, error_msg
    except json.JSONDecodeError as e:
        error_msg = f"Invalid JSON in schema file {schema_path}: {e}"
        return False, error_msg
    except ValidationError as e:
        error_msg = f"Validation failed: {e.message}"
        return False, error_msg
    except Exception as e:
        error_msg = f"Unexpected error during validation: {str(e)}"
        return False, error_msg