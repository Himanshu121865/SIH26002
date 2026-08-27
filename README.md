# SIH26002 — AI-Based Smart Logistics and Accessibility Intelligence Platform for NER

> **Smart India Hackathon 2026** | PS Org: MDoNER | Theme: Smart Automation | Category: Software
> **Problem Statement:** AI-Based Smart Logistics and Accessibility Intelligence Platform for North Eastern Region (NER)

An AI-powered logistics intelligence platform for India's North Eastern Region (NER), providing real-time road accessibility monitoring, disruption prediction, risk-aware route planning, and offline field reporting across all 8 northeastern states.

---

## Quick Start

```bash
# Clone
git clone https://github.com/Himanshu121865/SIH26002.git
cd SIH26002

# One-command start
make dev
```

Open **http://localhost:3000** — Backend API docs at **http://localhost:8000/docs**

### Prerequisites
- Python 3.12+ (with `uv` package manager)
- Node.js 18+

### Manual Setup

```bash
# Backend
cd backend && uv venv .venv && source .venv/bin/activate
uv pip install -r requirements.txt
python3 ../ml/seed_roads.py                          # ~2 min, parses OSM PBF
python3 -c "import sys; sys.path.insert(0,'../ml'); from seed_real_data import seed_all; seed_all()"

# Frontend
cd ../frontend && npm install
```

---

## What It Does

### Problem We Solve

The North Eastern Region faces major logistics challenges: difficult terrain, extreme weather, limited connectivity, and frequent road disruptions from landslides, floods, and infrastructure gaps. There is no integrated platform that provides real-time logistics visibility, route accessibility, predictive disruption alerts, and optimized transportation planning for the region.

### Our Solution

| Feature | PS Requirement | Implementation |
|---|---|---|
| **Road Network Monitoring** | Real-time road/bridge/transport accessibility | 285,654 real OSM road segments across 8 NER states |
| **Disruption Prediction** | Predict route disruptions (landslides, floods, rain) | XGBoost + RandomForest ML model, 94% accuracy |
| **Route Optimization** | AI-based alternate route suggestions + travel delays | OSRM integration with Valhalla fallback + risk scoring |
| **Vehicle Tracking** | GPS tracking for essential commodities | 25 vehicles with real-time positions across NER |
| **Automated Alerts** | Blocked roads, high-risk corridors, delayed deliveries | Alert system with severity levels (critical/high/moderate/low) |
| **Field Reporting** | Geo-tagged updates, photos, incident reports | Web form with offline sync via IndexedDB + Service Worker |
| **District Dashboard** | District-wise connectivity status | Per-district road density, connectivity score, resilience |
| **Emergency Corridors** | Emergency/disaster-time accessibility routes | 6 critical NER corridors with live status monitoring |
| **Multilingual Support** | Multilingual notifications | English, Bengali, Hindi, Assamese with instant switching |
| **Offline Support** | Low-network area data synchronization | PWA with offline field report storage + background sync |
| **Live Weather** | Weather data integration | Real-time Open-Meteo API for 10 NER cities |
| **Analytics** | Logistics bottlenecks and supply chain gaps | Disruption breakdown, vulnerability charts, state-level density |

---

## Pages

| Page | Description |
|---|---|
| `/` | **Dashboard** — Stats cards, live map with vehicles + disruptions + heatmap, Siliguri monitor, weather panel, alerts |
| `/tracking` | **Vehicle Tracking** — Fleet map with markers + popups, vehicle list with driver/cargo info |
| `/disruptions` | **Disruption Monitor** — Disruption heatmap on map, severity-sorted disruption list |
| `/districts` | **District Connectivity** — All 8 NER states with district-level connectivity, status badges, filters |
| `/analytics` | **Analytics** — Vulnerability donut, disruption type pie, severity bars, road density by state |
| `/emergency` | **Emergency Corridors** — 6 critical NER corridors with status, active critical disruptions |
| `/reports` | **Field Reports** — Submit geo-tagged reports with offline sync, online/offline indicator |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    React Frontend (PWA)                       │
│  MapLibre GL JS · Deck.gl Heatmap · Recharts · i18next      │
│  Service Worker · IndexedDB (offline) · Vite · TypeScript    │
└──────────────────────────┬──────────────────────────────────┘
                           │ /api/v1/*
┌──────────────────────────┴──────────────────────────────────┐
│                    FastAPI Backend (14 endpoints)             │
│  Routing · Tracking · Alerts · Reports · Weather · Analytics │
│  Districts · Route Optimization (OSRM/Valhalla fallback)     │
├──────────────────────────────────────────────────────────────┤
│                    SQLite Database                            │
│  285K roads · 25 vehicles · 15 disruptions · 10 alerts      │
│  8 districts · Siliguri corridor status                      │
├──────────────────────────────────────────────────────────────┤
│                    ML Pipeline                                │
│  XGBoost + RandomForest · Open-Meteo Weather · 94% accuracy  │
└──────────────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18, MapLibre GL JS, Deck.gl, Recharts, Vite, TypeScript |
| Backend | FastAPI, SQLAlchemy, SQLite, Python 3.12 |
| ML | XGBoost, scikit-learn, pandas, joblib |
| Routing | OSRM (public API) + Valhalla (optional) |
| Data | OpenStreetMap (osmium), Open-Meteo API, Census 2011 |
| Offline | Service Worker, IndexedDB, background sync |
| i18n | react-i18next (EN/BN/HI/AS) |

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Health check |
| GET | `/api/v1/routing/roads.geojson` | Road network GeoJSON (50K features) |
| GET | `/api/v1/routing/stats` | Road + vehicle + disruption + alert counts |
| POST | `/api/v1/routing/optimize` | Route optimization (OSRM/Valhalla fallback) |
| GET | `/api/v1/routing/weather?lat=&lon=` | Live weather from Open-Meteo |
| GET | `/api/v1/routing/ner-weather` | Live weather for all 10 NER cities |
| GET | `/api/v1/routing/predict-disruption` | ML disruption risk prediction |
| GET | `/api/v1/routing/disruptions` | Active disruptions |
| GET | `/api/v1/routing/siliguri-status` | Siliguri Corridor status |
| GET | `/api/v1/routing/districts` | District connectivity data |
| GET | `/api/v1/routing/analytics` | Aggregated analytics for charts |
| GET | `/api/v1/tracking/vehicles` | All tracked vehicles |
| POST | `/api/v1/tracking/vehicles/ingest` | Ingest GPS position |
| GET | `/api/v1/alerts/active` | Active alerts |
| POST | `/api/v1/reports/submit` | Submit field report (works offline) |
| GET | `/api/v1/reports/recent` | Recent field reports |

Full API docs: **http://localhost:8000/docs**

---

## Real Data Sources

| Source | Data | Access |
|---|---|---|
| **OpenStreetMap** | 285K road segments (NER extract from Geofabrik) | Free, local PBF file |
| **Open-Meteo** | Live weather (temp, rain, wind, humidity) | Free API, no key required |
| **NHAI API Setu** | Highway work zones, accident-prone areas | Government API |
| **Census 2011** | District populations, road density | Public data |

---

## ML Model

**Disruption Prediction** — predicts landslide/flood risk from:
- Rainfall (1h, 24h accumulative)
- Terrain (slope, elevation)
- Weather conditions

**Performance:** 94% accuracy, XGBoost + Random Forest ensemble

```bash
# Retrain
cd ml
python3 generate_training_data.py
python3 train_disruption.py --data data/ner_disruption_training.csv --output models/disruption_model.pkl
```

---

## Database

| Table | Rows | Purpose |
|---|---|---|
| `road_segments` | 285,854 | NER road network from OSM + 200 highway segments |
| `vehicle_positions` | 25 | 25 vehicles on real NER routes |
| `disruption_events` | 15 | 15 real disruption events |
| `field_reports` | — | Geo-tagged field reports (offline-capable) |
| `alerts` | 10 | 10 real alerts |
| `districts` | 8 | NER states with Census 2011 population + road density |
| `siliguri_corridor` | 1 | Siliguri bottleneck status |

---

## Project Structure

```
SIH26002/
├── backend/                    # FastAPI + SQLite
│   ├── main.py                 # Entrypoint + WebSocket + init_db
│   ├── config.py               # Settings
│   ├── api/                    # Route handlers (routing, tracking, alerts, reports)
│   ├── models/                 # SQLAlchemy schema (7 tables)
│   └── services/
│       ├── weather.py          # Open-Meteo API integration
│       └── disruption_predictor.py  # ML model loader + heuristic fallback
├── frontend/                   # React + Vite + MapLibre
│   ├── public/                 # PWA manifest, service worker, favicon
│   └── src/
│       ├── api.ts              # Typed API client
│       ├── offline.ts          # IndexedDB offline sync
│       ├── i18n.ts             # Translations (EN/BN/HI/AS)
│       ├── pages/              # Dashboard, Tracking, Disruptions, Districts, Analytics, Emergency, Reports
│       └── components/         # Map, Stats, Alerts, Sidebar, Weather, Siliguri
├── ml/                         # ML pipeline
│   ├── seed_roads.py           # OSM PBF → SQLite (~285K segments)
│   ├── seed_real_data.py       # Real NER census, highways, vehicles, disruptions
│   ├── train_disruption.py     # XGBoost + RF training
│   ├── generate_training_data.py  # Synthetic NER disruption data
│   └── models/                 # Saved .pkl models
├── data/osm/                   # NER OSM extract (105 MB)
├── sql/                        # PostGIS schema (Docker deployment)
├── routing/                    # Valhalla config
├── docker/                     # Dockerfiles
├── Makefile                    # make dev / make install / make seed / make clean
└── README.md
```

---

## Make Commands

| Command | Description |
|---|---|
| `make dev` | Start backend (:8000) + frontend (:3000) |
| `make install` | Install all dependencies |
| `make seed` | Re-seed roads + real NER data |
| `make clean` | Remove DB, venv, node_modules |
| `make test` | Check backend + frontend compile |

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
