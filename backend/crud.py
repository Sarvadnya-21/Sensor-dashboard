from sqlalchemy.orm import Session
from sqlalchemy import desc
from . import models, schemas
import json

def create_sensor_reading(db: Session, reading: schemas.SensorReadingCreate):
    db_reading = models.SensorData(
        topic=reading.topic,
        temperature=reading.temperature,
        humidity=reading.humidity,
        voltage=reading.voltage,
        current=reading.current,
        pressure=reading.pressure,
        raw_payload=reading.raw_payload
    )
    db.add(db_reading)
    db.commit()
    db.refresh(db_reading)
    return db_reading

def get_sensor_readings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.SensorData).order_by(desc(models.SensorData.timestamp)).offset(skip).limit(limit).all()

def create_alert(db: Session, alert: schemas.AlertCreate):
    db_alert = models.Alert(
        topic=alert.topic,
        violated_key=alert.violated_key,
        actual_value=alert.actual_value,
        threshold_value=alert.threshold_value,
        message=alert.message
    )
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert

def get_alerts(db: Session, skip: int = 0, limit: int = 50):
    return db.query(models.Alert).order_by(desc(models.Alert.timestamp)).offset(skip).limit(limit).all()

def get_dashboard_stats(db: Session):
    total_messages = db.query(models.SensorData).count()
    total_alerts = db.query(models.Alert).count() # Or active alerts if we had a status
    
    # Get latest reading for each distinct topic is complex in standard SQL without logic
    # Simplified: Get global latest reading
    latest = db.query(models.SensorData).order_by(desc(models.SensorData.timestamp)).first()
    
    latest_data = {}
    if latest:
        latest_data = {
            "topic": latest.topic,
            "timestamp": latest.timestamp,
            "values": latest.raw_payload
        }

    return {
        "total_messages": total_messages,
        "active_alerts_count": total_alerts, 
        "latest_readings": latest_data
    }
