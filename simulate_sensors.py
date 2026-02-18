import paho.mqtt.client as mqtt
import time
import random
import json

BROKER = "test.mosquitto.org"
TOPIC_BASE = "sensors"

SENSORS = ["device_01", "device_02", "device_03"]

def generate_data(device_id):
    # Occasionally generate a spike to trigger alerts
    temp_spike = random.choice([0, 0, 0, 10]) # 1 in 4 chance of spike addition
    volt_spike = random.choice([0, 0, 0, 0, 50])
    
    return {
        "temperature": round(random.uniform(20.0, 30.0) + temp_spike, 2),
        "humidity": round(random.uniform(40.0, 90.0), 2),
        "voltage": round(random.uniform(220.0, 240.0) + volt_spike, 2),
        "current": round(random.uniform(1.0, 5.0), 2),
        "pressure": round(random.uniform(980.0, 1020.0), 2)
    }

def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    print(f"Connecting to {BROKER}...")
    client.connect(BROKER, 1883, 60)
    
    try:
        while True:
            for device in SENSORS:
                topic = f"{TOPIC_BASE}/{device}"
                payload = generate_data(device)
                
                print(f"Publishing to {topic}: {payload}")
                client.publish(topic, json.dumps(payload))
                
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("Simulation stopped.")
        client.disconnect()

if __name__ == "__main__":
    main()
