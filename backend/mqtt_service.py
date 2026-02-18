import paho.mqtt.client as mqtt
import json
from sqlalchemy.orm import Session
from .database import SessionLocal
from . import crud, schemas

# Thresholds Configuration
# If a sensor value exceeds these limits, an alert is triggered.
THRESHOLDS = {
    "temperature": 30.0,
    "humidity": 80.0,
    "voltage": 240.0,
    "current": 15.0,
    "pressure": 1100.0
}

MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_TOPIC = "sensors/+"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe(MQTT_TOPIC)
    else:
        print(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    try:
        payload_str = msg.payload.decode()
        # print(f"Received: {payload_str} on {msg.topic}") # Debug logging
        
        try:
            payload = json.loads(payload_str)
        except json.JSONDecodeError:
            print("Received non-JSON message")
            return

        topic = msg.topic
        
        # Open DB Session
        db = SessionLocal()
        
        # 1. Store Raw Data
        sensor_reading = schemas.SensorReadingCreate(
            topic=topic,
            temperature=payload.get("temperature"),
            humidity=payload.get("humidity"),
            voltage=payload.get("voltage"),
            current=payload.get("current"),
            pressure=payload.get("pressure"),
            raw_payload=payload
        )
        crud.create_sensor_reading(db, sensor_reading)
        
        # 2. Check Thresholds & Generate Alerts
        for key, value in payload.items():
            if key in THRESHOLDS and isinstance(value, (int, float)):
                limit = THRESHOLDS[key]
                if value > limit:
                    alert_msg = f"{key} value {value} exceeded threshold {limit}"
                    print(f"ALERT: {alert_msg}")
                    
                    alert = schemas.AlertCreate(
                        topic=topic,
                        violated_key=key,
                        actual_value=float(value),
                        threshold_value=float(limit),
                        message=alert_msg
                    )
                    crud.create_alert(db, alert)
        
        db.close()
        
    except Exception as e:
        print(f"Error processing MQTT message: {e}")

# Initialize Client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

def start_mqtt():
    try:
        print(f"Connecting to MQTT broker {MQTT_BROKER}...")
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()
    except Exception as e:
        print(f"Error starting MQTT client: {e}")

def stop_mqtt():
    client.loop_stop()
