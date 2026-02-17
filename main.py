from fastapi import FastAPI
from pydantic import BaseModel
import json
from datetime import datetime

app = FastAPI()

DB_FILE = "database.json"

class LicenseRequest(BaseModel):
    client_id: str
    license_key: str

def load_db():
    with open(DB_FILE) as f:
        return json.load(f)

@app.post("/validate")
def validate_license(req: LicenseRequest):

    db = load_db()

    if req.client_id not in db:
        return {"valid": False, "reason": "unknown_client"}

    client = db[req.client_id]

    if client["license_key"] != req.license_key:
        return {"valid": False, "reason": "invalid_key"}

    if client["status"] != "active":
        return {"valid": False, "reason": "suspended"}

    return {"valid": True}
