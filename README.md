# SIH26002 — AI-Based Smart Logistics and Accessibility Intelligence Platform for NER

> **Smart India Hackathon 2026** | PS Org: MDoNER | Theme: Smart Automation | Category: Software

An AI-powered logistics intelligence platform for India's North Eastern Region (NER), providing real-time road accessibility monitoring, disruption prediction, and risk-aware route planning across the 8 northeastern states.

---

## Live Demo

```bash
# Backend
cd backend && source .venv/bin/activate
uvicorn main:app --reload --port 8000

# Frontend
cd frontend && npx vite --port 3000
```

Open **http://localhost:3000** — Backend API docs at **http://localhost:8000/docs**

---

## What It Does

| Feature | Description |
|---|---|
| **Road Network Map** | 285,654 real road segments from OpenStreetMap covering all 8 NER states |
| **Live Weather** | Real-time temperature, rainfall, wind from Open-Meteo for any NER location |
| **Disruption Prediction** | XGBoost + RandomForest ML model predicting landslide/flood risk from weather + terrain |
| **Vehicle Tracking** | GPS fleet tracking with real-time positions across NER cities |
| **Siliguri Corridor Monitor** | Dedicated monitoring for the 22km-wide chicken neck corridor |
| **Alert System** | Active alerts for weather, disruptions, and route hazards |
| **Field Reports** | Offline-capable incident reporting with photo upload |
| **Multilingual** | English, Bengali, Hindi, Assamese |

---

## Real Data Sources

| Source | Data | Access |
|---|---|---|
| **OpenStreetMap** | 285K road segments (NER extract from Geofabrik) | Free, local PBF file |
| **Open-Meteo** | Live weather (temp, rain, wind, humidity) | Free API, no key |
| **NHAI API Setu** | Highway work zones, accident-prone areas, landslide alerts | Government API |
| **India Meteorological Dept** | Rainfall data, weather warnings | Public data |
| **Census 2011** | District populations, road density | Public data |

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    React Frontend                        │
│  MapLibre GL JS · Deck.gl · Recharts · i18next          │
└──────────────────────┬──────────────────────────────────┘
                       │ /api/v1/*
┌──────────────────────┴──────────────────────────────────┐
│                   FastAPI Backend                        │
│  Routing · Tracking · Alerts · Reports · Weather        │
├─────────────────────────────────────────────────────────┤
│                   SQLite Database                        │
│  285K roads · Vehicles · Disruptions · Alerts           │
├─────────────────────────────────────────────────────────┤
│                   ML Pipeline                            │
│  XGBoost + RandomForest · Open-Meteo Weather            │
└─────────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18, MapLibre GL JS, Deck.gl, Vite, TypeScript |
| Backend | FastAPI, SQLAlchemy, SQLite, Python 3.12 |
| ML | XGBoost, scikit-learn, pandas, joblib |
| Data | OpenStreetMap (osmium), Open-Meteo API |
| Routing | Valhalla (optional, for production routing) |

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Health check |
| GET | `/api/v1/routing/roads.geojson` | Road network GeoJSON (50K features) |
| GET | `/api/v1/routing/stats` | Road + vehicle + disruption counts |
| GET | `/api/v1/routing/weather?lat=&lon=` | Live weather from Open-Meteo |
| GET | `/api/v1/routing/predict-disruption?lat=&lon=&slope_deg=` | ML risk prediction |
| GET | `/api/v1/routing/disruptions` | Active disruptions |
| GET | `/api/v1/routing/siliguri-status` | Siliguri Corridor status |
| GET | `/api/v1/tracking/vehicles` | All tracked vehicles |
| POST | `/api/v1/tracking/vehicles/ingest` | Ingest GPS position |
| GET | `/api/v1/alerts/active` | Active alerts |
| POST | `/api/v1/reports/submit` | Submit field report |

Full API docs: **http://localhost:8000/docs**

---

## Quick Start

### Prerequisites
- Python 3.12+ (with `uv` package manager)
- Node.js 18+

### Setup

```bash
# Clone
git clone <repo-url>
cd SIH26002

# Backend
cd backend
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt

# Seed road network from OSM (one-time, ~2 min)
python3 ../ml/seed_roads.py

# Seed demo data
python3 -c "import sys; sys.path.insert(0,'../ml'); from seed_demo_data import seed_all; seed_all()"

# Frontend
cd ../frontend
npm install
```

### Run

```bash
# Terminal 1 — Backend
cd backend && source .venv/bin/activate
uvicorn main:app --reload --port 8000

# Terminal 2 — Frontend
cd frontend && npx vite --port 3000
```

---

## Project Structure

```
SIH26002/
├── backend/                  # FastAPI + SQLite
│   ├── main.py               # Entrypoint + WebSocket + init_db
│   ├── config.py             # Settings
│   ├── services/
│   │   ├── weather.py        # Open-Meteo integration
│   │   └── disruption_predictor.py  # ML model + heuristic
│   ├── api/                  # Route handlers
│   └── models/               # SQLAlchemy schema
├── frontend/                 # React + Vite + MapLibre
│   └── src/
│       ├── pages/            # Dashboard, Tracking, Disruptions, Reports
│       └── components/       # Map, Stats, Alerts, Sidebar
├── ml/                       # ML pipeline
│   ├── seed_roads.py         # OSM PBF → SQLite
│   ├── seed_demo_data.py     # Demo vehicles/disruptions/alerts
│   ├── train_disruption.py   # XGBoost + RF training
│   └── generate_training_data.py  # Synthetic data generator
├── data/osm/                 # NER OSM extract (105 MB)
├── sql/                      # PostGIS schema (Docker)
└── routing/                  # Valhalla config
```

---

## ML Model

**Disruption Prediction** — predicts landslide/flood risk from:
- Rainfall (1h, 24h, 7d accumulative)
- Terrain (slope, elevation, distance to river)
- Soil moisture, historical landslides
- Road surface quality

**Performance:** 94% accuracy, XGBoost + Random Forest ensemble

```bash
# Retrain
cd ml
python3 generate_training_data.py
python3 train_disruption.py --data data/ner_disruption_training.csv --output models/disruption_model.pkl
```

---

## Team

| Role | Member |
|---|---|
| ML Lead | — |
| Backend Lead | — |
| Frontend Lead | — |
| GIS Specialist | — |
| Data Engineer | — |
| Presenter | — |

---

## License

Internal use for Smart India Hackathon 2026.
