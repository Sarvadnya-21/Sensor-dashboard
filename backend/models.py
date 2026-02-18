from sqlalchemy import Column, Integer, Float, String, DateTime, JSON
from sqlalchemy.sql import func
from .database import Base

class SensorData(Base):
    __tablename__ = "sensor_data"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    topic = Column(String(255), index=True)
    # Store individual sensor values as columns for easier querying/indexing if needed
    # Or keep as JSON if schema is flexible. 
    # Current requirement: 5 key-value parameters. 
    # Let's be explicit but also flexible.
    temperature = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)
    voltage = Column(Float, nullable=True)
    current = Column(Float, nullable=True)
    pressure = Column(Float, nullable=True)
    
    # Store raw full payload just in case
    raw_payload = Column(JSON)

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    topic = Column(String(255), index=True)
    violated_key = Column(String(50)) # e.g., "temperature"
    actual_value = Column(Float)
    threshold_value = Column(Float)
    message = Column(String(255))
