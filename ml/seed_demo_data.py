import uuid
import numpy as np
from datetime import datetime, timedelta
from sqlalchemy import text
from models.database import SessionLocal


NER_CITIES = [
    ("Guwahati", 26.1445, 91.7362),
    ("Shillong", 25.5788, 91.8933),
    ("Imphal", 24.8170, 93.9368),
    ("Agartala", 23.8315, 91.2869),
    ("Aizawl", 23.7271, 92.7176),
    ("Kohima", 25.6586, 94.1086),
    ("Gangtok", 27.3389, 88.6065),
    ("Itanagar", 27.0844, 93.6958),
    ("Dibrugarh", 27.4728, 94.9120),
    ("Silchar", 24.8333, 92.7789),
]


def seed_vehicles(n: int = 25):
    np.random.seed(42)
    db = SessionLocal()
    try:
        for i in range(n):
            city = NER_CITIES[i % len(NER_CITIES)]
            lat = city[1] + np.random.uniform(-0.1, 0.1)
            lon = city[2] + np.random.uniform(-0.1, 0.1)
            vid = f"NER-{1000 + i}"

            db.execute(
                text("INSERT OR REPLACE INTO vehicle_positions "
                     "(id, vehicle_id, driver_name, lat, lon, speed_kmh, heading, vehicle_type, "
                     "cargo_type, cargo_weight_kg, last_updated) "
                     "VALUES (:id, :vid, :driver, :lat, :lon, :speed, :heading, :vtype, "
                     ":ctype, :cweight, :updated)"),
                {
                    "id": str(uuid.uuid4()),
                    "vid": vid,
                    "driver": f"Driver {i + 1}",
                    "lat": lat, "lon": lon,
                    "speed": round(float(np.random.uniform(20, 80)), 1),
                    "heading": round(float(np.random.uniform(0, 360)), 1),
                    "vtype": np.random.choice(["truck", "van", "tanker"]),
                    "ctype": np.random.choice(["general", "food", "medicine", "fuel", "construction"]),
                    "cweight": int(np.random.randint(1000, 20000)),
                    "updated": datetime.utcnow(),
                },
            )
        db.commit()
        print(f"Seeded {n} vehicles")
    finally:
        db.close()


def seed_disruptions(n: int = 15):
    np.random.seed(42)
    db = SessionLocal()
    try:
        types = ["landslide", "flood", "road_damage", "accident", "fallen_tree"]
        severities = ["low", "moderate", "high", "critical"]

        for i in range(n):
            city = NER_CITIES[i % len(NER_CITIES)]
            etype = np.random.choice(types)
            sev = np.random.choice(severities, p=[0.2, 0.4, 0.3, 0.1])

            db.execute(
                text("INSERT INTO disruption_events "
                     "(id, event_type, severity, lat, lon, description, reported_by, created_at) "
                     "VALUES (:id, :etype, :sev, :lat, :lon, :desc, :reporter, :created)"),
                {
                    "id": str(uuid.uuid4()),
                    "etype": etype,
                    "sev": sev,
                    "lat": city[1] + float(np.random.uniform(-0.05, 0.05)),
                    "lon": city[2] + float(np.random.uniform(-0.05, 0.05)),
                    "desc": f"{etype.replace('_', ' ').title()} reported near {city[0]}",
                    "reporter": f"field_agent_{np.random.randint(1, 20)}",
                    "created": datetime.utcnow() - timedelta(hours=int(np.random.randint(0, 72))),
                },
            )
        db.commit()
        print(f"Seeded {n} disruptions")
    finally:
        db.close()


def seed_alerts(n: int = 10):
    np.random.seed(42)
    db = SessionLocal()
    try:
        for i in range(n):
            city = NER_CITIES[i % len(NER_CITIES)]
            db.execute(
                text("INSERT INTO alerts "
                     "(id, alert_type, severity, title, message, lat, lon, is_active, created_at) "
                     "VALUES (:id, :atype, :sev, :title, :msg, :lat, :lon, :active, :created)"),
                {
                    "id": str(uuid.uuid4()),
                    "atype": np.random.choice(["weather", "disruption", "route", "system"]),
                    "sev": np.random.choice(["info", "warning", "critical"]),
                    "title": f"Alert: {city[0]} region",
                    "msg": f"Monitor conditions in {city[0]} area",
                    "lat": city[1],
                    "lon": city[2],
                    "active": 1,
                    "created": datetime.utcnow() - timedelta(hours=int(np.random.randint(0, 48))),
                },
            )
        db.commit()
        print(f"Seeded {n} alerts")
    finally:
        db.close()


def seed_all():
    print("=== Seeding Demo Data ===")
    seed_vehicles(25)
    seed_disruptions(15)
    seed_alerts(10)
    print("Done!")


if __name__ == "__main__":
    seed_all()
