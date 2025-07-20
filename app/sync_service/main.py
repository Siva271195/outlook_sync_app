# THIS IS THE REST API TO BE CONFIGURED WITH TRIGGERS FROM DB

from fastapi import FastAPI, Request, HTTPException
import uvicorn
import json
import os
from app.helpers import kafka_client
from schemas.validation.schema_validator import validate_against_schema
from app import config

app = FastAPI()
schema_path = config.PROJECT_ROOT+"/schemas/internal/"

@app.post("/sync")
async def sync_data(request: Request):
    payload = await request.json()
    print("Sync API received:", json.dumps(payload, indent=2))
    
    table = payload.get("table")
    if not table:
        raise HTTPException(status_code=400, detail="Missing table field")
    
    # Validate payload against internal schema
    is_valid, error_msg = validate_against_schema(schema_path+table+".json", payload)
    
    if not is_valid:
        raise HTTPException(status_code=400, detail=f"Schema validation failed: {error_msg}")
    
    try:
        await kafka_client.send_message(table, payload)
        print(f"Published to topic '{table}': {payload.get('event_type')} for {payload.get('primary_key')}")
        return {"status": "published", "topic": table, "message": "Data sent to Kafka successfully"}
    except Exception as e:
        print(f"Error publishing to Kafka: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to publish to Kafka: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "sync-service"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)