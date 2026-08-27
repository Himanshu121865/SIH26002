from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from models.database import SessionLocal

router = APIRouter()


class VehiclePosition(BaseModel):
    vehicle_id: str
    lat: float
    lon: float
    speed_kmh: float
    heading: float
    vehicle_type: str = "truck"
    cargo_type: str = "general"
    driver_name: str = ""


@router.get("/vehicles")
async def get_all_vehicles():
    db = SessionLocal()
    try:
        rows = db.execute(
            text("SELECT vehicle_id, driver_name, lat, lon, speed_kmh, heading, "
                 "vehicle_type, cargo_type, last_updated "
                 "FROM vehicle_positions ORDER BY last_updated DESC")
        ).fetchall()
        vehicles = [
            {
                "vehicle_id": r[0],
                "driver_name": r[1],
                "lat": r[2],
                "lon": r[3],
                "speed_kmh": r[4],
                "heading": r[5],
                "vehicle_type": r[6],
                "cargo_type": r[7],
                "last_updated": str(r[8]),
            }
            for r in rows
        ]
        return {"vehicles": vehicles, "count": len(vehicles)}
    finally:
        db.close()


@router.get("/vehicles/{vehicle_id}")
async def get_vehicle(vehicle_id: str):
    db = SessionLocal()
    try:
        row = db.execute(
            text("SELECT vehicle_id, driver_name, lat, lon, speed_kmh, heading, "
                 "vehicle_type, cargo_type, last_updated "
                 "FROM vehicle_positions WHERE vehicle_id = :vid"),
            {"vid": vehicle_id},
        ).first()
        if not row:
            raise HTTPException(status_code=404, detail="Vehicle not found")
        return {
            "vehicle_id": row[0],
            "driver_name": row[1],
            "lat": row[2],
            "lon": row[3],
            "speed_kmh": row[4],
            "heading": row[5],
            "vehicle_type": row[6],
            "cargo_type": row[7],
            "last_updated": str(row[8]),
        }
    finally:
        db.close()


@router.post("/vehicles/ingest")
async def ingest_position(pos: VehiclePosition):
    import uuid
    from datetime import datetime

    db = SessionLocal()
    try:
        db.execute(
            text("INSERT INTO vehicle_positions "
                 "(id, vehicle_id, driver_name, lat, lon, speed_kmh, heading, vehicle_type, "
                 "cargo_type, last_updated) "
                 "VALUES (:id, :vid, :driver, :lat, :lon, :speed, :heading, :vtype, :ctype, :updated)"),
            {
                "id": str(uuid.uuid4()),
                "vid": pos.vehicle_id,
                "driver": pos.driver_name,
                "lat": pos.lat,
                "lon": pos.lon,
                "speed": pos.speed_kmh,
                "heading": pos.heading,
                "vtype": pos.vehicle_type,
                "ctype": pos.cargo_type,
                "updated": datetime.utcnow(),
            },
        )
        db.commit()
        return {"status": "received", "vehicle_id": pos.vehicle_id}
    finally:
        db.close()
