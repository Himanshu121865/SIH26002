"""
Parse NER OSM PBF and seed SQLite with road segments.
Run from backend/: source .venv/bin/activate && python3 ../ml/seed_roads.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

import osmium
from models.database import init_db, SessionLocal
from models.schema import RoadSegment, District, SiliguriCorridor

OSM_FILE = Path(__file__).resolve().parent.parent / "data" / "osm" / "north-eastern-zone-latest.osm.pbf"

HIGHWAY_TYPES = {
    "motorway", "motorway_link", "trunk", "trunk_link",
    "primary", "primary_link", "secondary", "secondary_link",
    "tertiary", "tertiary_link", "unclassified", "residential",
    "track", "service",
}


class RoadHandler(osmium.SimpleHandler):
    def __init__(self):
        super().__init__()
        self.nodes = {}
        self.roads = []

    def node(self, n):
        self.nodes[n.id] = (n.location.lat, n.location.lon)

    def way(self, w):
        highway = w.tags.get("highway")
        if highway not in HIGHWAY_TYPES:
            return

        nd_refs = [nd.ref for nd in w.nodes]
        if len(nd_refs) < 2:
            return

        coords = [self.nodes.get(ref) for ref in nd_refs]
        coords = [c for c in coords if c is not None]
        if len(coords) < 2:
            return

        self.roads.append({
            "osm_id": str(w.id),
            "name": w.tags.get("name"),
            "highway_type": highway,
            "surface_type": w.tags.get("surface"),
            "start_lat": coords[0][0],
            "start_lon": coords[0][1],
            "end_lat": coords[-1][0],
            "end_lon": coords[-1][1],
        })


NER_STATES = [
    ("Arunachal Pradesh", "Itanagar"),
    ("Assam", "Dispur"),
    ("Manipur", "Imphal"),
    ("Meghalaya", "Shillong"),
    ("Mizoram", "Aizawl"),
    ("Nagaland", "Kohima"),
    ("Sikkim", "Gangtok"),
    ("Tripura", "Agartala"),
]


def main():
    print("=== NER Road Network Seeder ===")

    init_db()
    db = SessionLocal()

    for state, capital in NER_STATES:
        if not db.query(District).filter_by(state_name=state).first():
            db.add(District(state_name=state, district_name=capital,
                            connectivity_score=0.5, resilience_score=0.5))
    if not db.query(SiliguriCorridor).first():
        db.add(SiliguriCorridor())
    db.commit()

    existing = db.query(RoadSegment).count()
    if existing > 0:
        print(f"Already have {existing} roads, skipping")
        db.close()
        return

    print(f"Parsing {OSM_FILE} ...")
    handler = RoadHandler()
    handler.apply_file(str(OSM_FILE), locations=True)

    print(f"Found {len(handler.roads)} road segments, inserting...")
    batch = []
    for i, road in enumerate(handler.roads):
        batch.append(RoadSegment(**road))
        if len(batch) >= 5000:
            db.add_all(batch)
            db.commit()
            print(f"  {i + 1}/{len(handler.roads)}")
            batch = []

    if batch:
        db.add_all(batch)
        db.commit()

    total = db.query(RoadSegment).count()
    print(f"Done! {total} road segments in database")
    db.close()


if __name__ == "__main__":
    main()
