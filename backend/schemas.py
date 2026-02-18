from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class SensorReadingBase(BaseModel):
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    voltage: Optional[float] = None
    current: Optional[float] = None
    pressure: Optional[float] = None

class SensorReadingCreate(SensorReadingBase):
    topic: str
    raw_payload: Optional[Dict[str, Any]] = None

class SensorReading(SensorReadingBase):
    id: int
    timestamp: datetime
    topic: str

    class Config:
        from_attributes = True

class AlertBase(BaseModel):
    topic: str
    violated_key: str
    actual_value: float
    threshold_value: float
    message: str

class AlertCreate(AlertBase):
    pass

class Alert(AlertBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

class DashboardStats(BaseModel):
    total_messages: int
    active_alerts_count: int
    latest_readings: Dict[str, Any] # Simple key-value of latest data per topic
