# MIMIC EXTERNAL API
from fastapi import FastAPI, Request
import uvicorn
import json
from app.helpers import kafka_client

app = FastAPI()

@app.post("/customer-a/webhook")
async def customer_a_webhook(request: Request):
    payload = await request.json()
    print("CUSTOMER A received:", payload)
    return {"status": "ok"}

@app.post("/customer-b/webhook") 
async def customer_b_webhook(request: Request):
    payload = await request.json()
    print("CUSTOMER B received:", payload)
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)