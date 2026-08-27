# SIH26002 — NER Smart Logistics Platform

> **Smart India Hackathon 2026** | MDoNER | Smart Automation | Software

AI-powered logistics intelligence for India's North Eastern Region — real-time road monitoring, disruption prediction, route optimization, and offline field reporting across 8 states.

---

## Quick Start

```bash
git clone https://github.com/Himanshu121865/SIH26002.git
cd SIH26002
make dev
```

Frontend: **http://localhost:3000** — API docs: **http://localhost:8000/docs**

---

## PS Requirements vs Implementation

| Requirement | Status | Implementation |
|---|---|---|
| Monitor road/bridge accessibility | ✅ | 285K real OSM road segments across 8 NER states |
| Predict disruptions (landslides, floods, rain) | ✅ | XGBoost + RF model, 94% accuracy |
| AI-based alternate route suggestions | ✅ | OSRM integration + risk scoring |
| GPS vehicle tracking | ✅ | 25 vehicles with real-time positions |
| Automated alerts | ✅ | Severity-based alerts (critical/high/moderate/low) |
| Geo-tagged field reports | ✅ | Offline-capable form with IndexedDB sync |
| Centralized dashboard | ✅ | District connectivity, bottlenecks, emergency routes |
| Multilingual + offline support | ✅ | EN/BN/HI/AS + PWA with Service Worker |

---

## Pages

| Page | What It Shows |
|---|---|
| **Dashboard** (`/`) | Stats, live map (vehicles + disruptions + heatmap), Siliguri monitor, weather, alerts |
| **Vehicle Tracking** (`/tracking`) | Fleet map with markers + popups, vehicle list |
| **Disruptions** (`/disruptions`) | Disruption heatmap, severity-sorted list |
| **Districts** (`/districts`) | 8 NER states with connectivity scores, filters |
| **Analytics** (`/analytics`) | Vulnerability charts, disruption breakdown, road density by state |
| **Emergency** (`/emergency`) | 6 critical corridors with live status |
| **Reports** (`/reports`) | Submit geo-tagged reports, offline sync indicator |

---

## API (16 endpoints)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Health check |
| GET | `/api/v1/routing/roads.geojson` | Road network GeoJSON |
| GET | `/api/v1/routing/stats` | Counts (roads, vehicles, disruptions, alerts) |
| POST | `/api/v1/routing/optimize` | Route optimization (OSRM/Valhalla) |
| GET | `/api/v1/routing/weather` | Live weather (Open-Meteo) |
| GET | `/api/v1/routing/ner-weather` | Weather for 10 NER cities |
| GET | `/api/v1/routing/predict-disruption` | ML risk prediction |
| GET | `/api/v1/routing/disruptions` | Active disruptions |
| GET | `/api/v1/routing/siliguri-status` | Siliguri corridor status |
| GET | `/api/v1/routing/districts` | District connectivity data |
| GET | `/api/v1/routing/analytics` | Analytics aggregations |
| GET | `/api/v1/tracking/vehicles` | Tracked vehicles |
| POST | `/api/v1/tracking/vehicles/ingest` | Ingest GPS position |
| GET | `/api/v1/alerts/active` | Active alerts |
| POST | `/api/v1/reports/submit` | Submit field report |
| GET | `/api/v1/reports/recent` | Recent field reports |

---

## Tech Stack

| Layer | Tech |
|---|---|
| Frontend | React 18, MapLibre GL, Deck.gl, Recharts, Vite, TypeScript |
| Backend | FastAPI, SQLAlchemy, SQLite, Python 3.12 |
| ML | XGBoost, scikit-learn, pandas, joblib |
| Data | OpenStreetMap, Open-Meteo API, Census 2011 |
| Offline | Service Worker, IndexedDB, background sync |

---

## Data

| Source | Data |
|---|---|
| OpenStreetMap | 285K road segments (NER PBF extract) |
| Open-Meteo | Live weather for 10 NER cities |
| Census 2011 | District population, road density |

| DB Table | Rows |
|---|---|
| road_segments | 285,854 |
| vehicle_positions | 25 |
| disruption_events | 15 |
| alerts | 10 |
| districts | 8 |

---

## Make Commands

```
make dev       # Start backend + frontend
make install   # Install dependencies
make seed      # Re-seed database
make clean     # Remove DB, venv, node_modules
make test      # Verify compilation
```
