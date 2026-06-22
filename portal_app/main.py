from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import uvicorn
from typing import List, Optional
import random
import sqlite3
import httpx
from pathlib import Path

app = FastAPI(title="Industrial Vehicle Portal")

DB_PATH = Path("vehicles.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vehicles (
            id TEXT PRIMARY KEY,
            vin TEXT NOT NULL,
            make TEXT,
            model TEXT,
            year TEXT,
            owner TEXT,
            lat REAL,
            lng REAL
        )
    ''')
    # Seed data for testing if empty
    cursor.execute('SELECT COUNT(*) FROM vehicles')
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO vehicles (id, vin, make, model, year, owner, lat, lng)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', ("TEST-VEHICLE-001", "VIN-001", "Tesla", "Model S", "2024", "Demo", 52.5200, 13.4050))
        cursor.execute('''
            INSERT INTO vehicles (id, vin, make, model, year, owner, lat, lng)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', ("TEST-VEHICLE-002", "VIN-002", "Tesla", "Model X", "2024", "Demo", 48.8566, 2.3522))
    
    conn.commit()
    conn.close()

init_db()

class VehicleCreate(BaseModel):
    vin: str
    owner: str

async def decode_vin(vin: str):
    """Call NHTSA API to decode VIN"""
    url = f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVin/{vin}?format=json"
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(url, timeout=10.0)
            data = resp.json()
            results = data.get("Results", [])
            
            info = {"make": "Unknown", "model": "Unknown", "year": "Unknown"}
            for item in results:
                variable = item.get("Variable")
                value = item.get("Value")
                if variable == "Make": info["make"] = value
                elif variable == "Model": info["model"] = value
                elif variable == "Model Year": info["year"] = value
            return info
        except Exception as e:
            print(f"NHTSA API Error: {e}")
            return None

@app.post("/api/register")
async def register_vehicle(vehicle: VehicleCreate):
    # Decode VIN using real API
    details = await decode_vin(vehicle.vin)
    
    new_id = f"V-{random.randint(1000, 9999)}"
    make = details["make"] if details else "Unknown"
    model = details["model"] if details else "Unknown"
    year = details["year"] if details else "Unknown"
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO vehicles (id, vin, make, model, year, owner, lat, lng)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (new_id, vehicle.vin, make, model, year, vehicle.owner, 52.5200, 13.4050))
    conn.commit()
    conn.close()
    
    return {"message": "Success", "vehicle": {"id": new_id, "make": make, "model": model}}

@app.get("/api/vehicles")
async def get_vehicles():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM vehicles')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.get("/api/gps/{vehicle_id}")
async def get_gps(vehicle_id: str):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM vehicles WHERE id = ?', (vehicle_id,))
    v = cursor.fetchone()
    
    if v:
        v = dict(v)
        # Simulate movement and update DB
        new_lat = v["lat"] + (random.random() - 0.5) * 0.005
        new_lng = v["lng"] + (random.random() - 0.5) * 0.005
        cursor.execute('UPDATE vehicles SET lat = ?, lng = ? WHERE id = ?', (new_lat, new_lng, vehicle_id))
        conn.commit()
        conn.close()
        return {"lat": round(new_lat, 4), "lng": round(new_lng, 4)}
    
    conn.close()
    return JSONResponse(status_code=404, content={"message": "Vehicle not found"})

# Serve static files
app.mount("/", StaticFiles(directory="portal_app/static", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
