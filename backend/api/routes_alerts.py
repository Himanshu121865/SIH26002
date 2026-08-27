from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy import text
from models.database import SessionLocal

router = APIRouter()


@router.get("/active")
async def get_active_alerts():
    db = SessionLocal()
    try:
        rows = db.execute(
            text("SELECT id, alert_type, severity, title, message, lat, lon, created_at "
                 "FROM alerts WHERE is_active = 1 ORDER BY created_at DESC LIMIT 50")
        ).fetchall()
        alerts = [
            {
                "id": r[0],
                "type": r[1],
                "severity": r[2],
                "title": r[3],
                "message": r[4],
                "lat": r[5],
                "lon": r[6],
                "created_at": str(r[7]),
            }
            for r in rows
        ]
        return {"alerts": alerts, "count": len(alerts)}
    finally:
        db.close()


@router.get("/history")
async def get_alert_history():
    db = SessionLocal()
    try:
        rows = db.execute(
            text("SELECT id, alert_type, severity, title, message, lat, lon, created_at "
                 "FROM alerts ORDER BY created_at DESC LIMIT 100")
        ).fetchall()
        alerts = [
            {
                "id": r[0],
                "type": r[1],
                "severity": r[2],
                "title": r[3],
                "message": r[4],
                "lat": r[5],
                "lon": r[6],
                "created_at": str(r[7]),
            }
            for r in rows
        ]
        return {"alerts": alerts, "count": len(alerts)}
    finally:
        db.close()


@router.post("/subscribe")
async def subscribe_alerts():
    return {"status": "subscribed"}
