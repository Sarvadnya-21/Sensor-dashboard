from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
from typing import List

from . import models, crud, schemas, database, mqtt_service

# Initialize Database
# This creates tables if they don't exist
models.Base.metadata.create_all(bind=database.engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Start MQTT
    mqtt_service.start_mqtt()
    yield
    # Shutdown: Stop MQTT
    mqtt_service.stop_mqtt()

app = FastAPI(title="Sensor Dashboard API", lifespan=lifespan)

# Allow CORS for Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Sensor Dashboard Backend is running"}

@app.get("/data", response_model=List[schemas.SensorReading])
def read_sensor_data(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Fetch recent sensor readings."""
    return crud.get_sensor_readings(db, skip=skip, limit=limit)

@app.get("/alerts", response_model=List[schemas.Alert])
def read_alerts(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    """Fetch generated alerts."""
    return crud.get_alerts(db, skip=skip, limit=limit)

@app.get("/stats")
def read_stats(db: Session = Depends(get_db)):
    """Fetch dashboard statistics."""
    return crud.get_dashboard_stats(db)
