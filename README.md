# Sensor Dashboard

A full-stack IoT monitoring application that consumes MQTT sensor data in real-time, stores it in a database, applies threshold-based alerting, and displays metrics through a React web dashboard.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Core Logic & Functionality](#core-logic--functionality)
- [API Reference](#api-reference)
- [Database Schema](#database-schema)
- [MQTT Integration](#mqtt-integration)
- [Configuration](#configuration)
- [Getting Started](#getting-started)
- [Data Flow](#data-flow)

---

## Overview

The Sensor Dashboard ingests telemetry data from IoT sensors via MQTT, persists readings in a relational database, evaluates them against configurable thresholds, and surfaces the data through a REST API consumed by a React frontend. When any monitored parameter exceeds its limit, an alert is automatically generated and stored.

---

## Architecture

```
┌─────────────────┐     MQTT (sensors/+)      ┌──────────────────────┐
│  IoT Sensors /  │ ───────────────────────► │   Backend (FastAPI)   │
│  Simulators     │   test.mosquitto.org      │   - MQTT subscriber   │
└─────────────────┘                          │   - REST API          │
                                             │   - CRUD + threshold  │
                                             └──────────┬───────────┘
                                                        │
                                                        ▼
                                             ┌──────────────────────┐
                                             │   SQLite / MySQL     │
                                             │   sensor_data.db     │
                                             └──────────┬──────────┘
                                                        │
                                             ┌──────────▼───────────┐
                                             │   Frontend (React)   │
                                             │   - Dashboard        │
                                             │   - Alerts view      │
                                             │   - Raw data view    │
                                             └──────────────────────┘
```

---

## Features

| Feature | Description |
|---------|-------------|
| **Real-time ingestion** | Subscribes to MQTT broker and processes incoming sensor messages |
| **Threshold alerting** | Automatically creates alerts when values exceed configured limits |
| **Dashboard stats** | Total messages, total alerts, and latest sensor readings |
| **Alerts page** | Paginated list of all threshold violations with details |
| **Raw data view** | Paginated table of stored sensor readings |
| **CORS support** | Backend allows cross-origin requests from the frontend |
| **Flexible database** | SQLite (default) or MySQL via environment variables |

---

## Technology Stack

### Backend

| Library | Purpose |
|---------|---------|
| **FastAPI** | REST API framework |
| **SQLAlchemy** | ORM and database access |
| **Pydantic** | Request/response validation |
| **Paho MQTT** | MQTT client for subscribing to sensor topics |
| **Uvicorn** | ASGI server |
| **python-dotenv** | Environment variable loading |

### Frontend

| Library | Purpose |
|---------|---------|
| **React 18** | UI framework |
| **Vite** | Build tool and dev server |
| **React Router** | Client-side routing |
| **Axios** | HTTP client for API calls |

---

## Project Structure

```
sensor_dashboard/
├── backend/
│   ├── main.py          # FastAPI app, routes, lifespan (MQTT start/stop)
│   ├── crud.py          # Database operations (create, read)
│   ├── models.py        # SQLAlchemy models (SensorData, Alert)
│   ├── schemas.py       # Pydantic schemas for API
│   ├── database.py      # Engine, session, DB config
│   ├── mqtt_service.py  # MQTT client, subscription, message handling
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx           # Routes, sidebar, layout
│   │   ├── main.jsx          # Entry point, Router
│   │   ├── api/client.js     # Axios instance, API helpers
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx # Stats + latest reading
│   │   │   ├── AlertsPage.jsx# Alerts table + pagination
│   │   │   └── RawDataView.jsx # Sensor data table + pagination
│   │   └── styles.css
│   ├── index.html
│   └── package.json
├── sensor_data.db       # SQLite database (created at runtime)
└── README.md
```

---

## Core Logic & Functionality

### 1. MQTT Message Processing (`mqtt_service.py`)

**Flow:**

1. Connect to `test.mosquitto.org:1883`
2. Subscribe to topic pattern `sensors/+` (matches `sensors/room1`, `sensors/device42`, etc.)
3. On each message:
   - Decode payload as JSON
   - Parse `temperature`, `humidity`, `voltage`, `current`, `pressure`
   - **Store reading** in `sensor_data` table via CRUD
   - **Check thresholds** for each numeric parameter
   - If value > threshold → create alert in `alerts` table

**Threshold logic:**

```python
THRESHOLDS = {
    "temperature": 30.0,   # °C
    "humidity": 80.0,      # %
    "voltage": 240.0,      # V
    "current": 15.0,       # A
    "pressure": 1100.0     # hPa
}
# Alert when: value > threshold
```

### 2. Database CRUD (`crud.py`)

| Function | Logic |
|----------|-------|
| `create_sensor_reading` | Inserts a new row into `sensor_data` with parsed values and raw JSON |
| `get_sensor_readings` | Returns readings ordered by `timestamp DESC` with `skip`/`limit` pagination |
| `create_alert` | Inserts a new row into `alerts` with topic, violated key, values, and message |
| `get_alerts` | Returns alerts ordered by `timestamp DESC` with pagination |
| `get_dashboard_stats` | Returns `total_messages` (count of sensor_data), `active_alerts_count` (count of alerts), and `latest_readings` (most recent row with topic + raw_payload) |

### 3. API Layer (`main.py`)

- **Lifespan:** On startup → start MQTT client; on shutdown → stop MQTT loop
- **CORS:** Allows all origins for development
- **Dependencies:** `get_db()` yields a session and closes it after each request

### 4. Frontend Logic

| Page | Logic |
|------|-------|
| **Dashboard** | Fetches `/stats` on mount; displays cards and latest reading table; shows error if backend unreachable |
| **Alerts** | Fetches `/alerts` with `skip`/`limit`; pagination with Previous/Next; page size 25 |
| **Raw Data** | Fetches `/data` with pagination; same page size; shows all sensor columns |

All API calls use the base URL from `VITE_API_BASE_URL` or default `http://localhost:8000`.

---

## API Reference

| Endpoint | Method | Params | Response |
|----------|--------|--------|----------|
| `/` | GET | - | `{ "message": "Sensor Dashboard Backend is running" }` |
| `/stats` | GET | - | `{ total_messages, active_alerts_count, latest_readings }` |
| `/data` | GET | `skip`, `limit` | `[SensorReading, ...]` |
| `/alerts` | GET | `skip`, `limit` | `[Alert, ...]` |

**Response shapes:**

- **SensorReading:** `id`, `timestamp`, `topic`, `temperature`, `humidity`, `voltage`, `current`, `pressure`
- **Alert:** `id`, `timestamp`, `topic`, `violated_key`, `actual_value`, `threshold_value`, `message`

---

## Database Schema

### `sensor_data`

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| timestamp | DateTime | Auto-set on insert |
| topic | String(255) | MQTT topic |
| temperature | Float | Nullable |
| humidity | Float | Nullable |
| voltage | Float | Nullable |
| current | Float | Nullable |
| pressure | Float | Nullable |
| raw_payload | JSON | Full message payload |

### `alerts`

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| timestamp | DateTime | Auto-set on insert |
| topic | String(255) | Source MQTT topic |
| violated_key | String(50) | Parameter that exceeded threshold |
| actual_value | Float | Measured value |
| threshold_value | Float | Configured limit |
| message | String(255) | Alert description |

---

## MQTT Integration

- **Broker:** `test.mosquitto.org:1883`
- **Topic pattern:** `sensors/+` (single-level wildcard)
- **Expected payload format (JSON):**

  ```json
  {
    "temperature": 25.5,
    "humidity": 60,
    "voltage": 220,
    "current": 5.2,
    "pressure": 1013
  }
  ```

- **Note:** You need external sensors or a simulator to publish messages to this broker. The dashboard only consumes; it does not publish.

---

## Configuration

### Backend (`.env` or environment)

| Variable | Default | Description |
|----------|---------|-------------|
| `USE_SQLITE` | `1` | Use SQLite; set to `0` for MySQL |
| `DB_USER` | `root` | MySQL user |
| `DB_PASSWORD` | `password` | MySQL password |
| `DB_HOST` | `localhost` | MySQL host |
| `DB_PORT` | `3306` | MySQL port |
| `DB_NAME` | `sensor_dashboard` | MySQL database name |

### Frontend

| Variable | Default | Description |
|----------|---------|-------------|
| `VITE_API_BASE_URL` | `http://localhost:8000` | Backend API base URL |

---

## Getting Started

### Prerequisites

- Python 3.x
- Node.js 18+
- (Optional) MQTT publisher or sensor simulator

### Backend

```bash
cd sensor_dashboard
python -m venv .venv
.\.venv\Scripts\Activate   # Windows
# source .venv/bin/activate  # Linux/macOS

pip install -r backend/requirements.txt
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd sensor_dashboard/frontend
npm install
npm run dev
```

### Access

- Frontend: http://localhost:5173  
- Backend API: http://localhost:8000  
- API docs: http://localhost:8000/docs  

---

## Data Flow

1. **Publish** – External device/simulator publishes JSON to `sensors/<id>` on `test.mosquitto.org`.
2. **Subscribe** – Backend MQTT client receives the message.
3. **Parse & store** – Payload is parsed and inserted into `sensor_data`.
4. **Threshold check** – Each numeric field is compared to `THRESHOLDS`; if exceeded, an alert is inserted.
5. **API** – Frontend fetches `/stats`, `/data`, `/alerts` via Axios.
6. **Render** – React components display the data in tables and cards.

---

## License

Private project. All rights reserved.
