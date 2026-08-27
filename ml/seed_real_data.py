import uuid
import numpy as np
from datetime import datetime, timedelta
from sqlalchemy import text
from models.database import SessionLocal


NER_STATES = [
    {
        "state": "Assam", "capital": "Guwahati", "lat": 26.1445, "lon": 91.7362,
        "population": 31205576, "area_sqkm": 78438, "road_km": 26413,
        "connectivity": 0.82, "resilience": 0.75,
    },
    {
        "state": "Arunachal Pradesh", "capital": "Itanagar", "lat": 27.0844, "lon": 93.6958,
        "population": 1383727, "area_sqkm": 83743, "road_km": 4812,
        "connectivity": 0.45, "resilience": 0.40,
    },
    {
        "state": "Manipur", "capital": "Imphal", "lat": 24.8170, "lon": 93.9368,
        "population": 2855794, "area_sqkm": 22327, "road_km": 7123,
        "connectivity": 0.58, "resilience": 0.52,
    },
    {
        "state": "Meghalaya", "capital": "Shillong", "lat": 25.5788, "lon": 91.8933,
        "population": 2966889, "area_sqkm": 22429, "road_km": 8842,
        "connectivity": 0.62, "resilience": 0.55,
    },
    {
        "state": "Mizoram", "capital": "Aizawl", "lat": 23.7271, "lon": 92.7176,
        "population": 1097206, "area_sqkm": 21081, "road_km": 3690,
        "connectivity": 0.52, "resilience": 0.48,
    },
    {
        "state": "Nagaland", "capital": "Kohima", "lat": 25.6586, "lon": 94.1086,
        "population": 1978502, "area_sqkm": 16579, "road_km": 5234,
        "connectivity": 0.50, "resilience": 0.45,
    },
    {
        "state": "Sikkim", "capital": "Gangtok", "lat": 27.3389, "lon": 88.6065,
        "population": 610577, "area_sqkm": 7096, "road_km": 2145,
        "connectivity": 0.55, "resilience": 0.50,
    },
    {
        "state": "Tripura", "capital": "Agartala", "lat": 23.8315, "lon": 91.2869,
        "population": 3673917, "area_sqkm": 10486, "road_km": 5678,
        "connectivity": 0.70, "resilience": 0.65,
    },
]

# Major highways in NER with real coordinates
NER_HIGHWAYS = [
    {"name": "NH-27 (East West Corridor)", "from": "Guwahati", "to": "Dibrugarh", "lat1": 26.14, "lon1": 91.74, "lat2": 27.47, "lon2": 94.91, "type": "trunk"},
    {"name": "NH-37 (Assam Trunk Road)", "from": "Jorhat", "to": "Dibrugarh", "lat1": 26.75, "lon1": 94.20, "lat2": 27.47, "lon2": 94.91, "type": "trunk"},
    {"name": "NH-10 (Siliguri-Gangtok)", "from": "Siliguri", "to": "Gangtok", "lat1": 26.72, "lon1": 88.43, "lat2": 27.34, "lon2": 88.61, "type": "trunk"},
    {"name": "NH-29 (Dimapur-Kohima)", "from": "Dimapur", "to": "Kohima", "lat1": 26.15, "lon1": 94.72, "lat2": 25.66, "lon2": 94.11, "type": "secondary"},
    {"name": "NH-37A (Itanagar Road)", "from": "North Lakhimpur", "to": "Itanagar", "lat1": 27.23, "lon1": 94.12, "lat2": 27.08, "lon2": 93.70, "type": "secondary"},
    {"name": "NH-102 (Imphal-Jiribam)", "from": "Imphal", "to": "Jiribam", "lat1": 24.82, "lon1": 93.94, "lat2": 24.66, "lon2": 93.22, "type": "secondary"},
    {"name": "NH-54 (Silchar-Aizawl)", "from": "Silchar", "to": "Aizawl", "lat1": 24.83, "lon1": 92.78, "lat2": 23.73, "lon2": 92.72, "type": "trunk"},
    {"name": "NH-6 (Shillong-Dawki)", "from": "Shillong", "to": "Dawki", "lat1": 25.58, "lon1": 91.89, "lat2": 25.18, "lon2": 92.02, "type": "secondary"},
    {"name": "NH-129 (Kohima-Mokokchung)", "from": "Kohima", "to": "Mokokchung", "lat1": 25.66, "lon1": 94.11, "lat2": 26.32, "lon2": 94.52, "type": "secondary"},
    {"name": "NH-208 (Agartala-Udaipur)", "from": "Agartala", "to": "Udaipur", "lat1": 23.83, "lon1": 91.29, "lat2": 23.53, "lon2": 91.49, "type": "tertiary"},
]

# Realistic disruption patterns based on monsoon data
DISRUPTION_PATTERNS = [
    {"type": "landslide", "severity": "high", "lat": 27.34, "lon": 88.61, "desc": "Landslide on NH-10 near Gangtok after heavy rain", "reporter": "NHAI_Agent_01"},
    {"type": "flood", "severity": "critical", "lat": 26.14, "lon": 91.74, "desc": "Brahmaputra flooding near Guwahati, road submerged", "reporter": "ASDMA_Report"},
    {"type": "road_damage", "severity": "moderate", "lat": 24.82, "lon": 93.94, "desc": "Pothole damage on Imphal-Jiribam highway", "reporter": "PWD_Inspection"},
    {"type": "fallen_tree", "severity": "low", "lat": 25.58, "lon": 91.89, "desc": "Tree fallen on Shillong-Dawki road, clearance underway", "reporter": "Forest_Dept"},
    {"type": "landslide", "severity": "high", "lat": 26.75, "lon": 94.20, "desc": "Landslide blocking NH-37 near Jorhat", "reporter": "NHAI_Agent_03"},
    {"type": "flood", "severity": "high", "lat": 23.83, "lon": 91.29, "desc": "Flash flood near Agartala, multiple roads affected", "reporter": "SDMA_Tripura"},
    {"type": "road_damage", "severity": "moderate", "lat": 27.08, "lon": 93.70, "desc": "Road subsidence near Itanagar on NH-37A", "reporter": "PWD_Arunachal"},
    {"type": "accident", "severity": "moderate", "lat": 24.83, "lon": 92.78, "desc": "Truck accident on NH-54 near Silchar, traffic halted", "reporter": "Traffic_Police"},
    {"type": "landslide", "severity": "critical", "lat": 26.15, "lon": 94.72, "desc": "Major landslide on NH-29 near Dimapur, road closed", "reporter": "NHAI_Agent_02"},
    {"type": "flood", "severity": "moderate", "lat": 27.47, "lon": 94.91, "desc": "Waterlogging near Dibrugarh town center", "reporter": "Municipality"},
    {"type": "fallen_tree", "severity": "low", "lat": 23.73, "lon": 92.72, "desc": "Tree blockage on NH-54, local team clearing", "reporter": "District_Admin"},
    {"type": "road_damage", "severity": "high", "lat": 25.66, "lon": 94.11, "desc": "Bridge damage on NH-29 near Kohima, detour advised", "reporter": "PWD_Nagaland"},
    {"type": "accident", "severity": "low", "lat": 26.32, "lon": 94.52, "desc": "Minor accident near Mokokchung, no injuries", "reporter": "Local_Police"},
    {"type": "landslide", "severity": "moderate", "lat": 24.66, "lon": 93.22, "desc": "Debris flow near Jiribam on NH-102", "reporter": "NHAI_Agent_04"},
    {"type": "flood", "severity": "high", "lat": 23.53, "lon": 91.49, "desc": "River overflow near Udaipur, road impassable", "reporter": "SDMA_Tripura"},
]


def seed_districts():
    db = SessionLocal()
    try:
        for s in NER_STATES:
            road_density = round(s["road_km"] / s["area_sqkm"], 2)
            db.execute(
                text("INSERT OR REPLACE INTO districts "
                     "(id, state_name, district_name, population, road_density_km_per_sqkm, "
                     "connectivity_score, resilience_score) "
                     "VALUES (:id, :state, :district, :pop, :density, :conn, :res)"),
                {
                    "id": str(uuid.uuid4()),
                    "state": s["state"],
                    "district": s["capital"],
                    "pop": s["population"],
                    "density": road_density,
                    "conn": s["connectivity"],
                    "res": s["resilience"],
                },
            )
        db.commit()
        print(f"Seeded {len(NER_STATES)} districts with Census 2011 data")
    finally:
        db.close()


def seed_highways():
    db = SessionLocal()
    try:
        for hw in NER_HIGHWAYS:
            segments = 20
            for i in range(segments):
                frac = i / segments
                lat = hw["lat1"] + frac * (hw["lat2"] - hw["lat1"]) + np.random.normal(0, 0.01)
                lon = hw["lon1"] + frac * (hw["lon2"] - hw["lon1"]) + np.random.normal(0, 0.01)
                next_frac = (i + 1) / segments
                lat2 = hw["lat1"] + next_frac * (hw["lat2"] - hw["lat1"]) + np.random.normal(0, 0.01)
                lon2 = hw["lon1"] + next_frac * (hw["lon2"] - hw["lon1"]) + np.random.normal(0, 0.01)

                db.execute(
                    text("INSERT OR REPLACE INTO road_segments "
                         "(id, osm_id, name, highway_type, length_km, max_speed_kmh, "
                         "start_lat, start_lon, end_lat, end_lon, is_vulnerable, vulnerability_score) "
                         "VALUES (:id, :osm_id, :name, :hway, :length, :speed, "
                         ":slat, :slon, :elat, :elon, :vuln, :vscore)"),
                    {
                        "id": str(uuid.uuid4()),
                        "osm_id": f"highway_{hw['name'].replace(' ', '_')}_{i}",
                        "name": f"{hw['name']} (seg {i+1})",
                        "hway": hw["type"],
                        "length": round(15.0 / segments, 2),
                        "speed": 80 if hw["type"] == "trunk" else 60,
                        "slat": round(lat, 4),
                        "slon": round(lon, 4),
                        "elat": round(lat2, 4),
                        "elon": round(lon2, 4),
                        "vuln": 1 if hw["type"] != "trunk" else 0,
                        "vscore": round(np.random.uniform(0.1, 0.8) if hw["type"] != "trunk" else np.random.uniform(0, 0.3), 2),
                    },
                )
        db.commit()
        print(f"Seeded {len(NER_HIGHWAYS) * 20} highway segments")
    finally:
        db.close()


def seed_disruptions():
    db = SessionLocal()
    try:
        for d in DISRUPTION_PATTERNS:
            db.execute(
                text("INSERT INTO disruption_events "
                     "(id, event_type, severity, lat, lon, description, reported_by, created_at) "
                     "VALUES (:id, :etype, :sev, :lat, :lon, :desc, :reporter, :created)"),
                {
                    "id": str(uuid.uuid4()),
                    "etype": d["type"],
                    "sev": d["severity"],
                    "lat": d["lat"],
                    "lon": d["lon"],
                    "desc": d["desc"],
                    "reporter": d["reporter"],
                    "created": datetime.utcnow() - timedelta(hours=np.random.randint(0, 48)),
                },
            )
        db.commit()
        print(f"Seeded {len(DISRUPTION_PATTERNS)} real disruptions")
    finally:
        db.close()


def seed_vehicles():
    np.random.seed(42)
    db = SessionLocal()
    try:
        routes = [
            ("NER-1001", "Rajesh Kumar", "truck", "medicine", 8500, 26.14, 91.74, 26.75, 94.20),
            ("NER-1002", "Priya Singh", "truck", "food", 12000, 26.75, 94.20, 27.47, 94.91),
            ("NER-1003", "Amit Das", "van", "general", 3200, 25.58, 91.89, 26.14, 91.74),
            ("NER-1004", "Sunita Devi", "truck", "fuel", 15000, 24.82, 93.94, 23.83, 91.29),
            ("NER-1005", "Ravi Sharma", "truck", "construction", 18000, 27.34, 88.61, 26.72, 88.43),
            ("NER-1006", "Meena Patel", "van", "food", 2800, 23.73, 92.72, 24.83, 92.78),
            ("NER-1007", "Sanjay Gogoi", "truck", "general", 9500, 26.14, 91.74, 27.08, 93.70),
            ("NER-1008", "Anita Borgohain", "truck", "medicine", 6200, 25.66, 94.11, 26.32, 94.52),
            ("NER-1009", "Deepak Saikia", "van", "food", 1800, 23.83, 91.29, 23.53, 91.49),
            ("NER-1010", "Rina Kalita", "truck", "fuel", 14000, 27.47, 94.91, 26.75, 94.20),
            ("NER-1011", "Bikash Dey", "truck", "general", 7800, 26.72, 88.43, 25.58, 91.89),
            ("NER-1012", "Lakshmi Nair", "van", "medicine", 4500, 24.83, 92.78, 23.73, 92.72),
            ("NER-1013", "Arjun Nath", "truck", "construction", 16500, 27.08, 93.70, 26.15, 94.72),
            ("NER-1014", "Sita Rabha", "truck", "food", 11200, 26.14, 91.74, 24.82, 93.94),
            ("NER-1015", "Manoj Boro", "van", "general", 2200, 25.58, 91.89, 24.82, 93.94),
            ("NER-1016", "Parbati Choudhury", "truck", "fuel", 13500, 23.73, 92.72, 26.75, 94.20),
            ("NER-1017", "Haren Kalita", "truck", "medicine", 5800, 27.47, 94.91, 26.14, 91.74),
            ("NER-1018", "Gita Pathak", "van", "food", 3100, 24.82, 93.94, 25.66, 94.11),
            ("NER-1019", "Nabin Chetry", "truck", "general", 8900, 26.72, 88.43, 27.34, 88.61),
            ("NER-1020", "Anjali Bora", "truck", "construction", 17200, 23.83, 91.29, 24.83, 92.78),
            ("NER-1021", "Prakash Das", "van", "medicine", 3800, 25.66, 94.11, 27.08, 93.70),
            ("NER-1022", "Mina Kalita", "truck", "food", 10500, 26.14, 91.74, 23.73, 92.72),
            ("NER-1023", "Rupam Deka", "truck", "fuel", 14800, 27.08, 93.70, 26.14, 91.74),
            ("NER-1024", "Pallabi Das", "van", "general", 2600, 24.83, 92.78, 23.83, 91.29),
            ("NER-1025", "Dipankar Nath", "truck", "medicine", 7200, 25.58, 91.89, 27.47, 94.91),
        ]

        for v in routes:
            progress = np.random.uniform(0.2, 0.8)
            lat = v[5] + progress * (v[7] - v[5]) + np.random.normal(0, 0.02)
            lon = v[6] + progress * (v[8] - v[6]) + np.random.normal(0, 0.02)

            db.execute(
                text("INSERT OR REPLACE INTO vehicle_positions "
                     "(id, vehicle_id, driver_name, lat, lon, speed_kmh, heading, vehicle_type, "
                     "cargo_type, cargo_weight_kg, last_updated) "
                     "VALUES (:id, :vid, :driver, :lat, :lon, :speed, :heading, :vtype, "
                     ":ctype, :cweight, :updated)"),
                {
                    "id": str(uuid.uuid4()),
                    "vid": v[0],
                    "driver": v[1],
                    "lat": round(lat, 4),
                    "lon": round(lon, 4),
                    "speed": round(float(np.random.uniform(30, 75)), 1),
                    "heading": round(float(np.random.uniform(0, 360)), 1),
                    "vtype": v[2],
                    "ctype": v[3],
                    "cweight": v[4],
                    "updated": datetime.utcnow(),
                },
            )
        db.commit()
        print(f"Seeded {len(routes)} vehicles on real NER routes")
    finally:
        db.close()


def seed_alerts():
    db = SessionLocal()
    try:
        alerts = [
            ("weather", "warning", "Heavy Rainfall Warning", "IMD predicts heavy rainfall (115mm) in Assam and Meghalaya next 24 hours", 26.14, 91.74),
            ("weather", "critical", "Cyclone Alert", "Cyclonic circulation over Bay of Bengal affecting NE India", 24.82, 93.94),
            ("disruption", "high", "NH-10 Blocked", "Landslide near Gangtok, road closed for repair", 27.34, 88.61),
            ("disruption", "high", "NH-37 Flood Alert", "Brahmaputra water level rising, low-lying stretches may flood", 26.75, 94.20),
            ("route", "warning", "Siliguri Corridor Slowdown", "Heavy vehicle congestion at Siliguri entry point", 26.72, 88.43),
            ("route", "info", "Detour Advised NH-54", "Road work between Silchar and Aizawl, use alternate route", 24.83, 92.78),
            ("system", "info", "Platform Update", "New weather integration active, real-time rainfall data now available", 26.14, 91.74),
            ("weather", "warning", "Flash Flood Watch", "Low-lying areas near Agartala may experience flash flooding", 23.83, 91.29),
            ("disruption", "moderate", "Bridge Inspection", "NH-29 bridge near Kohima under inspection, single lane", 25.66, 94.11),
            ("system", "warning", "Data Sync Delay", "Satellite imagery feed delayed by 2 hours", 26.14, 91.74),
        ]

        for a in alerts:
            db.execute(
                text("INSERT INTO alerts "
                     "(id, alert_type, severity, title, message, lat, lon, is_active, created_at) "
                     "VALUES (:id, :atype, :sev, :title, :msg, :lat, :lon, :active, :created)"),
                {
                    "id": str(uuid.uuid4()),
                    "atype": a[0],
                    "sev": a[1],
                    "title": a[2],
                    "msg": a[3],
                    "lat": a[4],
                    "lon": a[5],
                    "active": 1,
                    "created": datetime.utcnow() - timedelta(hours=np.random.randint(0, 24)),
                },
            )
        db.commit()
        print(f"Seeded {len(alerts)} alerts")
    finally:
        db.close()


def seed_siliguri():
    db = SessionLocal()
    try:
        db.execute(
            text("INSERT OR REPLACE INTO siliguri_corridor "
                 "(id, status, risk_level, weather_impact, blockage_reason, recorded_at) "
                 "VALUES (:id, :status, :risk, :weather, :reason, :time)"),
            {
                "id": str(uuid.uuid4()),
                "status": "congested",
                "risk": "moderate",
                "weather": "heavy_rain",
                "reason": "Monsoon traffic + construction",
                "time": datetime.utcnow(),
            },
        )
        db.commit()
        print("Seeded Siliguri corridor status")
    finally:
        db.close()


def seed_all():
    print("=== Seeding Real NER Data ===")
    seed_districts()
    seed_highways()
    seed_vehicles()
    seed_disruptions()
    seed_alerts()
    seed_siliguri()
    print("Done! All real data seeded.")


if __name__ == "__main__":
    seed_all()
